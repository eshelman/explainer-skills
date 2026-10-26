#!/usr/bin/env python3
"""Focused integrity, declaration and lexical-gate tests; no model judgments."""

import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
import check_words as gate


def fixture_core():
    words = set(('a am an and are at away be can cell cells core define defined definition '
                 'do does dog dogs energy far first for force form from has have here i in is it '
                 'its light mass measured meaning means more move moves named need not number of '
                 'on ordinary out part point read reason said see small so sound speed term that '
                 'the their them there these they this three to up use used value water we were '
                 'what when where will with word words work works you your').split())
    records = tuple(dict(lemma=w, forms=(w,), pos='n', known_fraction='', zipf_frequency='',
                         selection_reason='test fixture') for w in sorted(words))
    return gate.CoreVocabulary(records, frozenset(words), {word: (word,) for word in words}, 'fixture')


def term_manifest(**updates):
    entry = dict(term='quark', forms=['quark', 'quarks'], definition='a small part', reason='needed to name this part')
    entry.update(updates)
    return {'terms': [entry]}


class ScienceGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = fixture_core()

    def check(self, text, **kwargs):
        return gate.check_text(text, core=self.core, **kwargs)

    def test_default_research_and_strict_modes(self):
        for mode in ('research', 'undergraduate-strict'):
            result = self.check('Water moves.', mode=mode)
            self.assertTrue(result['ok'], result)
            self.assertEqual(result['mode'], mode)
            self.assertEqual(result['vocabulary_lemmas'], len(self.core.records))
        self.assertEqual(self.check('Water moves.')['mode'], 'research')

    def test_unlisted_words_and_locations(self):
        result = self.check('# Water\nQuark energy.')
        self.assertFalse(result['ok'])
        self.assertEqual(result['unlisted_words'], {'quark': 1})
        self.assertEqual((result['issues'][0]['line'], result['issues'][0]['column']), (2, 1))

    def test_inflections_are_explicit_and_standard_contractions_are_bounded(self):
        self.assertTrue(self.check("The dog's cells don't move. We're here.")['ok'])
        for text in ("Cellular water.", "The'quark.", "Water're here.", "I're here.", "Isn'tquark."):
            self.assertFalse(self.check(text)['ok'], text)

    def test_undeclared_term_is_not_implicitly_authorized_by_a_definition(self):
        self.assertFalse(self.check('A quark is a small part.')['ok'])

    def test_explicit_term_and_exact_core_definition_are_accepted(self):
        result = self.check('A **QUARK** is a small\n part. Quarks move.', terms=term_manifest())
        self.assertTrue(result['ok'], result)
        usage = result['declared_term_usage'][0]
        self.assertEqual(usage['occurrences'], 2)
        self.assertTrue(usage['definition_near_first_use'])
        self.assertTrue(self.check('A quark is **a *small* part**.', terms=term_manifest())['ok'])

    def test_multiword_permission_does_not_authorize_components_elsewhere(self):
        manifest = term_manifest(term='quantum foam', forms=['quantum foam'])
        self.assertTrue(self.check('Quantum foam is a small part.', terms=manifest)['ok'])
        self.assertIn('quantum', self.check('Quantum foam is a small part. Quantum moves.', terms=manifest)['unlisted_words'])

    def test_canonical_term_definition_and_local_first_use_are_required(self):
        cases = [
            ('A quark moves.', 'term_definition_missing'),
            ('A small part moves.', 'declared_term_missing'),
            ('Quarks are a small part.', 'declared_term_missing'),
            ('A quark moves. ' + 'Water moves. ' * 30 + 'A small part.', 'term_definition_not_near_first_use'),
            # A later nearby definition does not repair an unexplained first use.
            ('A quark moves. ' + 'Water moves. ' * 30 + 'A quark is a small part.', 'term_definition_not_near_first_use'),
        ]
        for text, kind in cases:
            result = self.check(text, terms=term_manifest())
            self.assertIn(kind, [issue['kind'] for issue in result['issues']], result)
        self.assertTrue(self.check('A small part is named quark.', terms=term_manifest())['ok'])

    def test_missing_empty_malformed_and_malicious_manifests_are_rejected(self):
        bad = [None, [], {}, {'terms': 'quark'}, {'terms': [{}]},
               term_manifest(forms=[]), term_manifest(forms=['quarks']),
               term_manifest(forms=['quark', 'QUARK']), term_manifest(forms=['quark', '**anything**']),
               term_manifest(definition='small part'), term_manifest(definition='1e3 2e4 3e5'),
               term_manifest(definition='a quantum part'),
               term_manifest(definition='a small part https://bad.test/'),
               term_manifest(definition='a small part citeturn0search0'),
               term_manifest(reason=''), term_manifest(term=''),
               {'terms': [dict(term_manifest()['terms'][0], unchecked='quarks')]}]
        for payload in bad:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                gate.validate_terms(payload, self.core)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(OSError):
                gate.load_terms(Path(tmp) / 'missing.json', self.core)
            path = Path(tmp) / 'bad.json'
            path.write_text('{"terms": [], "terms": []}')
            with self.assertRaises(ValueError):
                gate.load_terms(path, self.core)

    def test_typed_declarations_are_revalidated(self):
        forged = gate.Term('quark', ('quark',), 'a quantum part', 'needed')
        with self.assertRaises(ValueError):
            self.check('A quark is a quantum part.', terms=[forged])

    def test_strict_and_classic_reject_terms_even_an_empty_manifest(self):
        for mode in ('undergraduate-strict', 'classic'):
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.check('Water moves.', mode=mode, terms={'terms': []})

    def test_labels_and_image_alt_are_checked_hidden_urls_are_not(self):
        url = 'https://example.test/unlisted_123?quantum=1'
        self.assertTrue(self.check(f'[Read more here]({url})')['ok'])
        for text in (f'[Quark]({url})', f'![Quark]({url})'):
            self.assertIn('quark', self.check(text)['unlisted_words'])
        self.assertFalse(self.check(f'`[Read]({url})`')['ok'])
        self.assertFalse(self.check(f'```\n[Read]({url})\n```')['ok'])

    def test_only_exact_citation_metadata_shapes_are_opaque(self):
        tokens = ['citeturn0search0', 'citeturn0search0turn1view2',
                  'genui{"citation":{"ref":"turn0search0"}}',
                  'genui{"citation":{"refs":["turn0search0","turn1view2"]}}']
        for token in tokens:
            self.assertTrue(self.check('Water moves. ' + token)['ok'], token)
            self.assertFalse(self.check('`' + token + '`')['ok'], token)
        for token in ['citeunlisted prose', 'genui{"citation":{"ref":"quark"}}',
                      'genui{"citation":{"refs":[]}}',
                      'genui{"citation":{"ref":"turn0search0"},"text":"quark"}',
                      'genui{"citation":{"ref":"turn0search0","ref":"turn1view0"}}',
                      'citeturn0search0']:
            self.assertFalse(self.check('Water moves. ' + token)['ok'], token)

    def test_numeric_literals_and_math_operators(self):
        self.assertTrue(self.check('Water moves 12 + 2.5 - .25 = 1.2e-3 × 6.02E23.')['ok'])
        for text in ('H2O', '12quark', '1.2.3', 'water₂', '12 kg'):
            self.assertFalse(self.check(text)['ok'], text)

    def test_symbols_need_explicit_core_meanings_and_actual_usage(self):
        payload = {'symbols': [{'symbol': 'x', 'meaning': 'a measured value'}]}
        self.assertTrue(self.check('x is a measured value.', symbols=payload)['ok'])
        self.assertTrue(self.check('x is a measured value.', mode='undergraduate-strict', symbols=payload)['ok'])
        self.assertFalse(self.check('x moves.')['ok'])
        self.assertIn('symbol_meaning_missing', [i['kind'] for i in self.check('x moves.', symbols=payload)['issues']])
        self.assertIn('declared_symbol_missing', [i['kind'] for i in self.check('A measured value.', symbols=payload)['issues']])
        with self.assertRaises(ValueError):
            self.check('x is a quantum value.', symbols={'symbols': [{'symbol': 'x', 'meaning': 'a quantum value'}]})
        for symbol in ('а', '我', '𝚡'):
            with self.subTest(symbol=symbol), self.assertRaises(ValueError):
                self.check(symbol + ' is a measured value.', symbols={'symbols': [{'symbol': symbol, 'meaning': 'a measured value'}]})
        self.assertTrue(self.check('A value.')['semantic_review_notes'])

    def test_greek_and_tex_are_checked_without_a_math_escape_hatch(self):
        symbols = {'symbols': [{'symbol': '\\alpha', 'meaning': 'a measured value'}]}
        good = r'$\frac{\alpha}{2.5e-3}$ is a measured value.'
        self.assertTrue(self.check(good, symbols=symbols)['ok'])
        self.assertTrue(self.check('α is a measured value.', symbols=symbols)['ok'])
        self.assertFalse(self.check(r'$\alpha + 2$')['ok'])
        for text in (r'$\text{quark}$', r'$\mathrm{quark}$', r'$\quark{water}$',
                     '`quark`', '```\nquark\n```', r'\begin{quark} water \end{quark}'):
            self.assertFalse(self.check(text)['ok'], text)
        self.assertTrue(self.check(r'$\text{water} + 2$')['ok'])

    def test_unicode_and_markup_cannot_hide_words(self):
        for text in ('wаter', 'water\u200b', '🧠', '𝚝𝚑𝚎', '# Quark', '| Water | Quark |'):
            self.assertFalse(self.check(text)['ok'], text)

    def test_empty_input_fails(self):
        for text in ('', ' ', '---', '[](https://example.test/quark)', 'citeturn0search0'):
            self.assertFalse(self.check(text)['ok'], text)

    def test_lookup_is_exact_and_reports_lemma_membership(self):
        result = gate.lookup_words(['Water', "dog's", 'quark'], 'research', self.core, self.core.forms)
        self.assertEqual(result['lookup'][0]['lemmas'], ['water'])
        self.assertFalse(result['lookup'][1]['exact_form'])
        self.assertTrue(result['lookup'][1]['contraction_or_possessive_allowed'])
        self.assertFalse(result['lookup'][2]['exact_form'])


class ClassicGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries, cls.allowed = gate.load_words()

    def check(self, text):
        return gate.check_text(text, self.allowed)

    def test_every_official_spelling_is_accepted(self):
        result = self.check('\n'.join(self.entries))
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['word_count'], 3634)
        self.assertEqual(result['mode'], 'classic')

    def test_legacy_acceptance_and_rejections_remain(self):
        self.assertTrue(self.check("I don't think the up-goer will work.")['ok'])
        self.assertTrue(self.check('I DON’T think the up–goer will work.')['ok'])
        for text in ('Quantum physics.', "dog's", "we're", '1000', 'H2O', 'the + water', '`water`'):
            self.assertFalse(self.check(text)['ok'], text)
        self.assertEqual(self.check('Energy\nQuantum physics.')['unlisted_words'], {'energy': 1, 'physics': 1, 'quantum': 1})

    def test_classic_cli_status_and_lookup(self):
        script = str(Path(gate.__file__))
        for text, status in [('Water moves.', 0), ('Quantum water.', 1)]:
            result = subprocess.run([sys.executable, script, '--mode', 'classic', '--json'],
                                    input=text, text=True, capture_output=True)
            self.assertEqual(result.returncode, status, result.stdout + result.stderr)
        result = subprocess.run([sys.executable, script, '--mode', 'classic', '--lookup', 'water', 'quantum', '--json'],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(json.loads(result.stdout)['lookup']), 2)
        result = subprocess.run([sys.executable, script, '--mode', 'classic', '/missing-draft.txt'],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)


class CoreIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.path = Path(cls.temp.name) / 'core.tsv'
        cls.manifest_path = Path(cls.temp.name) / 'manifest.json'
        def suffix(index):
            letters = []
            for _ in range(4):
                letters.append(chr(97 + index % 26))
                index //= 26
            return ''.join(letters)
        cls.rows = [dict(lemma='core' + suffix(i), pos='n,v', forms='core' + suffix(i),
                         known_fraction='0.95', zipf_frequency='3.2', selection_reason='fixture')
                    for i in range(gate.EXPECTED_LEMMAS)]
        cls.rows[0]['forms'] += '|shared'
        cls.rows[1]['forms'] += '|shared'

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def write_core(self, rows=None, **manifest_updates):
        rows = rows if rows is not None else self.rows
        stream = io.StringIO(newline='')
        writer = csv.DictWriter(stream, fieldnames=gate.CORE_COLUMNS, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
        data = stream.getvalue().encode()
        self.path.write_bytes(data)
        manifest = dict(schema_version=1, lemma_count=15000,
                        surface_form_count=len({form for row in rows for form in row['forms'].split('|')}),
                        core_sha256=hashlib.sha256(data).hexdigest())
        manifest.update(manifest_updates)
        self.manifest_path.write_text(json.dumps(manifest))

    def test_all_records_and_shared_form_membership(self):
        self.write_core()
        core = gate.load_core(self.path, self.manifest_path)
        self.assertEqual(core.lemma_count, 15000)
        self.assertEqual(len(core.forms), 15001)
        self.assertEqual(len(core.memberships['shared']), 2)
        for record in core.records:
            self.assertIn(record['lemma'], record['forms'])
            self.assertTrue(all(record['forms']))

    def test_checksum_and_all_manifest_counts_are_enforced(self):
        self.write_core(core_sha256='0' * 64)
        with self.assertRaisesRegex(ValueError, 'checksum'):
            gate.load_core(self.path, self.manifest_path)
        self.write_core(surface_form_count=15000)
        with self.assertRaisesRegex(ValueError, 'surface-form count'):
            gate.load_core(self.path, self.manifest_path)
        self.write_core(lemma_count=14999)
        with self.assertRaisesRegex(ValueError, 'exactly 15000'):
            gate.load_core(self.path, self.manifest_path)
        self.write_core(rows=self.rows[:-1])
        with self.assertRaisesRegex(ValueError, 'exactly 15000'):
            gate.load_core(self.path, self.manifest_path)

    def test_every_lemma_requires_nonempty_unique_explicit_forms(self):
        for change in ({'forms': ''}, {'forms': 'shared'}, {'forms': self.rows[0]['forms'] + '|'},
                       {'forms': self.rows[0]['forms'] + '|shared'}, {'lemma': self.rows[1]['lemma']}):
            rows = [dict(self.rows[0], **change)] + self.rows[1:]
            self.write_core(rows=rows)
            with self.subTest(change=change), self.assertRaises(ValueError):
                gate.load_core(self.path, self.manifest_path)

    def test_bundled_core_all_records_and_default_cli_if_available(self):
        if not gate.CORE_FILE.exists() or not gate.CORE_MANIFEST.exists():
            self.skipTest('Bundled core data not yet generated; synthetic 15,000-record integrity fixture tested.')
        core = gate.load_core()
        self.assertEqual(len({record['lemma'] for record in core.records}), 15000)
        for record in core.records:
            self.assertIn(record['lemma'], record['forms'])
            self.assertTrue(all(record['forms']))
        result = subprocess.run([sys.executable, str(Path(gate.__file__)), '--json'],
                                input='Water moves.', text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['mode'], 'research')


if __name__ == '__main__':
    unittest.main()
