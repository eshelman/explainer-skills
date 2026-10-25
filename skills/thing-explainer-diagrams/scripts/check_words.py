#!/usr/bin/env python3
"""Deterministic Thing Explainer v2 vocabulary gate (Python standard library).

Default research mode admits the checksum-verified 15,000-lemma core and only
explicit, used, locally defined topic terms. Undergraduate-strict admits the
core without topic terms. Classic retains the fixed official spelling list.

A declared term's canonical spelling and exact definition must both occur in
visible output, ignoring case, whitespace and paired Markdown emphasis. The
complete definition must start within 250 normalized visible characters after
its first accepted term-form occurrence, or finish within 250 characters before
that occurrence. Symbols require their exact core-only meaning somewhere in the
visible output. Declarations establish lexical permission, not scientific truth.

Exit 0: pass; 1: draft fails; 2: input/manifest/vocabulary-integrity failure.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
import hashlib
import io
import json
import math
from pathlib import Path
import re
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
WORDLIST = ROOT / "references" / "words.txt"
CORE_FILE = ROOT / "references" / "core-15000.tsv"
CORE_MANIFEST = ROOT / "references" / "core-manifest.json"
EXPECTED_SHA256 = "fa78b7ef472d9b6ba5c0e9f7e8919e8e825d9b5c307baac28e5d4e0a1cebf5c7"
EXPECTED_ENTRIES = 3634
EXPECTED_NORMALIZED = 3616
EXPECTED_LEMMAS = 15000
CORE_COLUMNS = ["lemma", "pos", "forms", "known_fraction", "zipf_frequency", "selection_reason"]
MODES = ("research", "undergraduate-strict", "classic")
DEFINITION_DISTANCE = 250
WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)
NUMBER = re.compile(r"(?<![\w.])(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?(?!\w|\.[0-9])")
LINK = re.compile(r"!?\[[^\]\n]*\]\((https?://[^\s()<>]+)\)")
CODE = re.compile(r"```[\s\S]*?(?:```|$)|~~~[\s\S]*?(?:~~~|$)|(?<!`)`(?!`)[^`]*(?:`|$)")
PUNCTUATION = frozenset(".,;:!?-'’‘\"“”()[]{}*/_#>|~–—…")
SCIENCE_PUNCTUATION = PUNCTUATION | frozenset("`$^=+<>≤≥≠≈≡±∓−×÷∑∏∫√∞∂∇∈∉⊂⊆⊃⊇∩∪∧∨¬→←↔⇒⇔∝")
CITATION = re.compile(r"[^]*")
CITATION_REF = re.compile(r"turn[0-9]+[A-Za-z]+[0-9]+\Z")
EMPHASIS = re.compile(r"(?<!\w)(\*\*|__|\*|_)(?=\S)(.+?)(?<=\S)\1(?!\w)", re.DOTALL)
TEX_COMMAND = re.compile(r"\\([A-Za-z]+)")
# Syntax and mathematical operators only. Their brace contents are always checked.
TEX_SYNTAX = frozenset(("frac sqrt text textrm textbf textit mathrm mathbf mathit "
                        "operatorname left right cdot times div pm mp le leq ge geq ne neq "
                        "approx equiv to rightarrow leftarrow leftrightarrow in notin "
                        "partial nabla sum prod int limits infty ldots dots quad qquad").split())
# Function names carry meaning and are still checked as ordinary words.
TEX_FUNCTIONS = frozenset("sin cos tan log ln exp min max det lim".split())
GREEK = dict(zip("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega".split(),
                 "αβγδεζηθικλμνξοπρστυφχψω"))
GREEK.update({"Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ", "Pi": "Π", "Sigma": "Σ", "Upsilon": "Υ", "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω"})
CONTRACTIONS = {
    "can't": ("can", "not"), "cannot": ("can", "not"), "won't": ("will", "not"),
    "shan't": ("shall", "not"), "let's": ("let", "us"),
}
for _base in "is are was were do does did have has had could should would must need might ought".split():
    CONTRACTIONS[_base + "n't"] = (_base, "not")
for _base in "you we they who".split():
    CONTRACTIONS[_base + "'re"] = (_base, "are")
for _base in "i you we they could should would might must".split():
    CONTRACTIONS[_base + "'ve"] = (_base, "have")
for _base in "i you he she it we they who what there".split():
    CONTRACTIONS[_base + "'ll"] = (_base, "will")
    CONTRACTIONS[_base + "'d"] = (_base, "would")
CONTRACTIONS["i'm"] = ("i", "am")


@dataclass(frozen=True)
class CoreVocabulary:
    records: tuple[dict, ...]
    forms: frozenset[str]
    memberships: dict[str, tuple[str, ...]]
    sha256: str = ""

    @property
    def lemma_count(self) -> int:
        return len(self.records)


@dataclass(frozen=True)
class Term:
    term: str
    forms: tuple[str, ...]
    definition: str
    reason: str


@dataclass(frozen=True)
class Symbol:
    symbol: str
    meaning: str


def normalize(word: str) -> str:
    return word.replace("’", "'").lower()


def _phrase(text: str) -> str:
    return " ".join(normalize(text).split())


def _unique_json(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key!r}.")
        result[key] = value
    return result


def read_json(path: Path | str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_json)


def load_words() -> tuple[list[str], frozenset[str]]:
    """The legacy public API: verify and load the classic spelling list."""
    data = WORDLIST.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise ValueError("Bundled classic vocabulary checksum mismatch; restore the original list.")
    entries = data.decode("utf-8").splitlines()
    allowed = frozenset(normalize(word) for word in entries)
    if (len(entries) != EXPECTED_ENTRIES or len(set(entries)) != EXPECTED_ENTRIES
            or len(allowed) != EXPECTED_NORMALIZED):
        raise ValueError("Bundled classic vocabulary count mismatch.")
    return entries, allowed


def load_core(path: Path | str | None = None, manifest_path: Path | str | None = None) -> CoreVocabulary:
    """Load the immutable core, verifying bytes, schema, counts and every form."""
    path = Path(path) if path is not None else CORE_FILE
    manifest_path = Path(manifest_path) if manifest_path is not None else CORE_MANIFEST
    data = path.read_bytes()
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1:
        raise ValueError("Core manifest must have schema_version 1.")
    if type(manifest.get("lemma_count")) is not int or manifest["lemma_count"] != EXPECTED_LEMMAS:
        raise ValueError(f"Core manifest must authorize exactly {EXPECTED_LEMMAS} lemmas.")
    digest = hashlib.sha256(data).hexdigest()
    if manifest.get("core_sha256") != digest:
        raise ValueError("Bundled core checksum mismatch; restore the authorized core.")
    reader = csv.DictReader(io.StringIO(data.decode("utf-8")), delimiter="\t")
    if reader.fieldnames != CORE_COLUMNS:
        raise ValueError("Core TSV header does not match the required schema.")
    records, lemmas, memberships = [], set(), defaultdict(list)
    for line, row in enumerate(reader, 2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"Malformed core TSV record on line {line}.")
        lemma = row["lemma"]
        if not lemma or lemma != _phrase(lemma) or lemma in lemmas:
            raise ValueError(f"Empty, non-normalized or duplicate core lemma on line {line}.")
        forms = row["forms"].split("|")
        if any(not form or form != _phrase(form) for form in forms) or len(set(forms)) != len(forms):
            raise ValueError(f"Empty, non-normalized or duplicate core form on line {line}.")
        if lemma not in forms:
            raise ValueError(f"Core lemma {lemma!r} is missing from its explicit forms.")
        if any(not WORD.search(form) or any(ord(c) < 32 for c in form) for form in forms):
            raise ValueError(f"Invalid core form on line {line}.")
        for field in ("known_fraction", "zipf_frequency"):
            if row[field]:
                try:
                    value = float(row[field])
                except ValueError as exc:
                    raise ValueError(f"Invalid {field} on core line {line}.") from exc
                if not math.isfinite(value) or (field == "known_fraction" and not 0 <= value <= 1):
                    raise ValueError(f"Invalid {field} on core line {line}.")
        lemmas.add(lemma)
        records.append(dict(row, forms=tuple(forms)))
        for form in forms:
            memberships[form].append(lemma)
    if len(records) != EXPECTED_LEMMAS or len(lemmas) != EXPECTED_LEMMAS:
        raise ValueError(f"Core must contain exactly {EXPECTED_LEMMAS} unique lemmas; found {len(lemmas)}.")
    count = manifest.get("surface_form_count")
    if type(count) is not int or count != len(memberships):
        raise ValueError("Core unique surface-form count does not match its manifest.")
    return CoreVocabulary(tuple(records), frozenset(memberships),
                          {form: tuple(names) for form, names in memberships.items()}, digest)


def _code_ranges(text: str) -> list[tuple[int, int]]:
    return [match.span() for match in CODE.finditer(text)]


def mask_link_destinations(text: str) -> str:
    """Mask hidden HTTP(S) destinations, preserving labels, alt text and offsets."""
    chars = list(text)
    code_ranges = _code_ranges(text)
    for match in LINK.finditer(text):
        if any(start <= match.start() < end for start, end in code_ranges):
            continue
        start, end = match.span(1)
        chars[start:end] = " " * (end - start)
    return "".join(chars)


def _citation_valid(token: str) -> bool:
    if token.startswith("cite"):
        refs = token[len("cite"):-1].split("")
        return bool(refs) and all(CITATION_REF.fullmatch(ref) for ref in refs)
    if not token.startswith("genui"):
        return False
    try:
        obj = json.loads(token[len("genui"):-1], object_pairs_hook=_unique_json)
    except (ValueError, TypeError):
        return False
    if not isinstance(obj, dict) or set(obj) != {"citation"} or not isinstance(obj["citation"], dict):
        return False
    citation = obj["citation"]
    if set(citation) == {"ref"}:
        refs = [citation["ref"]]
    elif set(citation) == {"refs"} and isinstance(citation["refs"], list):
        refs = citation["refs"]
    else:
        return False
    return bool(refs) and all(isinstance(ref, str) and CITATION_REF.fullmatch(ref) for ref in refs)


def _visible(text: str) -> tuple[str, list[tuple[int, str]]]:
    chars = list(mask_link_destinations(text))
    errors = []
    matched_starts = set()
    code_ranges = _code_ranges(text)
    for match in CITATION.finditer(text):
        matched_starts.add(match.start())
        if _citation_valid(match.group()) and not any(start <= match.start() < end for start, end in code_ranges):
            chars[match.start():match.end()] = " " * len(match.group())
        else:
            errors.append((match.start(), match.group()))
    for match in re.finditer("", text):
        if match.start() not in matched_starts:
            errors.append((match.start(), text[match.start():match.start() + 80]))
    return "".join(chars), errors


def _normalized_visible(text: str) -> tuple[str, list[int]]:
    """Case/space/emphasis normalization with a map to original draft offsets."""
    items = list(enumerate(text))
    while True:
        working = "".join(char for _, char in items)
        matches = list(EMPHASIS.finditer(working))
        if not matches:
            break
        removed = set()
        for match in matches:
            size = len(match.group(1))
            for index in list(range(match.start(), match.start() + size)) + list(range(match.end() - size, match.end())):
                removed.add(index)
        items = [item for index, item in enumerate(items) if index not in removed]
    result, offsets = [], []
    for index, char in items:
        if char.isspace():
            if result and result[-1] != " ":
                result.append(" ")
                offsets.append(index)
        else:
            for lowered in normalize(char):
                result.append(lowered)
                offsets.append(index)
    if result and result[-1] == " ":
        result.pop()
        offsets.pop()
    return "".join(result), offsets


def _occurrences(text: str, form: str) -> list[re.Match]:
    return list(re.finditer(r"(?<!\w)" + re.escape(form) + r"(?!\w)", text))


def _word_allowed(word: str, allowed: frozenset[str], science: bool) -> bool:
    word = normalize(word)
    if word in allowed:
        return True
    if not science:
        return False
    if word in CONTRACTIONS and all(part in allowed for part in CONTRACTIONS[word]):
        return True
    return word.endswith("'s") and word[:-2] in allowed


def _core_fragment_errors(text: str, core: CoreVocabulary) -> list[str]:
    # No link, citation, code or TeX exceptions exist in declaration definitions.
    covered = bytearray(len(text))
    normalized, offsets = _normalized_visible(text)
    for form in core.forms:
        if not WORD.fullmatch(form):
            for match in _occurrences(normalized, form):
                start, end = offsets[match.start()], offsets[match.end() - 1] + 1
                covered[start:end] = b"\x01" * (end - start)
    for match in NUMBER.finditer(text):
        covered[match.start():match.end()] = b"\x01" * len(match.group())
    errors = []
    for match in WORD.finditer(text):
        if all(covered[match.start():match.end()]):
            continue
        covered[match.start():match.end()] = b"\x01" * len(match.group())
        if not _word_allowed(match.group(), core.forms, True):
            errors.append(match.group())
    for index, char in enumerate(text):
        if not covered[index] and not char.isspace() and char not in PUNCTUATION:
            errors.append(char)
    return errors


def _required_text(item: dict, key: str) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip() or any(ord(char) < 32 and not char.isspace() for char in value):
        raise ValueError(f"Declaration {key!r} must be a nonempty text string.")
    return value.strip()


def _ordinary_word_count(text: str) -> int:
    """Scientific-notation exponent markers are not definition words."""
    return len(WORD.findall(NUMBER.sub(lambda match: " " * len(match.group()), text)))


def validate_terms(payload: object, core: CoreVocabulary) -> tuple[Term, ...]:
    if not isinstance(payload, dict) or set(payload) != {"terms"} or not isinstance(payload["terms"], list):
        raise ValueError('Terms manifest must have the shape {"terms": [...]} only.')
    result, seen = [], set()
    for item in payload["terms"]:
        if not isinstance(item, dict) or set(item) != {"term", "forms", "definition", "reason"}:
            raise ValueError("Each term needs exactly term, forms, definition and reason.")
        term, definition, reason = (_required_text(item, key) for key in ("term", "definition", "reason"))
        if not isinstance(item["forms"], list) or not item["forms"]:
            raise ValueError(f"Term {term!r} needs a nonempty list of explicit forms.")
        forms = []
        for form in item["forms"]:
            if not isinstance(form, str) or not form.strip() or not WORD.search(form) or any(c in form for c in "[]{}<>`*_|\\\n\r\t"):
                raise ValueError(f"Term {term!r} has an invalid explicit form.")
            forms.append(_phrase(form))
        if len(set(forms)) != len(forms) or _phrase(term) not in forms:
            raise ValueError(f"Term {term!r} must occur in its forms, without duplicates.")
        if _phrase(term) in seen:
            raise ValueError(f"Duplicate term declaration: {term!r}.")
        if _ordinary_word_count(definition) < 3:
            raise ValueError(f"Definition for {term!r} needs at least three ordinary core words.")
        errors = _core_fragment_errors(definition, core)
        if errors:
            raise ValueError(f"Definition for {term!r} contains noncore text: {', '.join(repr(x) for x in errors)}.")
        seen.add(_phrase(term))
        result.append(Term(_phrase(term), tuple(forms), definition, reason))
    return tuple(result)


def load_terms(path: Path | str, core: CoreVocabulary) -> tuple[Term, ...]:
    return validate_terms(read_json(path), core)


def validate_symbols(payload: object, core: CoreVocabulary) -> tuple[Symbol, ...]:
    if not isinstance(payload, dict) or set(payload) != {"symbols"} or not isinstance(payload["symbols"], list):
        raise ValueError('Symbols manifest must have the shape {"symbols": [...]} only.')
    result, seen = [], set()
    for item in payload["symbols"]:
        if not isinstance(item, dict) or set(item) != {"symbol", "meaning"}:
            raise ValueError("Each symbol needs exactly symbol and meaning.")
        symbol, meaning = (_required_text(item, key) for key in ("symbol", "meaning"))
        if not (len(symbol) == 1 and (symbol in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" or symbol in GREEK.values())) and not (symbol.startswith("\\") and symbol[1:] in GREEK):
            raise ValueError(f"Symbol {symbol!r} must be one letter or an approved TeX Greek command.")
        if symbol in seen:
            raise ValueError(f"Duplicate symbol declaration: {symbol!r}.")
        if not _ordinary_word_count(meaning) or _core_fragment_errors(meaning, core):
            raise ValueError(f"Meaning for symbol {symbol!r} must use ordinary core words.")
        seen.add(symbol)
        result.append(Symbol(symbol, meaning))
    return tuple(result)


def load_symbols(path: Path | str, core: CoreVocabulary) -> tuple[Symbol, ...]:
    return validate_symbols(read_json(path), core)


def check_text(text: str, allowed: frozenset[str] | None = None, *, mode: str | None = None,
               core: CoreVocabulary | None = None, terms: Iterable[Term] | dict | None = None,
               symbols: Iterable[Symbol] | dict | None = None) -> dict:
    """Check every visible word. Passing legacy ``allowed`` defaults to classic.

    The CLI always supplies a mode. New callers normally supply ``core`` or let
    the default research mode load the verified bundled core.
    """
    mode = mode or ("classic" if allowed is not None and core is None else "research")
    if mode not in MODES:
        raise ValueError(f"Unknown mode: {mode!r}.")
    science = mode != "classic"
    if not science:
        if terms is not None or symbols is not None:
            raise ValueError("Classic mode rejects term and symbol manifests.")
        if allowed is None:
            _, allowed = load_words()
    else:
        core = core or load_core()
        allowed = core.forms
        if mode == "undergraduate-strict" and terms is not None:
            raise ValueError("Undergraduate-strict mode rejects a terms manifest.")
    term_entries = validate_terms(terms, core) if isinstance(terms, dict) else tuple(terms or ())
    symbol_entries = validate_symbols(symbols, core) if isinstance(symbols, dict) else tuple(symbols or ())
    if any(not isinstance(item, Term) for item in term_entries) or any(not isinstance(item, Symbol) for item in symbol_entries):
        raise ValueError("Declarations must be validated terms/symbols or manifest objects.")
    # Dataclass construction is public, so revalidate instead of trusting callers.
    if term_entries:
        term_entries = validate_terms({"terms": [dict(term=t.term, forms=list(t.forms), definition=t.definition, reason=t.reason) for t in term_entries]}, core)
    if symbol_entries:
        symbol_entries = validate_symbols({"symbols": [dict(symbol=s.symbol, meaning=s.meaning) for s in symbol_entries]}, core)
    visible, citation_errors = _visible(text)
    normalized, original_offsets = _normalized_visible(visible)
    line_starts = [0] + [i + 1 for i, ch in enumerate(text) if ch == "\n"]
    issues, words_seen = [], []
    covered = bytearray(len(visible))

    def issue(kind: str, value: str, offset: int = 0, **extra: object) -> None:
        line_index = bisect_right(line_starts, offset) - 1
        issues.append(dict(kind=kind, text=value, line=line_index + 1,
                           column=offset - line_starts[line_index] + 1, **extra))

    def cover(start: int, end: int) -> None:
        covered[start:end] = b"\x01" * (end - start)

    def cover_match(match: re.Match) -> None:
        if match.start() != match.end():
            cover(original_offsets[match.start()], original_offsets[match.end() - 1] + 1)

    for offset, value in citation_errors:
        issue("invalid_citation", value, offset)
    if science:
        for match in NUMBER.finditer(visible):
            cover(*match.span())
        # Explicitly listed compound/phrase core forms retain their full scope.
        for form in allowed:
            if not WORD.fullmatch(form):
                for match in _occurrences(normalized, form):
                    cover_match(match)
    term_usage = []
    for entry in term_entries:
        occurrences = sorted((match for form in entry.forms for match in _occurrences(normalized, form)), key=lambda m: m.start())
        canonical = _occurrences(normalized, entry.term)
        definition_text, _ = _normalized_visible(entry.definition)
        definitions = _occurrences(normalized, definition_text)
        near = bool(occurrences and any(
            0 <= match.start() - occurrences[0].end() <= DEFINITION_DISTANCE
            or 0 <= occurrences[0].start() - match.end() <= DEFINITION_DISTANCE
            for match in definitions))
        offset = original_offsets[occurrences[0].start()] if occurrences else 0
        if not canonical:
            issue("declared_term_missing", entry.term, offset)
        if not definitions:
            issue("term_definition_missing", entry.term, offset, definition=entry.definition)
        elif not near:
            issue("term_definition_not_near_first_use", entry.term, offset, maximum_gap=DEFINITION_DISTANCE)
        for match in occurrences:
            cover_match(match)
        term_usage.append(dict(term=entry.term, forms=list(entry.forms), occurrences=len(occurrences),
                               canonical_present=bool(canonical), definition_present=bool(definitions),
                               definition_near_first_use=near, definition=entry.definition, reason=entry.reason))
    symbol_usage = []
    symbol_spellings = set()
    for entry in symbol_entries:
        spellings = {entry.symbol}
        if entry.symbol.startswith("\\"):
            spellings.add(GREEK[entry.symbol[1:]])
        elif entry.symbol in GREEK.values():
            spellings.update("\\" + name for name, value in GREEK.items() if value == entry.symbol)
        symbol_spellings.update(spellings)
        found = []
        for spelling in spellings:
            # Variables are case-sensitive, unlike prose and term matching.
            for match in re.finditer(r"(?<!\w)" + re.escape(spelling) + r"(?!\w)", visible):
                found.append(match)
                cover(*match.span())
        meaning, _ = _normalized_visible(entry.meaning)
        meanings = _occurrences(normalized, meaning)
        if not found:
            issue("declared_symbol_missing", entry.symbol)
        if not meanings:
            issue("symbol_meaning_missing", entry.symbol, found[0].start() if found else 0, meaning=entry.meaning)
        symbol_usage.append(dict(symbol=entry.symbol, occurrences=len(found), meaning=entry.meaning, meaning_present=bool(meanings)))
    if science:
        for match in TEX_COMMAND.finditer(visible):
            if all(covered[match.start():match.end()]):
                continue
            name = match.group(1)
            if name in TEX_SYNTAX:
                cover(*match.span())
            elif name in GREEK:
                issue("undeclared_symbol", match.group(), match.start())
                cover(*match.span())
            elif name in TEX_FUNCTIONS:
                cover(match.start(), match.start() + 1)
            else:
                issue("unsupported_tex_command", match.group(), match.start())
                cover(match.start(), match.start() + 1)
        for match in re.finditer(r"\\(?:[()\[\],;! ]|\\)", visible):
            cover(*match.span())
    for match in WORD.finditer(visible):
        word = match.group()
        words_seen.append(normalize(word))
        if all(covered[match.start():match.end()]):
            continue
        cover(*match.span())
        if not _word_allowed(word, allowed, science):
            kind = "undeclared_symbol" if science and len(word) == 1 and word.isalpha() else "unlisted_word"
            issue(kind, word, match.start())
    punctuation = SCIENCE_PUNCTUATION if science else PUNCTUATION
    for offset, char in enumerate(visible):
        if not covered[offset] and not char.isspace() and char not in punctuation:
            issue("unsupported_character", char, offset)
    if not words_seen and not (science and NUMBER.search(visible)):
        issue("empty_text", "")
    issues.sort(key=lambda item: (item["line"], item["column"], item["kind"]))
    counts = Counter(normalize(i["text"]) for i in issues if i["kind"] in ("unlisted_word", "undeclared_symbol"))
    result = dict(ok=not issues, mode=mode, word_count=len(words_seen), unique_word_count=len(set(words_seen)),
                  unlisted_words=dict(sorted(counts.items())), issues=issues,
                  declared_term_usage=term_usage, declared_symbol_usage=symbol_usage)
    if science:
        result.update(vocabulary_lemmas=core.lemma_count, vocabulary_surface_forms=len(core.forms), core_sha256=core.sha256)
        single_letters = sorted({word for word in words_seen if len(word) == 1 and word in allowed})
        result["semantic_review_notes"] = (["Single-letter core words can also denote variables; review their meaning: " + ", ".join(single_letters)] if single_letters else [])
    else:
        result.update(vocabulary_entries=EXPECTED_ENTRIES, vocabulary_normalized_entries=EXPECTED_NORMALIZED)
    return result


def lookup_words(words: list[str], mode: str, core: CoreVocabulary | None, allowed: frozenset[str]) -> dict:
    results = []
    for word in words:
        form = _phrase(word)
        lemmas = list(core.memberships.get(form, ())) if core is not None else []
        results.append(dict(query=word, normalized=form, exact_form=form in allowed,
                            lemmas=lemmas, contraction_or_possessive_allowed=_word_allowed(form, allowed, mode != "classic")))
    return dict(mode=mode, vocabulary_lemmas=core.lemma_count if core else None,
                vocabulary_surface_forms=len(allowed), lookup=results)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", nargs="?", help="UTF-8 draft; omit or use - for stdin")
    parser.add_argument("--mode", choices=MODES, default="research")
    parser.add_argument("--terms", type=Path, help="Explicit topic-term JSON manifest; research mode only")
    parser.add_argument("--symbols", type=Path, help="Explicit symbol/meaning JSON manifest; science modes only")
    parser.add_argument("--json", action="store_true", help="Print structured results")
    parser.add_argument("--list", action="store_true", help="Print every explicit surface form for the selected mode")
    parser.add_argument("--lookup", nargs="+", metavar="WORD", help="Report exact-form membership and core lemmas")
    args = parser.parse_args()
    try:
        if args.mode != "research" and args.terms is not None:
            raise ValueError(f"{args.mode} mode rejects a terms manifest.")
        if args.mode == "classic" and args.symbols is not None:
            raise ValueError("Classic mode rejects a symbols manifest.")
        if args.list and args.lookup:
            raise ValueError("Choose either --list or --lookup.")
        core = None
        if args.mode == "classic":
            entries, allowed = load_words()
        else:
            core = load_core()
            allowed = core.forms
            entries = sorted(allowed)
        terms = load_terms(args.terms, core) if args.terms is not None else None
        symbols = load_symbols(args.symbols, core) if args.symbols is not None else None
        if args.list:
            print(json.dumps(dict(mode=args.mode, forms=entries), ensure_ascii=False, indent=2) if args.json else "\n".join(entries))
            return 0
        if args.lookup:
            result = lookup_words(args.lookup, args.mode, core, allowed)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                for item in result["lookup"]:
                    print(f"{item['query']}: exact_form={str(item['exact_form']).lower()}; lemmas={', '.join(item['lemmas']) or '(none)'}; contraction_or_possessive_allowed={str(item['contraction_or_possessive_allowed']).lower()}")
            return 0
        draft = sys.stdin.read() if args.file in (None, "-") else Path(args.file).read_text(encoding="utf-8")
        result = check_text(draft, allowed if args.mode == "classic" else None, mode=args.mode,
                            core=core, terms=terms, symbols=symbols)
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        if args.json:
            print(json.dumps(dict(ok=False, mode=args.mode, error=str(exc)), ensure_ascii=False))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["ok"]:
        print(f"PASS ({args.mode}): {result['word_count']} words; lexical checks passed. Scientific correctness requires separate review.")
    else:
        print(f"FAIL ({args.mode}): {len(result['issues'])} issue(s).")
        for item in result["issues"]:
            print(f"{item['line']}:{item['column']}: {item['kind']}: {item['text']!r}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
