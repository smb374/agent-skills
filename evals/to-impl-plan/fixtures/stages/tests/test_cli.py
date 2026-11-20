import unittest

from ledger.cli import main


class CliTest(unittest.TestCase):
    def test_export_not_implemented(self):
        self.assertEqual(main(["export"]), 1)

    def test_usage(self):
        self.assertEqual(main([]), 2)
