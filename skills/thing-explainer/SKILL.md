---
name: thing-explainer
description: Explain complex subjects, objects, papers, or passages creatively using only Randall Munroe’s bundled Thing Explainer vocabulary, with a deterministic word check. Use for Thing Explainer, Up Goer Five, or explanations constrained to the ten hundred most common words. Do not apply to ordinary requests for simplicity or progressive explanations without this vocabulary constraint.
---

# Thing Explainer

Explain the real mechanism or argument with a small vocabulary and an adult mind. Use vivid, original language, concrete scenes, apt comparisons, and occasional dry humor. Apply the vocabulary constraint from Randall Munroe’s *Thing Explainer*; do not imitate his personal voice or reuse his passages.

## Vocabulary contract

- Treat [references/words.txt](references/words.txt) as the sole allowlist. It contains **every one of the 3,634 spellings** from the official Simple Writer 0.2.1 list, including inflections and contractions. Straight and curly apostrophe variants collapse to 3,616 entries. Munroe counts most forms together; this is the official expanded form of his “ten hundred words,” not a generic frequency list or a newly invented list of roots. See [references/source.json](references/source.json) for provenance and checksums.
- Read the entire bundled list before drafting. Do not fetch a replacement list, rely on memory of common English, or silently add words. A word that feels easy can still be forbidden; `thousand`, `science`, and `energy` are absent.
- Accept only exact membership after lowercasing and normalizing curly apostrophes. Allow listed inflections and contractions only. Do not invent new forms, infer stems, or exempt arbitrary possessives. Rephrase an unlisted possessive as “the roof of the house.” Check each component of hyphenated phrases; do not split a forbidden word to disguise it.
- Apply the constraint to **all authored, reader-facing text** in an explanation: title, introduction, headings, body, quoted material, tables, captions, image text, alt text, source-link labels, follow-up questions, and progress notes. Do not repeat an unlisted technical name from the prompt, introduce a jargon glossary, or append an unchecked sign-off.
- Spell numbers with allowed words. Do not evade the vocabulary with digits, equations, acronyms, foreign words, Unicode lookalikes, code, emoji, or obscure technical senses of otherwise common words. Ordinary punctuation and Markdown layout are fine.
- Use descriptive Markdown links for evidence, with simple labels such as `[Read more here](https://example.org/paper)`. Only the nonvisible link destination is outside the word constraint; check the label. Use inline HTTP(S) links without title attributes or reference-link syntax. Do not use bare URLs or raw citation tokens as prose.
- Keep this constraint for the requested explanation; do not impose it on unrelated later tasks. Skill instructions, internal analysis, scripts, and source documents are not explanation output. Honor explicit user changes of scope; never silently relax the constraint or claim compliance for an exempted passage.

## Explain artfully and accurately

1. **Understand before translating.** Identify what the subject is, what its parts do, how causes produce effects, and which distinctions must survive. For an argument, preserve premises, conclusion, objections, and uncertainty. Read the supplied material; obtain sources when accuracy requires them. Never replace an inaccessible source with an invented explanation.
2. **Choose a useful scene.** Start with the central idea in one or two sentences. Build from a familiar action or object when it truly helps. Prefer short, concrete names based on function, shape, or motion over strings of “thing,” “stuff,” and “little.” Define a coined phrase at first use and keep it stable. The reader should not have to solve a riddle to identify each part.
3. **Show the chain of causes.** Explain what changes, why the next step follows, and how the parts fit together. Use a small example or counterexample when useful. Do not reduce a mechanism to an analogy or a list of renamed parts. For abstract ideas, use a concrete situation and then explain which relationship it illustrates.
4. **Keep the limits visible.** Mark an analogy as a comparison and say where it breaks if that matters. Preserve distinctions such as evidence versus guess, correlation versus cause, model versus reality, and one case versus all cases. Do not invent intention in cells or computers, erase uncertainty, or state a false simplification to satisfy the vocabulary. Narrow a claim when needed and say what the account leaves out in allowed words.
5. **Shape the piece for the subject.** Prefer connected, rhythmic prose, short sentences, and a memorable closing image that reinforces the mechanism. Use a compact table or sequence only when it clarifies relationships. Choose depth from the request; the small vocabulary does not require a shallow explanation. Avoid baby talk, forced whimsy, and humor that displaces an explanation. Use common senses even when a rare sense would pass the word check.

Research with ordinary technical language internally. Preserve citations using simple link labels; this vocabulary restriction does not excuse unsupported claims. If the input is ambiguous or unavailable, ask the minimum needed question in allowed words. If exact notation or terminology is essential but outside scope, explain the limit in allowed words rather than silently inserting it.

## Check, revise, deliver

Use the bundled Python standard-library checker. Resolve `SKILL_DIR` to this skill’s actual installed directory; its parent folder may be renamed after installation. Write a UTF-8 draft outside the skill folder.

```bash
python3 "$SKILL_DIR/scripts/check_words.py" --list
python3 "$SKILL_DIR/scripts/check_words.py" /absolute/path/to/draft.md --json
```

Or pipe text to the checker; no file argument means stdin. The checker verifies vocabulary integrity, reports every unlisted word with line/column locations, rejects unsupported symbols and empty input, and exits nonzero on failure. It checks headings, link labels, and body alike; it masks only simple inline link destinations. Plain text, ordinary Markdown, and tables are supported. Do not insert Mermaid, HTML, rendered image lettering, or other unvalidated formats by default.

- Revise **every** flagged item, reread for meaning and naturalness, and run the checker again. Reword complete sentences when a local substitution makes the account clumsy or inaccurate. Never edit the vocabulary or weaken the checker to make a draft pass.
- Review meaning separately: can the reader explain what causes what, distinguish the relevant concepts, and identify the main limitation? A zero-error word check proves vocabulary compliance, not factual accuracy or literary quality.
- Run the final check on the **complete exact text to be delivered**, including any source section and opening or closing text. After it passes, deliver that text without additions or edits. Do not print the checker report unless requested.
- If execution is unavailable, manually check every word against the bundled list, shorten the output if needed, and do not claim automated verification. If the list itself is unavailable, say “I need the word list before I can do this.” rather than substituting another vocabulary.

For checker maintenance, run `python3 "$SKILL_DIR/scripts/test_check_words.py"`. These tests check vocabulary completeness and actual acceptance/rejection behavior; they do not evaluate the explanation’s truth or clarity.
