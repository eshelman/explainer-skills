---
name: thing-explainer-diagrams
description: Explain hard subjects through original XKCD-inspired black-ink schematic drawings and short hand-lettered labels, using the complete Thing Explainer word list. Use for Thing Explainer diagrams, illustrated explanations, and explanatory comics. Require rendered-image review for style, correctness, legibility, and vocabulary before delivery.
---

# Thing Explainer Diagrams

Create an original explanatory drawing with the visual grammar the user requested from XKCD and Thing Explainer: thin black ink on white, simple recognizable objects, expressive stick figures when useful, hand-lettered notes, and drawings that explain through action and spatial relationships. Preserve causal accuracy and the complete simple-word constraint.

Treat style as a requirement, not optional decoration. A corporate infographic with wobbly boxes fails. A generic flowchart with a stick figure pasted beside it also fails. Do not copy a published panel, trace an existing composition, sign as the artist, or imply authorship by Randall Munroe.

Read [references/visual-review.md](references/visual-review.md) before planning and before reviewing. The complete vocabulary is bundled; no other skill must be installed.

## Vocabulary contract

- Read the entire [references/words.txt](references/words.txt) before drafting. It is the sole allowlist: all 3,634 official expanded spellings, including inflections; 3,616 entries after apostrophe normalization. See [references/source.json](references/source.json) for provenance.
- Apply it to ALL authored reader-facing explanation text: image lettering, title, dialogue, captions, alt text, accompanying prose, caveats, source-link labels, progress notes, and final sign-off. Never move jargon outside the image to evade the rule. Internal plans, code, reviewer reports, and this skill's instructions are exempt.
- Use exact list membership after lowercasing and normalizing apostrophes. Do not infer stems, add inflections, disguise a word through hyphens, or use digits, formulas, acronyms, or technical names as an escape. Draw arrows and objects normally; the text checker need not accept drawing geometry.
- Use short functional names that preserve meaning. Do not turn everything into unnamed boxes. Spell numbers with allowed words.
- Keep a plain UTF-8 file containing only the exact intended visible image text, in reading order. Keep any accompanying prose in a separate file. Validate both with the bundled checker before rendering and after every text revision.
- Use simple Markdown evidence links such as [Read more here](https://example.org). Only their nonvisible destinations are exempt. Source-supported limits must survive simplification.
- Never weaken the list or checker. If necessary detail cannot be conveyed honestly with these words, narrow the explanation or state the limitation in allowed words.

## Plan a drawing, not a page layout

1. Understand the subject first; check primary sources for uncertain or current claims. Keep an internal fact plan listing the mechanism, relationships, analogy mappings, and relevant limits.
2. Choose one central question and the simplest scene that lets the reader SEE its answer. Use a cutaway, a before/after pair, or two to three small scenes when useful.
3. Describe what each object DOES before writing its label. Draw the object or an explicitly marked analogy: e.g., workers waiting at a doorway, slips of paper moving between readers, a pot over a flame, or a telescope pointed at a path of light. An object-shaped drawing is not evidence that the analogy is true.
4. Apply the label-hiding test: with every word hidden, the drawing must still communicate a meaningful action, relationship, comparison, or obstruction. Labeled rectangles connected by arrows usually fail this test.
5. Prefer a few short callouts close to objects over section headings and paragraphs. Aim for under eighty visible words on a single image; reduce scope or split into panels when the subject needs more. This target applies only to image lettering, not the accompanying explanation. Do not overcompress into misleading labels.
6. Write the exact text list and run the vocabulary checker before rendering. Keep the technical fact plan out of the image-text file.

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
4. Request an independent reviewer agent whenever available. Give it the image, user request, fact plan with sources, checked text files, and visual-review rubric. Do not pass the generator's self-rating, desired verdict, or an explanation of why it ought to pass. Require the reviewer to inspect pixels and return per-gate evidence. If delegation is unavailable, run a distinct self-review pass with the same evidence requirements and record that limitation; never claim independence.
5. Use the rubric in references/visual-review.md. Style, correctness, legibility, and vocabulary are separate PASS/FAIL/BLOCKED gates; also check the accompanying explanation against the delivery contract below. Require concrete observations tied to the current image and prose. A strong gate cannot compensate for a failed gate or missing explanation.
6. Transcribe the lettering actually visible, compare it with the planned text, and check the transcription. OCR can assist but cannot certify spelling or legibility. Unreadable text is a failure, not permission to assume the intended label.
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

Include meaningful conceptual limits in the fundamentals or conclusion without sacrificing the explanation. Keep text and drawing mutually consistent; do not let an analogy imply a literal mechanism. Check the title and every prose sentence with the same bundled vocabulary checker, and review both meaning and the required structure before delivery. Do not add unchecked delivery prose after the final vocabulary check.

## Commands

Resolve SKILL_DIR to this installed folder, which may be renamed by installation:

```bash
python3 "$SKILL_DIR/scripts/check_words.py" --list
python3 "$SKILL_DIR/scripts/check_words.py" /absolute/path/to/image-text.txt --json
python3 "$SKILL_DIR/scripts/check_words.py" /absolute/path/to/caption.md --json
```

The checker proves vocabulary membership, not meaning, style, or legibility. Test checker changes with scripts/test_check_words.py; never alter its acceptance rules to make an image pass.
