# Visual review contract

Judge an original XKCD-inspired explanatory drawing under the selected Thing
Explainer v2 mode: research by default, undergraduate-strict or classic on request.
Inspect the image itself before judging it. Do not infer success from file creation,
source code, the prompt, or the generator's report. Be willing to reject it.

## Style: all required

- Thin black ink and generous white space dominate; lettering feels drawn by hand.
- At least one recognizable scene, object interaction, cutaway, or spatial mechanism
  teaches the subject. Objects can be simple, but not interchangeable labeled cards.
- With labels hidden, there is still a meaningful action or relationship to describe.
- The composition reads as an explanatory cartoon or annotated drawing at a glance.
  Small relevant plots or boxes are fine; a business infographic with jitter is not.
- No corporate heading system, decorative palette, large filled cards, dashboard
  layout, or decision-flow template dominates the image.

Do not require stick figures in an explanation about stars, molecules, or machines.
When people appear, their actions must help explain. Do not reward decorative people.
Do not equate "unpolished" with unreadable, careless, or factually vague.

## Correctness: all required

- The mechanism and direction of each meaningful relationship match the fact plan.
- Geometry and grouping do not introduce a false causal claim or numerical precision.
- Distinguish literal mechanism from analogy; a pictured door is not a literal part
  of a computer unless the explanation is actually about a physical door.
- Distinguish known facts, proposed uses, hopes, and unknowns where relevant.
- Reject a scientifically false claim even if the picture is excellent.
- Check that technical terms retain their scientific meaning and that definitions
  teach the relevant distinction. Explain specialist senses of familiar core words.
- Check quantities, units, equations, symbol meanings and assumptions against the
  fact plan. A lexical pass does not verify mathematics or a causal claim.
- If sources or necessary topic context are absent, mark this gate BLOCKED instead
  of guessing. A style-only audit may leave other gates BLOCKED.

## Legibility: all required

- Read every word in the delivered image; inspect small-screen scale as applicable.
- No clipping, collisions, ambiguous arrow endpoints, tiny caveats, or faint text.
- Handwriting is coherent and easy to read, not pseudo-text or merely a tiny accent.
- Reading order is evident, and objects retain recognizable shapes.
- If text requires heavy zoom, reduce the amount of text or split the panels.
- Inspect a whole-image preview at about 390 pixels wide for phone delivery.
  Aim for the smallest lettering to read like roughly fourteen-pixel text there;
  a magnified crop alone cannot clear a small-screen failure.

## Vocabulary: all required

- Transcribe every visible word, including stray marks that look like lettering.
- Compare the transcription with the approved text list; report missing, extra, or
  altered words. Natural line breaks may differ without changing meaning.
- Record the mode. Research uses the fixed 15,000-lemma core plus necessary defined
  topic terms and explained notation; undergraduate-strict rejects topic-term
  exceptions; classic uses the original list and rejects term/symbol manifests.
- Run the bundled checker independently on the actual image transcription and
  complete accompanying explanation, with only the manifests used on each surface.
- Verify that image terms have their canonical form and exact core-only definitions
  visibly near first use in the image, not only in the prose or alt text. Check the
  250-character definition placement rule and actual spatial proximity. Repeated
  terms do not need repeated definitions within one surface.
- Require readable symbol meanings on each surface where symbols occur; inspect
  units, acronyms and familiar words with specialist senses even if accepted.
- Do not silently add definitions to the transcript that are absent from the image.
- Do not assume a correct text plan guarantees correct rendered lettering.

## Review response

Before delivery, also check the accompanying explanation (unless the user explicitly
requested a different format): a text title outside the image, one introductory
sentence, one to three sentences explaining the fundamentals, and one closing
conclusion sentence. Require complete sentences that teach the core mechanism or
relationship, not fragments or a list of image labels. Check accuracy, agreement
with the drawing, relevant limits, and vocabulary across the whole explanation.
A passing picture with an absent or caption-only explanation is not a complete
delivery. For an explicitly scoped image-only audit, mark prose not assessed and
do not claim the complete delivery passed.

Return a short internal report with:

- artifact identity: exact path/handle and SHA-256 when locally available;
- inspected: yes/no and how you viewed it;
- each gate: PASS, FAIL, or BLOCKED, with concrete observations;
- label-hiding test: one sentence describing what the drawing communicates;
- actual image transcription and any discrepancies;
- selected mode, per-surface checker results, and term-definition/symbol checks;
- accompanying explanation: PASS, FAIL, or BLOCKED, with sentence counts and any
  content or vocabulary defects (or not assessed for an image-only audit);
- required fixes, ordered by severity;
- overall: PASS only if every gate and the required accompanying explanation passed
  on this exact artifact and text; clearly label image-only audit results as such.

An unchecked or unviewable gate is BLOCKED. Do not average gates or write "all pass"
without image-specific evidence. The generator must revise any failure and obtain a
fresh review. Four attempts is a work budget, not permission to ship a failure.

## Calibration examples

These are behavioral distinctions, not templates to copy.

- A tall white page with green section markers, bold sans-serif headings, pale
  rounded boxes, bar charts, decision diamonds, and paragraphs fails STYLE even
  if some borders are uneven and every word is allowed.
- A line of actual drawn workers carrying pieces toward a doorway, with the front
  worker visibly blocking entry and a hand-lettered note nearby, can pass STYLE.
  Still check that the doorway's role is an honest analogy and that labels are readable.
- A lovely pencil sketch with unreadable labels fails LEGIBILITY.
- A monochrome drawing with the wrong arrow direction fails CORRECTNESS.
- A correctly drawn mechanism with one forbidden caption word fails VOCABULARY.
- A research-mode picture labeled with an undeclared specialist term fails
  VOCABULARY even if the accompanying prose explains it. A declared term with its
  readable adjacent definition can pass; research vocabulary is not a style failure.
- A definition that passes lexical checks but misstates the science fails CORRECTNESS.
- A tiny definition fails LEGIBILITY even when its text passes the checker.
- A schematic with no people may pass STYLE through meaningful drawn objects and
  annotation. Do not add a stick figure just to tick a box.
