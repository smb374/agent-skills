import tempfile
import unittest
from pathlib import Path

from ledger.store import Entry, load


class LoadTest(unittest.TestCase):
    def test_load(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "l.tsv"
            path.write_text("2026-01-02\tBakery\t1250\n")
            self.assertEqual(load(path), [Entry("2026-01-02", "Bakery", 1250)])
