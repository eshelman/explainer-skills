#!/usr/bin/env python3
"""Rebuild the fixed 15,000-headword core; not needed for ordinary skill use.

Build-only dependencies: wordfreq==3.1.1 and lemminflect==0.2.3.
Run with these pinned packages available on PYTHONPATH. Outputs go to this
installed personal skill, never a separate uninstalled scratch copy.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = 15000
VALID = re.compile(r"[a-z]+")
VERSIONS = {"wordfreq": "3.1.1", "lemminflect": "0.2.3"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict:
    for package, expected in VERSIONS.items():
        if importlib.metadata.version(package) != expected:
            raise ValueError(f"Build requires {package}=={expected}")
    from lemminflect import getAllInflections, getAllLemmas
    from wordfreq import top_n_list, zipf_frequency

    curation_path = ROOT / "references" / "core-curation.json"
    curation = json.loads(curation_path.read_text())
    variants = {k: v for k, v in curation["variants"].items() if k != v}
    technical = set(curation["technical_only"].lower().split())
    excluded = set(curation["exclude"].lower().split()) | technical
    general = set(curation["general_anchors"].lower().split()) - excluded
    academic = set(curation["academic_anchors"].lower().split()) - excluded
    manual = general | academic

    def canonical(word):
        word = variants.get(word, word)
        lemmas = getAllLemmas(word)
        if not lemmas or any(word in values for values in lemmas.values()):
            return word
        choices = {variants.get(value, value) for values in lemmas.values()
                   for value in values if VALID.fullmatch(value)}
        return sorted(choices, key=lambda w: (-zipf_frequency(w, "en"), w))[0] if choices else word

    # Frequency data suggest candidates. A candidate must be a dictionary
    # headword, not merely a frequently seen inflected surface string.
    candidates = {}
    for surface in top_n_list("en", 150000):
        if not VALID.fullmatch(surface):
            continue
        word = variants.get(surface, surface)
        if word in excluded:
            continue
        lemmas = getAllLemmas(word)
        pos = sorted(key for key, values in lemmas.items() if word in values)
        if pos:
            candidates[word] = set(pos)

    reserved = {}
    for raw in sorted(manual):
        if not VALID.fullmatch(raw):
            raise ValueError(f"Invalid curated word {raw!r}")
        word = canonical(raw)
        if word in excluded:
            continue
        mapping = getAllLemmas(word)
        pos = {key for key, values in mapping.items() if word in values}
        candidates.setdefault(word, set()).update(pos)
        reserved[word] = ("curated-academic" if raw in academic else "curated-general")
    if len(reserved) >= TARGET:
        raise ValueError("Curated seed unexpectedly consumes full core")
    ranked = sorted((w for w in candidates if w not in reserved),
                    key=lambda w: (-zipf_frequency(w, "en"), w))
    selected = set(reserved) | set(ranked[:TARGET - len(reserved)])
    if len(selected) != TARGET:
        raise ValueError("Insufficient distinct canonical headwords")

    aliases = {}
    for alias, head in variants.items():
        if head in selected:
            aliases.setdefault(head, set()).add(alias)

    records = []
    all_forms = set()
    for word in sorted(selected):
        forms = {word}
        bases = [word] + sorted(aliases.get(word, ()))
        for base in bases:
            forms.add(base)
            # Dictionary-backed inflections only: no productive stemming,
            # derivational families, or neural/out-of-vocabulary guesses.
            for values in getAllInflections(base).values():
                forms.update(v for v in values if VALID.fullmatch(v))
        for form in curation.get("extra_forms", {}).get(word, []):
            if not VALID.fullmatch(form):
                raise ValueError(f"Invalid editorial inflection {form!r}")
            forms.add(form)
        forms -= technical
        forms -= (set(curation["exclude"].lower().split()) - {word})
        if word not in forms:
            raise ValueError(f"Lost lemma {word}")
        all_forms.update(forms)
        records.append({
            "lemma": word,
            "pos": ",".join(sorted(candidates[word])) or "CURATED",
            "forms": "|".join(sorted(forms)),
            "known_fraction": "",
            # Do not reproduce the source frequency table. The complete
            # deterministic selection algorithm + pinned inputs is the audit.
            "zipf_frequency": "",
            "selection_reason": reserved.get(word, "general-frequency-dictionary"),
        })

    path = ROOT / "references" / "core-15000.tsv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), delimiter="\t",
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)

    inputs = {}
    for package in VERSIONS:
        dist = importlib.metadata.distribution(package)
        files = {}
        for item in dist.files or ():
            name = str(item)
            if name.startswith(package + "/") and not name.endswith(".pyc"):
                p = Path(dist.locate_file(item))
                if p.is_file():
                    files[name] = sha(p)
        inputs[package] = {"version": VERSIONS[package], "files_sha256": files}

    manifest = {
        "schema_version": 1,
        "skill_version": "2.0.0",
        "vocabulary_id": "undergraduate-general-15000-v1",
        "lemma_count": TARGET,
        "surface_form_count": len(all_forms),
        "core_sha256": sha(path),
        "curation_sha256": sha(curation_path),
        "counting_unit": "Unique lower-case canonical headword strings; parts of speech are recorded, homographs share one entry, curated US/UK spelling variants are aliases. Inflections are forms, not extra headwords.",
        "selection": {
            "candidate_pool": "150,000 English wordfreq surface types, filtered to dictionary-backed canonical headwords, plus the independently authored general/academic seeds.",
            "ranking": "Descending wordfreq English Zipf frequency of the headword; lexicographic tie-break. Reserve canonical curated seeds, then fill exactly 15,000 slots.",
            "curated_lemma_count": len(reserved),
            "curated_academic_count": sum(r["selection_reason"] == "curated-academic" for r in records),
            "dictionary_frequency_count": sum(r["selection_reason"] == "general-frequency-dictionary" for r in records),
            "technical_only_exclusions": len(technical),
            "inflections": "Enumerated LemmInflect dictionary forms plus explicit editorial forms for dictionary gaps and spelling aliases. No runtime stemming or family expansion.",
            "frequency_data_vintage": "wordfreq data snapshot through approximately 2021",
            "technical_scope": "Technical-only exclusions are editorial, non-exhaustive. Membership does not license an unexplained specialist sense.",
        },
        "familiarity": {
            "status": "Provisional; not validated against an undergraduate reader sample.",
            "known_fraction_column": "Intentionally empty; no measured percentages are claimed for these entries.",
            "not_used": "Original Brysbaert OSF prevalence materials are CC BY-NC-SA 4.0; their per-word ratings and filtering were not used in this redistributable core. The proposed >=95% prevalence gate is not implemented.",
            "limitation": "Frequency and dictionary membership are proxies for accessibility, not proof of knowledge. Evaluate this fixed 15,000-headword version through use and revise its membership.",
        },
        "sources": [
            {"name": "wordfreq", "version": "3.1.1", "author": "Robyn Speer",
             "url": "https://github.com/rspeer/wordfreq",
             "doi": "https://doi.org/10.5281/zenodo.7199437",
             "use": "Candidate generation and frequency ranking, not export of source frequency values.",
             "licenses": ["Apache-2.0 (software)", "CC-BY-SA-4.0 (frequency data; see source notices)"]},
            {"name": "LemmInflect", "version": "0.2.3", "author": "Brad Jascob",
             "url": "https://github.com/bjascob/LemmInflect",
             "use": "Canonical dictionary headwords, POS, and explicitly enumerated inflections.",
             "licenses": ["MIT"]},
            {"name": "Thing Explainer v2 editorial curation",
             "use": "Independently authored general/academic seeds, conventional spelling aliases and exclusions.",
             "path": "references/core-curation.json"},
        ],
        "resource_license": "CC-BY-SA-4.0 for core-15000.tsv, with LemmInflect MIT notice retained. Existing classic word list retains its own provenance.",
        "license_notice": "references/core-license.txt",
        "build_dependencies": inputs,
    }
    (ROOT / "references" / "core-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    try:
        result = build()
    except (OSError, ValueError, ImportError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps({k: result[k] for k in (
        "vocabulary_id", "lemma_count", "surface_form_count", "core_sha256")}, indent=2))
