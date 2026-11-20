"""Tests for install.sh. Fake npx, curl, and wget put the download and the vendor calls offline."""

import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
URL = "https://github.com/smb374/agent-skills/archive/refs/heads/main.tar.gz"
# The tools that install.sh and the fake commands call.
TOOLS = (
    "tar",
    "gzip",
    "mktemp",
    "cp",
    "rm",
    "mkdir",
    "grep",
    "basename",
    "cat",
)
ARCHIVE_VENDOR = "c/three w\n"


def vendor_calls(vendor_txt, agent):
    return [
        f"--yes skills add {repo} --global --agent {agent} --skill {skills} --yes"
        for repo, skills in (
            line.split(" ", 1)
            for line in vendor_txt.splitlines()
            if line.strip() and not line.startswith("#")
        )
    ]


class InstallTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.dir = self.tmp / "skills"
        self.scratch = self.tmp / "scratch"
        self.scratch.mkdir()
        self.npx_log = self.tmp / "npx.log"
        self.curl_log = self.tmp / "curl.log"
        self.wget_log = self.tmp / "wget.log"
        self.archive = self.tmp / "main.tar.gz"
        # The vendor list of the tarball differs from the repo's, so a test can tell which one is read.
        (self.tmp / "vendor.txt").write_text(ARCHIVE_VENDOR)
        with tarfile.open(self.archive, "w:gz") as tar:
            for name in ("install.sh", "skills", "fill"):
                tar.add(
                    ROOT / name,
                    arcname=f"agent-skills-main/{name}",
                    filter=lambda i: None if "__pycache__" in i.name else i,
                )
            tar.add(self.tmp / "vendor.txt", arcname="agent-skills-main/vendor.txt")
        # The fakes write the archive to the path after -o (curl) or -O (wget).
        self.bin = self.tmp / "bin"
        self.bin.mkdir()
        self.fake("npx", f'cat >/dev/null\necho "$*" >> "{self.npx_log}"')
        for name, log in (("curl", self.curl_log), ("wget", self.wget_log)):
            self.fake(
                name,
                f'echo "$*" >> "{log}"\n'
                "while [ $# -gt 0 ]; do\n"
                f'    case $1 in -o|-O) cp "{self.archive}" "$2" ;; esac\n'
                "    shift\n"
                "done",
            )
        self.tools = self.tmp / "tools"
        self.tools.mkdir()
        for name in TOOLS:
            (self.tools / name).symlink_to(shutil.which(name))
        self.set_path(self.bin, os.environ["PATH"])

    def fake(self, name, body):
        path = self.bin / name
        path.write_text(f"#!/bin/sh\n{body}\n")
        path.chmod(0o755)

    def set_path(self, *dirs):
        self.env = {
            **os.environ,
            "PATH": ":".join(map(str, dirs)),
            "TMPDIR": str(self.scratch),
        }

    def only_fakes(self, *names):
        """Limit PATH to the fakes in `names` and the plain tools."""
        only = self.tmp / "only"
        only.mkdir()
        for name in names:
            (only / name).symlink_to(self.bin / name)
        self.set_path(only, self.tools)

    def run_install(self, *args):
        return subprocess.run(
            [str(ROOT / "install.sh"), "--dir", str(self.dir), *args],
            check=False,
            env=self.env,
            capture_output=True,
            text=True,
        )

    def assert_copies(self):
        for name in SKILLS:
            self.assertTrue((self.dir / name / "SKILL.md").is_file())
            self.assertFalse((self.dir / name).is_symlink())

    def test_default_downloads_with_curl(self):
        result = self.run_install("--no-vendor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(URL, self.curl_log.read_text())
        self.assert_copies()
        self.assertEqual(list(self.scratch.iterdir()), [])

    def test_wget_fallback_without_curl(self):
        self.only_fakes("wget", "npx")
        result = self.run_install("--no-vendor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(URL, self.wget_log.read_text())
        self.assert_copies()

    def test_no_downloader_fails(self):
        self.only_fakes("npx")
        result = self.run_install("--no-vendor")
        self.assertEqual(result.returncode, 1)
        self.assertIn("curl", result.stderr)
        self.assertIn("wget", result.stderr)

    def test_src_does_not_download(self):
        result = self.run_install("--src", str(ROOT), "--no-vendor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_copies()
        self.assertFalse(self.curl_log.exists())
        self.assertFalse(self.wget_log.exists())

    def test_existing_target_skips(self):
        self.run_install("--src", str(ROOT), "--no-vendor")
        target = self.dir / SKILLS[0]
        (target / "mine.txt").write_text("keep")
        again = self.run_install("--src", str(ROOT), "--no-vendor")
        self.assertEqual(again.returncode, 1)
        self.assertIn(f"skip: {target}", again.stdout)
        self.assertTrue((target / "mine.txt").is_file())

    def test_force_replaces_target(self):
        self.run_install("--src", str(ROOT), "--no-vendor")
        target = self.dir / SKILLS[0]
        (target / "mine.txt").write_text("drop")
        again = self.run_install("--src", str(ROOT), "--no-vendor", "--force")
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertFalse((target / "mine.txt").exists())
        self.assertTrue((target / "SKILL.md").is_file())

    def test_old_flags_fail(self):
        for flag in ("--link", "--copy", "--bogus"):
            with self.subTest(flag=flag):
                result = self.run_install(flag)
                self.assertEqual(result.returncode, 2)
                self.assertIn("usage:", result.stderr)

    def test_vendor_calls_npx_per_line(self):
        result = self.run_install("--src", str(ROOT), "--agent", "opencode")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.npx_log.read_text().splitlines(),
            vendor_calls((ROOT / "vendor.txt").read_text(), "opencode"),
        )

    def test_vendor_reads_list_of_source_tree(self):
        tree = self.tmp / "tree"
        (tree / "skills" / "demo").mkdir(parents=True)
        (tree / "vendor.txt").write_text("# comment\na/one x\n\nb/two y z\n")
        result = self.run_install("--src", str(tree))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.npx_log.read_text().splitlines(),
            [
                "--yes skills add a/one --global --agent pi --skill x --yes",
                "--yes skills add b/two --global --agent pi --skill y z --yes",
            ],
        )

    def test_force_keeps_vendor_calls(self):
        self.run_install("--src", str(ROOT))
        plain = self.npx_log.read_text()
        self.npx_log.unlink()
        self.run_install("--src", str(ROOT), "--force")
        self.assertEqual(self.npx_log.read_text(), plain)

    def test_vendor_from_download(self):
        result = self.run_install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.npx_log.read_text().splitlines(),
            vendor_calls(ARCHIVE_VENDOR, "pi"),
        )

    def test_no_vendor_skips_npx(self):
        self.run_install("--src", str(ROOT), "--no-vendor")
        self.assertFalse(self.npx_log.exists())

    def fill_tree(self):
        """A source tree with the listed skill `handoff`, one unlisted skill, and fill."""
        tree = self.tmp / "tree"
        for name in ("handoff", "other"):
            (tree / "skills" / name).mkdir(parents=True)
            (tree / "skills" / name / "SKILL.md").write_text(name)
        (tree / "fill").mkdir()
        (tree / "fill" / "fill.py").write_text("# fill\n")
        return tree

    def test_listed_skill_gets_fill(self):
        result = self.run_install("--src", str(self.fill_tree()), "--no-vendor")
        self.assertEqual(result.returncode, 0, result.stderr)
        fill = self.dir / "handoff" / "scripts" / "fill.py"
        self.assertEqual(fill.read_text(), "# fill\n")
        self.assertFalse((self.dir / "other" / "scripts").exists())

    def test_skipped_skill_gets_no_fill(self):
        (self.dir / "handoff").mkdir(parents=True)
        result = self.run_install("--src", str(self.fill_tree()), "--no-vendor")
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"skip: {self.dir / 'handoff'}", result.stdout)
        self.assertFalse((self.dir / "handoff" / "scripts").exists())


class DocsTest(unittest.TestCase):
    def test_docs_install_commands_pass_src(self):
        # A bare ./install.sh installs the downloaded main, not the clone.
        for doc in ("README.md", "CONTRIBUTING.md"):
            lines = (ROOT / doc).read_text().splitlines()
            for number, line in enumerate(lines, 1):
                for command in re.findall(r"\./install\.sh[^`\n]*", line):
                    self.assertIn("--src", command, f"{doc}:{number}: {line}")


if __name__ == "__main__":
    unittest.main()
