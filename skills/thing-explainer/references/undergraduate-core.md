# Undergraduate General core — first release

Use this fixed 15,000-headword vocabulary as Thing Explainer v2’s general language. It is a first release to evaluate through use, not an experiment comparing vocabulary sizes.

## Count and selection

Count unique lower-case canonical headword strings; record POS but combine homographs. Inflections and curated US/UK spelling aliases are accepted forms, not extra headwords. This operational lemma convention differs from broad word families and POS-separated senses.

Generate candidates from the first 150,000 English wordfreq surface types. Keep LemmInflect dictionary-backed canonical headwords, rather than treating every surface type as a new lemma. Reserve independently authored general and academic seeds, merge explicit spelling aliases, remove editorial technical-only exclusions, then fill exactly 15,000 slots by descending headword frequency with a lexical tie-break. Enumerate dictionary inflections and a small explicit editorial table for dictionary gaps. Never use runtime stemming or open-ended derivation.

The selection inputs are core-curation.json. The pinned, deterministic builder is scripts/build_core.py. The manifest records counts, SHA-256 hashes, package versions and input-file hashes. Runtime requires only bundled data and Python standard library.

## Limits

Frequency and dictionary membership are proxies for likely accessibility, not proof of audience understanding. The frequency snapshot is largely through 2021. The academic seeds keep conversational frequency from crowding out reasoning words such as constraint and inference. Technical exclusions are editorial and non-exhaustive. Explain specialist meanings even when their spellings pass.

The proposed >=95% measured recognition gate is NOT implemented. Inspection of the original authors’ OSF license showed CC BY-NC-SA 4.0, so this redistributable resource does not embed those per-word ratings or use them for selection. known_fraction is deliberately empty for every entry; do not invent scores or describe the core as undergraduate-validated. Evaluate this fixed release through use and revise its membership when requested.

Research mode permits explicit, locally defined necessary topic terms. Strict mode restricts lexical choices to the core. No checker establishes scientific truth or comprehension.

## Provenance

- Robyn Speer, wordfreq 3.1.1: https://github.com/rspeer/wordfreq . Cite https://doi.org/10.5281/zenodo.7199437 . Use its API for candidate ranking, not an export of its frequency values. Software is Apache-2.0; data carry CC BY-SA 4.0 and source attribution notices.
- Brad Jascob, LemmInflect 0.2.3: https://github.com/bjascob/LemmInflect . MIT-licensed dictionary lemma/inflection API.
- The editorial seeds, aliases and exclusions are independently authored. The adapted core vocabulary resource is CC BY-SA 4.0 with source notices retained in core-license.txt.
- Original prevalence project, inspected but not used: https://osf.io/g4xrt/ ; license.txt: https://osf.io/z7fgj/ .

Classic vocabulary provenance remains in source.json.
