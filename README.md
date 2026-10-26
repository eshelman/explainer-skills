# Explainer Skills

Reusable Codex skills for explaining difficult subjects clearly.

## For total beginners

Copy and paste this into your AI chat window:

```text
Please install the skills from https://github.com/eshelman/explainer-skills
```

Then try one of the prompts below.

## Included skills

- [`thing-explainer`](skills/thing-explainer/): v2 explains complex research with a checked 15,000-lemma undergraduate vocabulary, defined technical terms, and explained notation; research mode is the default.
- [`progressive-disclosure`](skills/progressive-disclosure/): explains dense scientific, technical, and philosophical material through progressively deeper layers.
- [`thing-explainer-diagrams`](skills/thing-explainer-diagrams/): v2 explains science with original black-ink schematic drawings, a 15,000-lemma vocabulary, defined technical terms, and a rendered-image review loop; research mode is the default.

## Try it

### Thing Explainer

Thing Explainer v2 defaults to **research** mode: it uses the embedded 15,000-lemma general undergraduate core (34,154 accepted forms), introduces necessary specialist terms with definitions near first use, and permits numbers, equations, units, and explained symbols. The checker runs locally with Python’s standard library; no vocabulary download is needed.

Request **undergraduate-strict** mode for core vocabulary without specialist-term exceptions, or **classic** mode for the original ten-hundred-word restriction. The broader core is provisional: it uses frequency, dictionary morphology, and editorial curation, and is not a measured guarantee of undergraduate familiarity. Provenance, licenses, and a reproducible builder are bundled with the skill.

- Use the `thing-explainer` skill on mixture of experts.
- Use the `thing-explainer` skill on KV cache.
- Use the `thing-explainer` skill on how a semiconductor fab makes chips.
- Use the `thing-explainer` skill on reward hacking.
- Use the `thing-explainer` skill on Jevons paradox.
- Use the `thing-explainer` skill on recursive self-improvement.
- Use the `thing-explainer` skill on dark matter.
- Use the `thing-explainer` skill on dark energy.
- Use the `thing-explainer` skill on DNA methylation.
- Use the `thing-explainer` skill on why onions become sweet when cooked.
- Use the `thing-explainer` skill in undergraduate-strict mode on autoencoders.
- Use the `thing-explainer` skill in classic mode on dark matter.

### Progressive Disclosure

- Use the `progressive-disclosure` skill on mixture of experts versus diffusion language models.
- Use the `progressive-disclosure` skill on DNA methylation.
- Use the `progressive-disclosure` skill on what an AI agent is.
- Use the `progressive-disclosure` skill on emergent capability in AI.
- Use the `progressive-disclosure` skill on Goodhart's law.
- Use the `progressive-disclosure` skill on the ontology of thought.

### Thing Explainer Diagrams

Research mode uses the embedded 15,000-lemma general undergraduate core from Thing Explainer v2, with necessary specialist terms defined near first use and mathematical notation explained. Image labels and accompanying prose are checked separately; a technical label needs a readable definition in the image itself. The skill is self-contained and does not require the text-only skill to be installed.

Each picture comes with a title, an introductory sentence, one to three sentences explaining the fundamentals, and a closing conclusion. Style, scientific correctness, phone-size legibility, vocabulary, and the accompanying explanation are reviewed before delivery.

Request **undergraduate-strict** mode for the core vocabulary without specialist-term exceptions, or **classic** mode for the original ten-hundred-word restriction. The broader core is provisional, not a measured guarantee of undergraduate comprehension; its provenance and reuse notices are bundled with the skill.

- Use the `thing-explainer-diagrams` skill on mixture of experts.
- Use the `thing-explainer-diagrams` skill on how a transformer operates.
- Use the `thing-explainer-diagrams` skill on dark matter.
- Use the `thing-explainer-diagrams` skill on autoencoders.
- Use the `thing-explainer-diagrams` skill in classic mode on dark matter.
- Use the `thing-explainer-diagrams` skill on why adding more cooks may not make dinner ready sooner.

## Repository layout

Add future skills as separate directories under `skills/`:

```text
skills/
├── progressive-disclosure/
├── thing-explainer/
└── thing-explainer-diagrams/
```

Each skill directory should contain its own `SKILL.md` and any supporting
scripts, references, or assets it needs.
