import unittest

from ledger.money import format_cents


class FormatCentsTest(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(format_cents(1250), "12.50")

    def test_negative(self):
        self.assertEqual(format_cents(-150), "-1.50")
