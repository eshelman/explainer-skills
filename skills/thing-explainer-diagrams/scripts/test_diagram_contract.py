#!/usr/bin/env python3
"""Exercise diagram reading surfaces against the real bundled v2 CLI."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TERM = {"terms": [{"term": "stochastic", "forms": ["stochastic"],
                   "definition": "having outcomes that include random variation",
                   "reason": "Distinguishes random outcomes from a fixed outcome."}]}
LABELS = "Stochastic: having outcomes that include random variation.\nInput\nPossible outcomes"
PROSE = ("# Different outcomes\n\nA stochastic process has outcomes that can differ.\n\n"
         "Stochastic means having outcomes that include random variation. "
         "The arrows show possible outcomes, not a fixed result.\n\n"
         "Repeated inputs can therefore produce different results.")


class DiagramSurfaces(unittest.TestCase):
    def run_gate(self, text, mode=None, terms=None, symbols=None):
        with tempfile.TemporaryDirectory() as directory:
            args = [sys.executable, str(ROOT / "scripts/check_words.py"), "--json"]
            if mode:
                args += ["--mode", mode]
            for flag, data in (("terms", terms), ("symbols", symbols)):
                if data is not None:
                    path = Path(directory) / (flag + ".json")
                    path.write_text(json.dumps(data), encoding="utf-8")
                    args += ["--" + flag, str(path)]
            run = subprocess.run(args, input=text, text=True, capture_output=True)
            return run.returncode, json.loads(run.stdout)

    def test_default_accepts_research_terms_on_both_surfaces(self):
        for text in (LABELS, PROSE):
            code, result = self.run_gate(text, terms=TERM)
            self.assertEqual(code, 0, result)
            self.assertEqual(result["mode"], "research")
            self.assertEqual(result["vocabulary_lemmas"], 15000)

    def test_prose_definition_cannot_rescue_image_label(self):
        self.assertEqual(self.run_gate(PROSE, terms=TERM)[0], 0)
        code, result = self.run_gate("Stochastic\nInput\nPossible outcomes", terms=TERM)
        self.assertEqual(code, 1)
        self.assertIn("term_definition_missing", [i["kind"] for i in result["issues"]])

    def test_rendered_typo_or_lost_definition_is_rejected(self):
        for altered in (LABELS.replace("Stochastic:", "Stochastik:"),
                        LABELS.replace("random variation", "variation")):
            self.assertNotEqual(self.run_gate(altered, terms=TERM)[0], 0)

    def test_core_only_labels_allow_technical_prose_separately(self):
        self.assertEqual(self.run_gate("Input\nRandom variation\nPossible outcomes")[0], 0)
        self.assertEqual(self.run_gate(PROSE, terms=TERM)[0], 0)

    def test_strict_rejects_term_exceptions(self):
        self.assertEqual(self.run_gate(LABELS, mode="undergraduate-strict", terms=TERM)[0], 2)
        self.assertEqual(self.run_gate("Input\nRandom variation", mode="undergraduate-strict")[0], 0)

    def test_symbol_meaning_must_exist_on_image(self):
        symbols = {"symbols": [{"symbol": "x", "meaning": "the measured value"}]}
        self.assertEqual(self.run_gate("x = 2\nx: the measured value", symbols=symbols)[0], 0)
        code, result = self.run_gate("x = 2", symbols=symbols)
        self.assertEqual(code, 1)
        self.assertIn("symbol_meaning_missing", [i["kind"] for i in result["issues"]])

    def test_classic_remains_explicit_and_restricted(self):
        text = "More hands can help. People can block each other."
        self.assertEqual(self.run_gate(text, mode="classic")[0], 0)
        self.assertNotEqual(self.run_gate("2 hands", mode="classic")[0], 0)
        self.assertEqual(self.run_gate(text, mode="classic", terms=TERM)[0], 2)


if __name__ == "__main__":
    unittest.main()
