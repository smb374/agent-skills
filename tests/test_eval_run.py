"""Tests for evals/run.py. A fake pi binary records its calls and writes one file."""

import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("eval_run", ROOT / "evals" / "run.py")
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)
PI_SETTINGS = (ROOT / "evals" / "pi-agent" / "settings.json").read_text()

# The agent writes out.txt, which shows the arm. The judge (--no-tools) prints FAKE_JUDGE.
FAKE_PI = r"""#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
with open(os.environ["FAKE_PI_LOG"], "a") as f:
    agent_dir = os.environ.get("PI_CODING_AGENT_DIR")
    settings = os.path.join(agent_dir, "settings.json")
    settings = open(settings).read() if os.path.isfile(settings) else None
    f.write(json.dumps({"args": args, "agent_dir": agent_dir, "settings": settings}) + "\n")
if os.environ.get("FAKE_PI_FAIL"):
    print("boom", file=sys.stderr)
    sys.exit(3)
if "--no-tools" in args:
    text = os.environ.get("FAKE_JUDGE", '{"pass": true, "reason": "ok"}')
else:
    with open("out.txt", "w") as f:
        f.write("skill" if "--skill" in args else "baseline")
    text = "done\u2028next line"
# Like Anthropic, most prompt tokens arrive as cache reads and writes: 4 + 5 + 1 = 10.
usage = {"input": 4, "cacheRead": 5, "cacheWrite": 1, "output": 5, "cost": {"total": 0.001}}
msg = {"role": "assistant", "content": [{"type": "text", "text": text}], "usage": usage}
print(json.dumps({"type": "session"}))
print(json.dumps({"type": "message_end", "message": msg}, ensure_ascii=False))
"""

CHECKS = [
    {
        "id": "uses-skill",
        "type": "file_matches",
        "path": "out.txt",
        "pattern": "^skill$",
    },
    {
        "id": "not-baseline",
        "type": "file_not_matches",
        "path": "out.txt",
        "pattern": "baseline",
    },
    {"id": "missing", "type": "file_not_matches", "path": "nope.txt", "pattern": "x"},
    {"id": "exists", "type": "file_exists", "path": "seed.txt"},
    {"id": "cmd", "type": "command", "run": "cat seed.txt", "stdout": "^seed$"},
    {"id": "cmd-exit", "type": "command", "run": "exit 2", "exit": 2},
    {"id": "judged", "type": "judge", "paths": ["out.txt"], "question": "Is it fine?"},
]


class EvalRunTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.root = self.tmp / "repo"
        (self.root / "skills" / "demo").mkdir(parents=True)
        fixture = self.root / "evals" / "demo" / "fixtures" / "one"
        fixture.mkdir(parents=True)
        (fixture / "seed.txt").write_text("seed\n")
        self.write_cases(
            [{"id": "one", "fixture": "fixtures/one", "prompt": "go", "checks": CHECKS}]
        )
        fake = self.tmp / "pi"
        fake.write_text(FAKE_PI)
        fake.chmod(0o755)
        self.log = self.tmp / "pi.log"
        env = {
            "PI_BIN": str(fake),
            "FAKE_PI_LOG": str(self.log),
            "EVAL_MODEL": "fake/model",
            "EVAL_JUDGE_MODEL": "",
        }
        self.saved_env = {
            k: os.environ.get(k)
            for k in [
                *env,
                "FAKE_PI_FAIL",
                "FAKE_JUDGE",
                "OPENROUTER_API_KEY",
                "OPENCODE_API_KEY",
            ]
        }
        os.environ.update(env)
        self.addCleanup(self.restore_env)
        self.saved_root = run.ROOT
        shutil.copytree(ROOT / "evals" / "pi-agent", self.root / "evals" / "pi-agent")
        run.ROOT = self.root
        self.addCleanup(setattr, run, "ROOT", self.saved_root)

    def restore_env(self):
        for key, value in self.saved_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def write_cases(self, cases):
        (self.root / "evals" / "demo" / "cases.json").write_text(json.dumps(cases))

    def main(self, *args):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = run.main(["demo", "--out", str(self.tmp / "results"), *args])
        return code, out.getvalue(), err.getvalue()

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def result_dir(self):
        (path,) = (self.tmp / "results").iterdir()
        return path

    def test_scores_each_check_per_arm(self):
        code, out, _ = self.main("--runs", "2", "--jobs", "1")
        self.assertEqual(code, 0)
        self.assertIn("| uses-skill | 0/2 | 2/2 |", out)
        self.assertIn("| not-baseline | 0/2 | 2/2 |", out)
        for check in ("missing", "exists", "cmd", "cmd-exit", "judged"):
            expected = "0/2 | 0/2" if check == "missing" else "2/2 | 2/2"
            self.assertIn(f"| {check} | {expected} |", out)
        self.assertIn("| **total** | **8/14** | **12/14** |", out)
        self.assertIn("| input tokens | 20 | 20 |", out)
        self.assertIn("| cost | $0.0020 | $0.0020 |", out)
        result = self.result_dir()
        self.assertTrue((result / "summary.md").is_file())
        self.assertEqual(len(json.loads((result / "verdicts.json").read_text())), 4)
        self.assertEqual(
            (result / "one" / "skill-1" / "workdir" / "out.txt").read_text(), "skill"
        )
        self.assertIn(
            "\u2028", (result / "one" / "skill-1" / "events.jsonl").read_text()
        )

    def test_isolates_each_agent_run(self):
        self.main("--runs", "1")
        agent_calls = [c for c in self.calls() if "--no-tools" not in c["args"]]
        self.assertEqual(len(agent_calls), 2)
        for call in agent_calls:
            args = call["args"]
            for flag in ("--no-session", "-nc", "-ne", "--no-mcp"):
                self.assertIn(flag, args)
            self.assertEqual(
                args[args.index("--tools") + 1], "read,edit,write,grep,find,ls"
            )
            self.assertEqual(args[args.index("--model") + 1], "fake/model")
            self.assertNotIn(str(Path.home()), call["agent_dir"])
            self.assertEqual(call["settings"], PI_SETTINGS)
        skill_args = [c["args"] for c in agent_calls if "--skill" in c["args"]]
        self.assertEqual(
            skill_args[0][skill_args[0].index("--skill") + 1],
            str(self.root / "skills" / "demo"),
        )
        self.assertEqual(sum("--no-skills" in c["args"] for c in agent_calls), 1)

    def test_judge_uses_judge_model(self):
        os.environ["EVAL_JUDGE_MODEL"] = "fake/judge"
        self.main("--runs", "1")
        judge_calls = [c["args"] for c in self.calls() if "--no-tools" in c["args"]]
        self.assertEqual(len(judge_calls), 2)
        self.assertTrue(
            all(a[a.index("--model") + 1] == "fake/judge" for a in judge_calls)
        )
        self.assertIn("=== out.txt", judge_calls[0][-1])
        self.assertTrue(all(a[a.index("--thinking") + 1] == "low" for a in judge_calls))

    def test_pi_settings_pin_the_thinking_level(self):
        settings = json.loads(PI_SETTINGS)
        self.assertEqual(settings["defaultThinkingLevel"], "medium")

    def test_bash_toggle_adds_bash(self):
        self.write_cases(
            [
                {
                    "id": "one",
                    "fixture": "fixtures/one",
                    "prompt": "go",
                    "checks": [],
                    "bash": True,
                }
            ]
        )
        self.main("--runs", "1")
        args = self.calls()[0]["args"]
        self.assertEqual(
            args[args.index("--tools") + 1], "read,edit,write,grep,find,ls,bash"
        )

    def test_judge_reply_that_is_not_a_verdict_fails(self):
        os.environ["FAKE_JUDGE"] = "I think it is fine."
        code, out, _ = self.main("--runs", "1")
        self.assertEqual(code, 0)
        self.assertIn("| judged | 0/1 | 0/1 |", out)
        verdicts = json.loads((self.result_dir() / "verdicts.json").read_text())
        self.assertIn("not a verdict", verdicts[0]["verdicts"][-1]["reason"])

    def test_pi_failure_is_reported_and_exits_1(self):
        os.environ["FAKE_PI_FAIL"] = "1"
        code, out, _ = self.main("--runs", "1")
        self.assertEqual(code, 1)
        self.assertIn("pi exited 3: boom", out)

    def test_missing_model_exits_2(self):
        os.environ["EVAL_MODEL"] = ""
        code, _, err = self.main()
        self.assertEqual(code, 2)
        self.assertIn("EVAL_MODEL is not set", err)

    def test_any_provider_runs_without_a_key_check(self):
        # The runner checks no provider key; pi reports a missing key itself.
        for key in ("OPENROUTER_API_KEY", "OPENCODE_API_KEY"):
            os.environ.pop(key, None)
        for model in ("openrouter/deepseek/x", "opencode-go/kimi-x"):
            with self.subTest(model=model):
                os.environ["EVAL_MODEL"] = model
                code, out, _ = self.main("--runs", "1")
                self.assertEqual(code, 0)
                self.assertIn(f"- model: `{model}`", out)

    def test_progress_is_logged_per_run(self):
        code, _, err = self.main("--runs", "1")
        self.assertEqual(code, 0)
        log = (self.result_dir() / "progress.log").read_text()
        self.assertEqual(err, log)
        self.assertRegex(log, r"start: 2 runs, 4 at a time, results in ")
        self.assertRegex(log, r"run   one baseline-1\n")
        self.assertRegex(log, r"run   one skill-1\n")
        self.assertRegex(log, r"\[1/2\] one \w+-1: \d+/\d+ checks \(\d+s\)\n")
        self.assertRegex(log, r"\[2/2\] one \w+-1: \d+/\d+ checks \(\d+s\)\n")

    def test_bad_case_files_exit_2(self):
        bad = [
            (
                [{"fixture": "fixtures/one", "prompt": "go", "checks": []}],
                "has no 'id'",
            ),
            (
                [{"id": "a", "fixture": "nope", "prompt": "go", "checks": []}],
                "no fixture",
            ),
            (
                [
                    {
                        "id": "a",
                        "fixture": "fixtures/one",
                        "prompt": "go",
                        "checks": [{"id": "x", "type": "magic"}],
                    }
                ],
                "bad check type",
            ),
            (
                [{"id": "a", "fixture": "fixtures/one", "prompt": "go", "checks": []}]
                * 2,
                "duplicate case id",
            ),
            (
                [
                    {
                        "id": "a",
                        "fixture": "fixtures/one",
                        "prompt": "go",
                        "checks": [CHECKS[0], CHECKS[0]],
                    }
                ],
                "unique 'id'",
            ),
        ]
        for cases, message in bad:
            with self.subTest(message=message):
                self.write_cases(cases)
                code, _, err = self.main()
                self.assertEqual(code, 2)
                self.assertIn(message, err)

    def test_unknown_case_id_exits_2(self):
        code, _, err = self.main("--case", "nope")
        self.assertEqual(code, 2)
        self.assertIn("unknown case ids: nope", err)


if __name__ == "__main__":
    unittest.main()
