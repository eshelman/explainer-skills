---
name: thing-explainer
description: Explain complex science, technology, and philosophy with an embedded 15,000-lemma general undergraduate vocabulary, checked topic-term definitions, and explained notation. Use for Thing Explainer or the broader undergraduate version. Preserve classic mode for Up Goer Five or ten-hundred-word constraints. Do not activate for ordinary questions without this explanation style or vocabulary constraint.
---

# Thing Explainer — version 2

Explain difficult ideas with familiar language while preserving the requested scientific depth. Default to the embedded **15,000-lemma Undergraduate General core** and introduce necessary specialist terms explicitly. Write vivid, original explanations with an adult mind; use concrete examples and apt comparisons without imitating Randall Munroe’s personal voice or copying his passages.

## Choose a mode

- **Research (default):** core vocabulary, explicitly defined topic terms, and explained notation. Aim for an English-fluent undergraduate outside the topic’s specialty. Explain graduate and frontier material by building prerequisites, not deleting difficult distinctions.
- **Undergraduate strict:** when asked for only the new embedded vocabulary, use the core without specialist-word exceptions. Retain ordinary numbers and explained notation; state genuine limits rather than silently broadening the vocabulary.
- **Classic:** when explicitly asked for the original restriction, Up Goer Five, or the ten hundred words, follow the classic procedure below. Do not default to classic merely because the user invokes Thing Explainer.

Scope the constraint to the requested explanation, not unrelated later tasks. Check all authored reader-facing explanation text: titles, introductions, body, tables, captions, alt text, quotations, source labels, questions and closing text. Source material, internal notes, commands and these skill instructions are not explanation output.

## Use the embedded core

Use [references/core-15000.tsv](references/core-15000.tsv) as the sole general vocabulary. It contains exactly 15,000 unique canonical headword strings, recorded parts of speech, and explicitly enumerated accepted forms. Homographs share a headword; curated spelling aliases do not create extra headwords. Do not infer derivatives from roots or authorize an entire family.

Read [references/undergraduate-core.md](references/undergraduate-core.md) when first using this version. Counts, hashes, selection inputs and versions are in [references/core-manifest.json](references/core-manifest.json); reuse notices are in [references/core-license.txt](references/core-license.txt). The core is provisional editorial common ground, not a measured guarantee of undergraduate comprehension. Per-word familiarity percentages are deliberately absent.

Use lookups rather than loading the full table into context. Resolve SKILL_DIR to the actual installed folder.

~~~bash
python3 "$SKILL_DIR/scripts/check_words.py" --lookup inference constraints hypothesis algorithms
~~~

Membership permits an ordinary sense, not every specialist meaning. Explain field-specific uses of familiar words such as attention, work, energy, field, random, normal, bias, model, significance and confidence. Consult [references/sense-notes.json](references/sense-notes.json) for reminders. Expand unfamiliar acronyms on first use even if they pass the vocabulary check.

## Explain accurately and artfully

1. Identify the actual question, mechanism or argument, relevant quantities and relationships, and assumptions, limitations and uncertainties that must survive. Read supplied material and obtain primary sources when verification is needed. Do not invent an inaccessible paper’s contents.
2. Orient the reader with the central idea, then establish prerequisites in a useful order. Prefer direct terms such as evidence, probability, inference and approximation over elaborate substitute names. Preserve exact distinctions, scope, units, comparisons, and the difference between prediction and a causal claim.
3. Show how causes produce effects or premises support a conclusion. An analogy may introduce a concept but must not replace its mechanism; state its limits when material. Use examples, calculations, tables or diagrams when they clarify.
4. Retain necessary specialist names so readers can connect to the literature. Define them through core vocabulary, then use them consistently. Do not replace essential scientific concepts with vague stories, or swamp a short explanation with unnecessary jargon.
5. Preserve numbers, units, equations and standard notation when they improve precision. Define symbols and explain the relationship in words. Never introduce a false verbal simplification just to avoid notation.
6. Match depth to the request without an arbitrary length cap. Use readable sentences, rhythm, concrete language and occasional useful humor. Avoid baby talk, forced whimsy, decorative metaphors and unnecessary scholarly phrasing.

## Introduce topic terms and symbols

For research mode, create an explicit per-explanation JSON manifest outside the skill directory:

~~~json
{"terms":[{"term":"stochastic","forms":["stochastic"],"definition":"having outcomes that include random variation","reason":"The source contrasts this process with one having a fixed outcome."}]}
~~~

Require all four fields; include the canonical term in forms and enumerate other needed word or complete phrase forms. Definitions must contain at least three words and use core vocabulary (numeric literals are allowed), without depending on undeclared specialist terms. Build prerequisites first when needed.

Use each canonical term and its exact definition in the delivered explanation. After normalizing case, whitespace and Markdown emphasis, the definition must **start within 250 visible characters after the first accepted term-form occurrence, or finish within 250 characters before it**. An inline definition or adjacent sentence works; a distant glossary does not. This checks placement, not scientific truth or necessity.

For variables or Greek symbols, use an optional separate manifest:

~~~json
{"symbols":[{"symbol":"x","meaning":"the measured value"}]}
~~~

Use each symbol and its exact core-only meaning in the explanation. Symbols are single case-sensitive Latin/Greek characters or approved TeX Greek commands. Core words that happen to be single letters still need semantic review when used as variables. Units and mathematical function names must be core words or defined topic terms. Approved mathematical syntax does not exempt prose, variable names, unknown macros or text inside equations.

A declaration is permission for this explanation, not an expansion of the core. Prefer the smallest topic vocabulary the task actually needs; do not register arbitrary difficult words to evade the constraint.

## Check, revise, deliver

Write the complete exact output to a UTF-8 draft outside the skill folder. Runtime checking uses Python standard library and bundled data only, without downloads, frequency packages or morphology packages.

~~~bash
python3 "$SKILL_DIR/scripts/check_words.py" /absolute/path/draft.md --terms /absolute/path/terms.json --symbols /absolute/path/symbols.json --json
python3 "$SKILL_DIR/scripts/check_words.py" /absolute/path/draft.md --mode undergraduate-strict --json
~~~

Omit unnecessary manifests. Revise every unlisted word, invalid declaration, missing definition, unexplained symbol and unsupported construct. Reword awkward sentences instead of accumulating exemptions. Do not change the core, checksum or checker during explanation generation.

Use ordinary Markdown source links or genuine platform citation metadata. Check source labels and surrounding prose; only hidden URL destinations and well-formed citation tokens are opaque references. Code and equations do not receive a blanket exemption. The checker supports a limited TeX subset, not arbitrary TeX programs. Avoid raw HTML and unchecked image lettering.

Review meaning separately: preserve substantive claims and qualifications, distinguish observations from inference and speculation, check units and equations, and ask whether the reader can explain what causes what. A lexical pass proves neither accuracy nor comprehension.

After all edits, check the whole final text, including titles, labels, citations and closing text. Deliver that exact text without unchecked additions. Keep internal manifests and reports out of the answer unless requested. Do not claim automated verification when execution was unavailable. If core resources cannot be read, report that limitation instead of substituting a remembered list.

## Classic compatibility

Keep [references/words.txt](references/words.txt) and [references/source.json](references/source.json) unchanged. They hold all 3,634 official Simple Writer spellings, or 3,616 after apostrophe normalization. In classic mode, read that entire list; use only exact normalized entries, spell numbers out, and reject specialist-term or symbol declarations, unlisted derivatives and arbitrary possessive suffixes. Check all explanation text; genuine citations and hidden link destinations retain their non-prose metadata.

~~~bash
python3 "$SKILL_DIR/scripts/check_words.py" --mode classic --list
python3 "$SKILL_DIR/scripts/check_words.py" /absolute/path/draft.md --mode classic --json
~~~

For maintenance only, run scripts/test_check_words.py. Rebuild with scripts/build_core.py and its pinned dependencies only when the user requests a vocabulary revision. Ordinary skill use must never rebuild or resize the core.
