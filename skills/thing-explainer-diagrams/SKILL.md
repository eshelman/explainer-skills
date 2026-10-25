---
name: thing-explainer-diagrams
description: Explain science and technology through original XKCD-inspired black-ink schematic drawings and structured prose. Default to research mode with an embedded 15,000-lemma undergraduate vocabulary, defined specialist terms, and explained notation. Use for Thing Explainer diagrams, illustrated explanations, and explanatory comics; preserve explicit classic and undergraduate-strict modes. Require rendered-image review for style, correctness, legibility, and vocabulary before delivery.
---

# Thing Explainer Diagrams — version 2

Create an original explanatory drawing with thin black ink on white, simple recognizable objects, expressive stick figures when useful, hand-lettered notes, and drawings that explain through action and spatial relationships. Preserve scientific depth, causal accuracy, and the selected vocabulary contract. Use familiar adult language; do not replace necessary concepts with vague substitute names.

Treat style as a requirement, not optional decoration. A corporate infographic with wobbly boxes fails. A generic flowchart with a stick figure pasted beside it also fails. Do not copy a published panel, trace an existing composition, sign as the artist, or imply authorship by Randall Munroe.

Read [references/visual-review.md](references/visual-review.md) before planning and before reviewing. The vocabulary and checker are bundled from Thing Explainer v2; no other skill must be installed.

## Choose a mode

- **Research (default):** use the embedded 15,000-lemma Undergraduate General core, explicitly defined necessary topic terms, and explained notation. Aim at an English-fluent undergraduate outside the specialty; build prerequisites rather than deleting graduate or frontier distinctions. Do not infer classic mode from the words Thing Explainer, XKCD, or a request for a simple drawing.
- **Undergraduate strict:** when asked to use only the new core, use `--mode undergraduate-strict` without topic-term exceptions. Retain ordinary numbers and explained notation; report genuine vocabulary limits.
- **Classic:** only when explicitly requested, use `--mode classic` and the original ten-hundred-word restriction. Read the entire [references/words.txt](references/words.txt); keep its 3,634 official spellings (3,616 normalized entries) and [references/source.json](references/source.json) unchanged. Spell numbers out; reject term and symbol manifests, unlisted derivatives, and arbitrary possessive suffixes.

## Vocabulary and terminology contract

Read [references/undergraduate-core.md](references/undergraduate-core.md) on first use and consult [references/sense-notes.json](references/sense-notes.json) for specialist senses of familiar words. Use [references/core-15000.tsv](references/core-15000.tsv) as the sole general vocabulary in research and undergraduate-strict modes. It has exactly 15,000 unique canonical headwords and enumerated accepted forms; do not infer derivatives or authorize whole word families. Use `--lookup` rather than loading the whole table into context. Counts, hashes and provenance are in [references/core-manifest.json](references/core-manifest.json); preserve [references/core-license.txt](references/core-license.txt). This is provisional editorial common ground, not a measured guarantee of undergraduate comprehension.

Apply the selected mode to all authored reader-facing explanation text: image lettering, titles, dialogue, captions, alt text, prose, caveats, source labels, progress notes, and closing text. Internal plans, code, manifests, reviewer reports and these instructions are exempt. The constraint does not extend to unrelated later tasks. Use genuine platform citations or ordinary Markdown source links; only hidden URL destinations and valid citation metadata are exempt, not their visible labels. Never weaken the vocabulary or checker to obtain a pass.

In research mode, retain the scientific names readers need to connect to the literature. Expand unfamiliar acronyms and explain specialist senses even when their spellings pass (for example attention, normal, bias or confidence). Introduce only terms needed for this explanation. Create a per-output term manifest outside the skill directory:

~~~json
{"terms":[{"term":"stochastic","forms":["stochastic"],"definition":"having outcomes that include random variation","reason":"Needed to distinguish random outcomes from a fixed outcome."}]}
~~~

Require all four fields. Enumerate accepted word or complete-phrase forms, including the canonical term. Each definition must use at least three core words (numeric literals are allowed), without undeclared specialist dependencies. Include the canonical term and its exact definition in the delivered text. After case, whitespace and Markdown-emphasis normalization, the definition must start within 250 visible characters after the first accepted term-form occurrence, or finish within 250 characters before it. A distant glossary is insufficient. The checker establishes placement and vocabulary, not whether the definition is scientifically adequate.

In research and undergraduate-strict modes, preserve useful numbers, units, equations and notation. Define symbols and explain the relationship in words; use an optional manifest such as:

~~~json
{"symbols":[{"symbol":"x","meaning":"the measured value"}]}
~~~

Use each symbol and its exact core-only meaning in the output. Symbols are single case-sensitive Latin/Greek letters or approved TeX Greek commands. Units and function names must be core words or defined topic terms (the latter only in research mode). Familiar single letters used as variables still need meaning review. Mathematical syntax is not an exemption for prose or arbitrary TeX. Draw mathematical relationships with deterministic tools when precision matters.

## Check the picture and prose as separate reading surfaces

- Keep exact intended image text in reading order in `image-text.txt`, and the complete accompanying text (including its title, alt text and source labels) in `prose.md`, outside the skill directory. The files must represent delivered text, not include hidden definitions merely to satisfy the checker.
- Check each surface independently before rendering and after every revision, using the selected mode and only the declarations used on that surface. Keep separate image/prose term and symbol manifests when their contents differ. Keep shared definitions consistent.
- A specialist name in an image title or label needs its definition visibly in that image near first use. Put symbol meanings in a nearby readable legend or callout. A definition solely in the caption, alt text, or prose cannot rescue an unexplained image label, and an image definition cannot rescue unexplained prose.
- Review spatial proximity as well as the checker's character-distance rule: a plausible linear transcription can hide a confusing visual layout. If a full definition cannot fit legibly, use an accurate core-word label in the image and introduce the specialist name in the prose, or split the image into smaller self-contained panels. Do not shrink definitions to unreadable footnotes.
- After rendering, transcribe actual visible lettering, symbols, numbers and units; check that transcription with the image manifests. Compare it to the approved text plan. OCR can assist, but not replace reading the image.
- Check the whole final accompanying text after all edits. No unchecked additions. Runtime checking uses the Python standard library and bundled resources only. If execution or core resources are unavailable, report the limitation; do not claim a pass or substitute a remembered list.

## Plan a drawing, not a page layout

1. Understand the subject first; check primary sources for uncertain or current claims. Keep an internal fact plan listing the mechanism, relationships, analogy mappings, and relevant limits.
2. Choose one central question and the simplest scene that lets the reader SEE its answer. Use a cutaway, a before/after pair, or two to three small scenes when useful.
3. Describe what each object DOES before writing its label. Draw the object or an explicitly marked analogy: e.g., workers waiting at a doorway, slips of paper moving between readers, a pot over a flame, or a telescope pointed at a path of light. An object-shaped drawing is not evidence that the analogy is true.
4. Apply the label-hiding test: with every word hidden, the drawing must still communicate a meaningful action, relationship, comparison, or obstruction. Labeled rectangles connected by arrows usually fail this test.
5. Prefer a few short callouts close to objects over section headings and paragraphs. Aim for under eighty visible words on a single image; reduce scope or split into panels when the subject needs more. This target applies only to image lettering, not the accompanying explanation. Do not overcompress into misleading labels.
6. Draft both reading surfaces and their necessary term/symbol declarations, then run the checker on each before rendering. Keep the technical fact plan out of the checked text. State assumptions, limits and uncertainty that matter; distinguish prediction from causation. Preserve exact quantities and units instead of replacing them with an inaccurate analogy.

## Required visual language

- Use mostly white space and thin, slightly uneven black strokes. Default to black and white. Use a small accent only if it encodes an essential distinction, never as a brand palette or decorative heading color.
- Use legible hand-lettering or a verified handwritten font with uneven baselines and human rhythm. Keep letterforms clear and size adequate. A font-family declaration is not proof of a loaded font: inspect the rendered result. Plain sans-serif headings and tiny handwritten captions do not satisfy this.
- For phone viewing, aim for the smallest label to read like roughly fourteen-pixel text in a 390-pixel-wide preview (about thirty-seven pixels in a 1024-pixel-wide source). Judge the rendered letters, not a requested font size. Small caveats count too; use extra white space or panels instead of shrinking them.
- Give objects distinctive shapes and affordances. Show an opening, a hand passing something, a folded note, a pot handle, or an actual path when that matters. Use poses, motion marks, leader lines, and short dialogue purposefully.
- Use thin callout lines and modest arrowheads, with endpoints that unambiguously attach to the intended object. Show what moves and what merely points.
- Let the scene carry the explanation. Stick figures are optional; they must perform explanatory work if present. Humor is optional and must follow the mechanism.
- Avoid broad pastel fills, rounded UI cards, status bars, pill shapes, decision diamonds, dashboard grids, giant bold sans-serif titles, section rules, numbered marketing sections, stock icons, gradients, shadows, and large block arrowheads. A necessary chart or enclosure is allowed, but must not dominate an otherwise generic business infographic.
- Do not treat adding line jitter, sepia paper, or a comic font to a conventional flowchart as a style fix. Redesign its composition.

## Choose a renderer that can meet the brief

For illustrative scenes, use an available image-generation tool when appropriate. Request original black-ink explanatory cartoon artwork with exact checked hand-lettered text and explicit spatial relationships. Follow the environment's image-generation/editing instructions. Describe the actual scene; do not rely on the artist's name alone.

For precise technical geometry, quantitative plots, or exact circuit/topology relationships, use deterministic drawing tools. Do not use generated imagery for precision-dependent claims. Programmatic output must still draw recognizable objects or meaningful spatial structure with verified handwritten lettering. Vector-first is not a blanket default, and generic flowchart or slide templates are not an acceptable fallback.

If image generation alters a label, edit/regenerate through the supported image tool; verify the repaired whole image again. If the user requested vector work, keep all text in an inspectable text layer and check its extracted content. Never claim a rendered image passed because its source text passed.

If no available renderer can meet the requested style, explain the limitation instead of substituting an unrelated aesthetic.

## Mandatory generate-review-revise loop

1. Render a candidate; retain its exact image path or image handle and its text plan.
2. Open the ACTUAL rendered image. If the file is missing, retrieve the real output before proceeding. If you cannot inspect it, mark the review blocked; a successful script exit, SVG source, OCR, or another agent's unsupported assurance cannot substitute for visual inspection.
3. Inspect the whole composition and the labels at the intended display size, including phone-size readability when relevant. Check detailed crops as needed. If a reduced preview is unreadable, enlarge lettering, shorten text, or split the scene.
4. Request an independent reviewer agent whenever available. Give it the image, user request, fact plan with sources, selected mode, text files, per-surface term/symbol manifests, and visual-review rubric. Do not pass the generator's self-rating, desired verdict, or an explanation of why it ought to pass. Require the reviewer to inspect pixels and return per-gate evidence. If delegation is unavailable, run a distinct self-review pass with the same evidence requirements and record that limitation; never claim independence.
5. Use the rubric in references/visual-review.md. Style, correctness, legibility, and vocabulary are separate PASS/FAIL/BLOCKED gates; also check the accompanying explanation against the delivery contract below. Require concrete observations tied to the current image and prose. A strong gate cannot compensate for a failed gate or missing explanation.
6. Transcribe the lettering and notation actually visible, compare it with the planned text, and check each reading surface independently under the selected mode. Review actual term-definition proximity and symbol meanings. OCR cannot certify spelling or legibility. Unreadable text is a failure, not permission to assume the intended label.
7. On failure, name the visible defect, revise its cause, and render again. For a style failure, redesign the scene rather than merely changing a font or color. Recheck all gates after every revision.
8. Use a default budget of four candidates. Return only a candidate that passed ALL gates. If the budget is exhausted, simplify and test again only when a concrete fix is evident; otherwise report the unmet requirement in allowed words. Never label the least-bad failing draft as completed. Show a failing draft only if the user explicitly asks.
9. The parent agent must open the final candidate itself, read the review findings, and resolve any contradictions. Keep a small internal record identifying the exact artifact (path plus SHA-256 for a local image), review evidence, and fixes. Any later edit invalidates that review.

Do not include internal reports or scores in the finished explanation unless asked. Follow platform rules for image previews and persistence; do not promise invisible drafts if the renderer automatically displays intermediate images.

## Deliver

Return the passing image AND an accompanying explanation by default, not just an optional caption. Unless the user explicitly asks for a different format, include these text elements in order:

1. **Title:** a short, clear title in allowed words, written as text outside the image even if the picture also has a title.
2. **Introduction:** one complete sentence introducing the subject or central question.
3. **Fundamentals:** one to three complete sentences explaining the core mechanism or relationship and how to read the picture. Use enough detail for a new reader to follow why or how it works; do not merely repeat labels or list what is drawn.
4. **Conclusion:** one complete closing sentence giving the main takeaway or its significance.

Use short paragraphs rather than explicit "Introduction", "Fundamentals", or "Conclusion" headings. The result is a title plus three to five explanatory sentences; do not force the body into a one-line caption, fragments, or semicolon-packed sentences. Keep the full explanation outside the image so that readable image labels can remain brief. The image may appear before or between the prose blocks as the platform permits, but it cannot replace them; respect platform-specific display rules.

Include meaningful conceptual limits and necessary definitions in the fundamentals or conclusion without sacrificing the explanation. The title follows the selected mode, including nearby definitions for specialist terms. Prefer a core-word title when defining a specialist title would make the introduction awkward. Use the full three fundamentals sentences when needed; narrow the picture's scope or split into explained panels rather than overloading sentences or removing essential science. Keep text and drawing mutually consistent; do not let an analogy imply a literal mechanism. Check the title and every prose sentence with the same bundled checker, and review meaning and structure before delivery. Do not add unchecked delivery prose after the final check.

## Commands

Resolve SKILL_DIR to this installed folder, which may be renamed by installation:

```bash
python3 "$SKILL_DIR/scripts/check_words.py" --lookup inference stochastic attention
python3 "$SKILL_DIR/scripts/check_words.py" /absolute/path/to/image-text.txt --mode research --terms /absolute/path/to/image-terms.json --symbols /absolute/path/to/image-symbols.json --json
python3 "$SKILL_DIR/scripts/check_words.py" /absolute/path/to/prose.md --mode research --terms /absolute/path/to/prose-terms.json --symbols /absolute/path/to/prose-symbols.json --json
python3 "$SKILL_DIR/scripts/check_words.py" /absolute/path/to/image-text.txt --mode undergraduate-strict --json
python3 "$SKILL_DIR/scripts/check_words.py" /absolute/path/to/image-text.txt --mode classic --json
```

Omit unnecessary manifests. Repeat the chosen mode for both surfaces. Classic rejects both manifests; undergraduate-strict rejects term manifests but allows explained symbols. Omitting `--mode` selects research.

The checker proves lexical membership and declared-definition placement, not meaning, style, spatial proximity, or legibility. For maintenance, run scripts/test_check_words.py and scripts/test_diagram_contract.py. The core, its manifest, curation, licenses, sense notes and scripts/check_words.py are copied unchanged from Thing Explainer v2. The pinned scripts/build_core.py is for authorized vocabulary maintenance only; never rebuild, resize or weaken the core during explanation generation.
