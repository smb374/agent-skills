import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from ledger.cli import main


class CliTest(unittest.TestCase):
    def test_usage(self):
        self.assertEqual(main([]), 2)

    def test_total(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "l.tsv"
            path.write_text("2026-01-02\tBakery\t1250\n2026-01-03\tCafe\t300\n")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main(["total", str(path)])
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue(), "total: 15.50\n")
