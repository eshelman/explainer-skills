#!/usr/bin/env python3
"""Validate Thing Explainer prose against the complete official spelling list.

Python standard library only. Exit 0: compliant; 1: text fails; 2: input or
vocabulary-integrity failure. Not a semantic, factual, or readability checker.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
WORDLIST = ROOT / "references" / "words.txt"
EXPECTED_SHA256 = "fa78b7ef472d9b6ba5c0e9f7e8919e8e825d9b5c307baac28e5d4e0a1cebf5c7"
EXPECTED_ENTRIES = 3634
EXPECTED_NORMALIZED = 3616
# Whole Unicode letter sequences are checked, not silently transliterated.
WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)
# Deliberately small Markdown subset: no title attributes, nested URLs, or
# reference definitions. Percent-encode parentheses in link destinations.
LINK = re.compile(r"!?\[[^\]\n]*\]\((https?://[^\s()<>]+)\)")
PUNCTUATION = frozenset(".,;:!?-'’‘\"“”()[]{}*/_#>|~–—…")


def normalize(word: str) -> str:
    return word.replace("’", "'").lower()


def load_words() -> tuple[list[str], frozenset[str]]:
    data = WORDLIST.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise ValueError("Bundled vocabulary checksum mismatch; restore the original list.")
    entries = data.decode("utf-8").splitlines()
    allowed = frozenset(normalize(word) for word in entries)
    if (len(entries) != EXPECTED_ENTRIES or len(set(entries)) != EXPECTED_ENTRIES
            or len(allowed) != EXPECTED_NORMALIZED):
        raise ValueError("Bundled vocabulary count mismatch.")
    return entries, allowed


def mask_link_destinations(text: str) -> str:
    chars = list(text)
    for match in LINK.finditer(text):
        start, end = match.span(1)
        chars[start:end] = " " * (end - start)
    return "".join(chars)


def check_text(text: str, allowed: frozenset[str]) -> dict:
    visible = mask_link_destinations(text)
    line_starts = [0] + [i + 1 for i, ch in enumerate(text) if ch == "\n"]
    issues = []
    covered = bytearray(len(visible))
    words_seen = []

    def issue(kind: str, value: str, offset: int) -> None:
        line_index = bisect_right(line_starts, offset) - 1
        issues.append({"kind": kind, "text": value, "line": line_index + 1,
                       "column": offset - line_starts[line_index] + 1})

    for match in WORD.finditer(visible):
        word = match.group()
        words_seen.append(normalize(word))
        covered[match.start():match.end()] = b"\x01" * len(word)
        if normalize(word) not in allowed:
            issue("unlisted_word", word, match.start())

    for offset, char in enumerate(visible):
        if covered[offset] or char.isspace() or char in PUNCTUATION:
            continue
        issue("unsupported_character", char, offset)

    if not words_seen:
        issue("empty_text", "", 0)

    issues.sort(key=lambda item: (item["line"], item["column"]))
    counts = Counter(normalize(i["text"]) for i in issues if i["kind"] == "unlisted_word")
    return {"ok": not issues, "word_count": len(words_seen),
            "unique_word_count": len(set(words_seen)),
            "unlisted_words": dict(sorted(counts.items())), "issues": issues,
            "vocabulary_entries": EXPECTED_ENTRIES,
            "vocabulary_normalized_entries": EXPECTED_NORMALIZED}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", help="UTF-8 draft; omit or use - for stdin")
    parser.add_argument("--json", action="store_true", help="Print structured results")
    parser.add_argument("--list", action="store_true", help="Print every bundled spelling")
    args = parser.parse_args()
    try:
        entries, allowed = load_words()
        if args.list:
            print("\n".join(entries))
            return 0
        draft = (sys.stdin.read() if args.file in (None, "-")
                 else Path(args.file).read_text(encoding="utf-8"))
        result = check_text(draft, allowed)
    except (OSError, UnicodeError, ValueError) as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["ok"]:
        print(f"PASS: {result['word_count']} words; no unlisted words or unsupported characters.")
    else:
        print(f"FAIL: {len(result['issues'])} issue(s).")
        for item in result["issues"]:
            print(f"{item['line']}:{item['column']}: {item['kind']}: {item['text']!r}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
