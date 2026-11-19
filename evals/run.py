#!/usr/bin/env python3
"""Run the eval cases of one skill with headless pi, with and without the skill.

Usage: python3 evals/run.py <skill> [--runs N] [--case ID] [--jobs N]
See evals/README.md for the case format and the settings.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARMS = ("baseline", "skill")
TOOLS = "read,edit,write,grep,find,ls"
PI_TIMEOUT = 900  # seconds; a slow model can take several minutes on a 10-step task
COMMAND_TIMEOUT = 60  # seconds; a command check runs a short script on the fixture
JUDGE_MAX_BYTES = (
    50_000  # the judge skips a larger file, so one log cannot fill its context
)
JUDGE_PROMPT = """You grade the work of a coding agent. Answer one question about the files below.
Reply with one JSON object and nothing else: {{"pass": true or false, "reason": "<one sentence>"}}

Question: {question}

{files}"""


class EvalError(Exception):
    """A runner error: a bad case file, a missing setting, or a failed pi call."""


def load_cases(skill):
    path = ROOT / "evals" / skill / "cases.json"
    if not path.is_file():
        raise EvalError(f"{path} does not exist")
    cases = json.loads(path.read_text())
    seen = set()
    for case in cases:
        for key in ("id", "fixture", "prompt", "checks"):
            if key not in case:
                raise EvalError(f"{path}: case {case.get('id', '?')} has no '{key}'")
        if case["id"] in seen:
            raise EvalError(f"{path}: duplicate case id {case['id']}")
        seen.add(case["id"])
        if not (path.parent / case["fixture"]).is_dir():
            raise EvalError(f"{path}: case {case['id']}: no fixture {case['fixture']}")
        check_ids = [check.get("id") for check in case["checks"]]
        if None in check_ids or len(set(check_ids)) != len(check_ids):
            raise EvalError(
                f"{path}: case {case['id']}: each check needs a unique 'id'"
            )
        for check in case["checks"]:
            if check.get("type") not in CHECKS:
                raise EvalError(
                    f"{path}: case {case['id']}: bad check type {check.get('type')}"
                )
    return cases


def pi(args, cwd, env):
    """Run pi in JSON mode, and return (raw stdout, events)."""
    cmd = [
        env["PI_BIN"],
        "--mode",
        "json",
        "--no-session",
        "-nc",
        "-ne",
        "--no-mcp",
        *args,
    ]
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=PI_TIMEOUT
        )
    except subprocess.TimeoutExpired as e:
        raise EvalError(f"pi timed out after {PI_TIMEOUT} s") from e
    if proc.returncode != 0:
        raise EvalError(f"pi exited {proc.returncode}: {proc.stderr.strip()[-500:]}")
    # Split on LF only: JSON strings can hold U+2028, which splitlines() also splits on.
    try:
        events = [json.loads(line) for line in proc.stdout.split("\n") if line.strip()]
    except json.JSONDecodeError as e:
        raise EvalError(f"pi wrote a line that is not JSON: {e}") from e
    return proc.stdout, events


def assistant_messages(events):
    return [
        e["message"]
        for e in events
        if e.get("type") == "message_end" and e["message"].get("role") == "assistant"
    ]


def reply(events):
    messages = assistant_messages(events)
    if not messages:
        return ""
    content = messages[-1].get("content", [])
    return "".join(b.get("text", "") for b in content if b.get("type") == "text")


def usage(events):
    total = {"input": 0, "output": 0, "cost": 0.0}
    for message in assistant_messages(events):
        u = message.get("usage") or {}
        # Anthropic reports cached prompt tokens apart from "input".
        total["input"] += sum(u.get(k, 0) for k in ("input", "cacheRead", "cacheWrite"))
        total["output"] += u.get("output", 0)
        total["cost"] += (u.get("cost") or {}).get("total", 0)
    return total


def read_text(workdir, rel):
    path = workdir / rel
    return path.read_text() if path.is_file() else None


def check_file_matches(check, workdir, env):
    text = read_text(workdir, check["path"])
    if text is None:
        return False, f"{check['path']} is missing"
    return bool(re.search(check["pattern"], text, re.M)), ""


def check_file_not_matches(check, workdir, env):
    text = read_text(workdir, check["path"])
    if text is None:
        return False, f"{check['path']} is missing"
    match = re.search(check["pattern"], text, re.M)
    return match is None, f"found {match.group(0)!r}" if match else ""


def check_file_exists(check, workdir, env):
    return (workdir / check["path"]).is_file(), ""


def check_command(check, workdir, env):
    proc = subprocess.run(
        ["bash", "-c", check["run"]],
        cwd=workdir,
        capture_output=True,
        text=True,
        timeout=COMMAND_TIMEOUT,
    )
    want = check.get("exit", 0)
    if proc.returncode != want:
        return False, f"exit {proc.returncode}, want {want}"
    if "stdout" in check and not re.search(check["stdout"], proc.stdout, re.M):
        return False, f"stdout does not match {check['stdout']!r}"
    return True, ""


def judge_files(check, workdir):
    if "paths" in check:
        paths = [workdir / p for p in check["paths"]]
    else:
        paths = sorted(p for p in workdir.rglob("*") if p.is_file())
    parts = []
    for path in paths:
        rel = path.relative_to(workdir)
        if not path.is_file():
            parts.append(f"=== {rel}\n(missing)")
        elif path.stat().st_size <= JUDGE_MAX_BYTES:
            parts.append(f"=== {rel}\n{path.read_text(errors='replace')}")
    return "\n\n".join(parts)


def check_judge(check, workdir, env):
    prompt = JUDGE_PROMPT.format(
        question=check["question"], files=judge_files(check, workdir)
    )
    _, events = pi(
        [
            "--model",
            env["EVAL_JUDGE_MODEL"],
            "--thinking",
            "low",
            "--no-tools",
            "--no-skills",
            prompt,
        ],
        workdir,
        env,
    )
    text = reply(events)
    # Take the first JSON object; the judge may add text with braces after it.
    start = text.find("{")
    try:
        verdict = json.JSONDecoder().raw_decode(text, start)[0] if start >= 0 else None
    except json.JSONDecodeError:
        verdict = None
    if not isinstance(verdict, dict) or not isinstance(verdict.get("pass"), bool):
        shown = text if len(text) <= 400 else f"{text[:200]} ... {text[-200:]}"
        return False, f"judge reply is not a verdict: {shown!r}"
    return verdict["pass"], verdict.get("reason", "")


CHECKS = {
    "file_matches": check_file_matches,
    "file_not_matches": check_file_not_matches,
    "file_exists": check_file_exists,
    "command": check_command,
    "judge": check_judge,
}


def run_one(skill, case, arm, n, out, env):
    run_dir = out / case["id"] / f"{arm}-{n}"
    run_dir.mkdir(parents=True)
    result = {
        "case": case["id"],
        "arm": arm,
        "run": n,
        "verdicts": [],
        "usage": None,
        "error": None,
    }
    # The workdir and the agent dir live outside the repo, so pi finds no project config.
    # The agent dir holds only the committed eval settings, so device settings cannot leak in.
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp) / "work"
        agent_dir = Path(tmp) / "agent"
        shutil.copytree(ROOT / "evals" / skill / case["fixture"], workdir)
        shutil.copytree(ROOT / "evals" / "pi-agent", agent_dir)
        run_env = {**env, "PI_CODING_AGENT_DIR": str(agent_dir)}
        tools = TOOLS + (",bash" if case.get("bash") else "")
        # --no-skills drops discovered skills such as ~/.agents/skills; --skill still loads.
        arm_args = ["--no-skills"]
        if arm == "skill":
            arm_args += ["--skill", str(ROOT / "skills" / skill)]
        try:
            stdout, events = pi(
                [
                    "--model",
                    env["EVAL_MODEL"],
                    "--tools",
                    tools,
                    *arm_args,
                    case["prompt"],
                ],
                workdir,
                run_env,
            )
            (run_dir / "events.jsonl").write_text(stdout)
            result["usage"] = usage(events)
            for check in case["checks"]:
                ok, reason = CHECKS[check["type"]](check, workdir, run_env)
                result["verdicts"].append(
                    {"id": check["id"], "pass": ok, "reason": reason}
                )
        except (EvalError, subprocess.TimeoutExpired) as e:
            result["error"] = str(e)
        shutil.copytree(workdir, run_dir / "workdir")
    return result


def summarize(skill, cases, results, env, runs):
    lines = [
        f"# Eval: {skill}",
        "",
        f"- model: `{env['EVAL_MODEL']}`",
        f"- judge: `{env['EVAL_JUDGE_MODEL']}`",
        f"- runs per arm: {runs}",
        "",
    ]
    for case in cases:
        rs = [r for r in results if r["case"] == case["id"]]
        lines += [
            f"## {case['id']}",
            "",
            "| Check | baseline | skill |",
            "| --- | --- | --- |",
        ]
        totals = {arm: [0, 0] for arm in ARMS}
        for check in case["checks"]:
            cells = []
            for arm in ARMS:
                passed = sum(
                    v["pass"]
                    for r in rs
                    if r["arm"] == arm
                    for v in r["verdicts"]
                    if v["id"] == check["id"]
                )
                count = sum(1 for r in rs if r["arm"] == arm)
                totals[arm][0] += passed
                totals[arm][1] += count
                cells.append(f"{passed}/{count}")
            lines.append(f"| {check['id']} | {' | '.join(cells)} |")
        lines.append(
            "| **total** | "
            + " | ".join(f"**{p}/{c}**" for p, c in totals.values())
            + " |"
        )
        for key, label in (("input", "input tokens"), ("output", "output tokens")):
            cells = [
                str(sum((r["usage"] or {}).get(key, 0) for r in rs if r["arm"] == arm))
                for arm in ARMS
            ]
            lines.append(f"| {label} | {' | '.join(cells)} |")
        cells = [
            f"${sum((r['usage'] or {}).get('cost', 0) for r in rs if r['arm'] == arm):.4f}"
            for arm in ARMS
        ]
        lines.append(f"| cost | {' | '.join(cells)} |")
        errors = [r for r in rs if r["error"]]
        if errors:
            lines += ["", "Errors:", ""]
            lines += [f"- {r['arm']}-{r['run']}: {r['error']}" for r in errors]
        lines.append("")
    return "\n".join(lines)


def settings():
    env = dict(os.environ)
    env["PI_BIN"] = env.get("PI_BIN") or "pi-bolt"
    if not env.get("EVAL_MODEL"):
        raise EvalError(
            "EVAL_MODEL is not set. Copy .env.example to .env and fill it in."
        )
    if not env.get("EVAL_JUDGE_MODEL"):
        env["EVAL_JUDGE_MODEL"] = env["EVAL_MODEL"]
    return env


class Progress:
    """Writes one line per run event to stderr and to a log file."""

    def __init__(self, path, total):
        self.path = path
        self.total = total
        self.finished = 0
        self.lock = threading.Lock()

    def log(self, msg):
        line = f"{datetime.now():%H:%M:%S} {msg}"
        with self.lock:
            print(line, file=sys.stderr, flush=True)
            with self.path.open("a") as f:
                f.write(line + "\n")

    def done(self, r, seconds):
        with self.lock:
            self.finished += 1
            n = self.finished
        if r["error"]:
            status = f"error: {r['error']}"
        else:
            passed = sum(v["pass"] for v in r["verdicts"])
            status = f"{passed}/{len(r['verdicts'])} checks"
        name = f"{r['case']} {r['arm']}-{r['run']}"
        self.log(f"[{n}/{self.total}] {name}: {status} ({seconds:.0f}s)")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("skill")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument(
        "--case", action="append", help="run only this case id; repeatable"
    )
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--out", type=Path, default=ROOT / "evals" / "results")
    args = parser.parse_args(argv)
    try:
        env = settings()
        cases = load_cases(args.skill)
        if args.case:
            unknown = set(args.case) - {c["id"] for c in cases}
            if unknown:
                raise EvalError(f"unknown case ids: {', '.join(sorted(unknown))}")
            cases = [c for c in cases if c["id"] in args.case]
    except EvalError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    args.out.mkdir(parents=True, exist_ok=True)
    # mkdtemp adds a random suffix, so two runs in the same second get two directories.
    prefix = f"{datetime.now():%Y%m%d-%H%M%S}-{args.skill}-"
    out = Path(tempfile.mkdtemp(prefix=prefix, dir=args.out))
    jobs = [(c, arm, n) for c in cases for arm in ARMS for n in range(1, args.runs + 1)]
    progress = Progress(out / "progress.log", len(jobs))
    progress.log(f"start: {len(jobs)} runs, {args.jobs} at a time, results in {out}")

    def job(case, arm, n):
        progress.log(f"run   {case['id']} {arm}-{n}")
        start = time.monotonic()
        r = run_one(args.skill, case, arm, n, out, env)
        progress.done(r, time.monotonic() - start)
        return r

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda j: job(*j), jobs))
    (out / "verdicts.json").write_text(json.dumps(results, indent=2))
    summary = summarize(args.skill, cases, results, env, args.runs)
    (out / "summary.md").write_text(summary)
    print(summary)
    print(f"Results: {out}")
    return 1 if any(r["error"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
