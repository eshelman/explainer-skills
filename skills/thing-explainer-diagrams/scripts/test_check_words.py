#!/usr/bin/env python3
"""Behavioral checks for the fixed vocabulary and the user-facing text gate."""

import sys
sys.dont_write_bytecode = True
import subprocess
import unittest
from pathlib import Path

from check_words import check_text, load_words


class WordGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries, cls.allowed = load_words()

    def check(self, text):
        return check_text(text, self.allowed)

    def test_every_official_spelling_is_accepted(self):
        result = self.check("\n".join(self.entries))
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["word_count"], 3634)

    def test_case_contractions_and_hyphenated_phrases(self):
        self.assertEqual(self.check("I CAN’T explain a thousand things.")["unlisted_words"], {"thousand": 1})
        self.assertTrue(self.check("I don't think the up-goer will work.")["ok"])
        self.assertTrue(self.check("I DON’T think the up–goer will work.")["ok"])

    def test_technical_words_are_flagged_with_locations(self):
        r = self.check("# Energy\nQuantum physics is hard.\nPhysics is hard.")
        self.assertEqual(r["unlisted_words"], {"energy": 1, "physics": 2, "quantum": 1})
        self.assertEqual((r["issues"][0]["line"], r["issues"][0]["column"]), (1, 3))

    def test_apostrophes_do_not_bypass_validation(self):
        for text in ["the'quantum", "'quantum", "dog's", "isn'tquantum", "we're"]:
            with self.subTest(text=text):
                self.assertFalse(self.check(text)["ok"])

    def test_only_link_destination_is_exempt(self):
        self.assertTrue(self.check("[Read more here](https://example.org/Quantum_123?a=2#energy)")["ok"])
        self.assertIn("quantum", self.check("[Quantum](https://example.org/a)")["unlisted_words"])
        self.assertIn("quantum", self.check("![Quantum](https://example.org/a)")["unlisted_words"])
        self.assertFalse(self.check('[Read here](https://example.org/a "Quantum")')["ok"])
        self.assertFalse(self.check("https://example.org/quantum")["ok"])
        # A URL inside code is visible, so it cannot receive a link exemption.
        self.assertFalse(self.check("`[Read](https://example.org/quantum)`")["ok"])

    def test_digits_symbols_and_unicode_do_not_evade_gate(self):
        for text in ["1000", "H2O", "AI", "energy₂", "café", "wаter", "water\u200b", "🧠", "𝚝𝚑𝚎", "the + water"]:
            with self.subTest(text=text):
                self.assertFalse(self.check(text)["ok"])

    def test_headings_tables_and_closing_are_checked(self):
        good = "# How it works\n\n| Part | What it does |\n|---|---|\n| Water | It moves. |\n\n**Think about that.**"
        self.assertTrue(self.check(good)["ok"])
        self.assertFalse(self.check(good + "\nSummary.")["ok"])

    def test_empty_input_fails(self):
        for text in ["", "   ", "---", "[](https://example.org/quantum)"]:
            with self.subTest(text=text):
                self.assertFalse(self.check(text)["ok"])

    def test_cli_exit_statuses(self):
        script = str(Path(__file__).with_name("check_words.py"))
        for text, status in [("Water moves.", 0), ("Quantum water.", 1)]:
            process = subprocess.run([sys.executable, script, "--json"], input=text,
                                     capture_output=True, text=True)
            self.assertEqual(process.returncode, status, process.stdout + process.stderr)
        process = subprocess.run([sys.executable, script, str(Path(__file__).with_name("missing-draft.txt"))],
                                 capture_output=True, text=True)
        self.assertEqual(process.returncode, 2)


if __name__ == "__main__":
    unittest.main()
