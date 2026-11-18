"""Tests for install.sh. A fake npx records the vendor calls."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())


class InstallTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.dir = self.tmp / "skills"
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        self.npx_log = self.tmp / "npx.log"
        npx = bin_dir / "npx"
        # The fake reads stdin, like a real npx can.
        npx.write_text(f'#!/bin/sh\ncat >/dev/null\necho "$*" >> "{self.npx_log}"\n')
        npx.chmod(0o755)
        self.env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}"}

    def run_install(self, *args):
        return subprocess.run(
            [str(ROOT / "install.sh"), "--dir", str(self.dir), *args],
            check=False,
            env=self.env,
            capture_output=True,
            text=True,
        )

    def test_link_is_idempotent(self):
        self.assertEqual(self.run_install("--no-vendor").returncode, 0)
        for name in SKILLS:
            target = self.dir / name
            self.assertEqual(os.readlink(target), str(ROOT / "skills" / name))
        again = self.run_install("--no-vendor")
        self.assertEqual(again.returncode, 0)
        self.assertIn("linked:", again.stdout)

    def test_copy_skips_existing(self):
        self.assertEqual(self.run_install("--copy", "--no-vendor").returncode, 0)
        for name in SKILLS:
            self.assertTrue((self.dir / name / "SKILL.md").is_file())
            self.assertFalse((self.dir / name).is_symlink())
        again = self.run_install("--copy", "--no-vendor")
        self.assertEqual(again.returncode, 1)
        self.assertIn("skip:", again.stdout)

    def test_link_skips_copy(self):
        self.run_install("--copy", "--no-vendor")
        result = self.run_install("--no-vendor")
        self.assertEqual(result.returncode, 1)
        self.assertFalse((self.dir / SKILLS[0]).is_symlink())

    def test_vendor_calls_npx_per_line(self):
        result = self.run_install("--agent", "opencode")
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = [
            f"--yes skills add {repo} --global --agent opencode --skill {skills} --yes"
            for repo, skills in (
                line.split(" ", 1)
                for line in (ROOT / "vendor.txt").read_text().splitlines()
                if line.strip() and not line.startswith("#")
            )
        ]
        self.assertEqual(self.npx_log.read_text().splitlines(), expected)

    def test_vendor_npx_does_not_eat_lines(self):
        repo = self.tmp / "repo"
        (repo / "skills" / "demo").mkdir(parents=True)
        shutil.copy(ROOT / "install.sh", repo)
        (repo / "vendor.txt").write_text("# comment\na/one x\n\nb/two y z\n")
        result = subprocess.run(
            [str(repo / "install.sh"), "--dir", str(self.dir)],
            check=False,
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.npx_log.read_text().splitlines(),
            [
                "--yes skills add a/one --global --agent pi --skill x --yes",
                "--yes skills add b/two --global --agent pi --skill y z --yes",
            ],
        )

    def test_no_vendor_skips_npx(self):
        self.run_install("--no-vendor")
        self.assertFalse(self.npx_log.exists())

    def test_unknown_flag_fails(self):
        self.assertEqual(self.run_install("--bogus").returncode, 2)


if __name__ == "__main__":
    unittest.main()
