# Explainer Skills

Reusable Codex skills for explaining difficult subjects clearly.

## For total beginners

Copy and paste this into your AI chat window:

```text
Please install the skills from https://github.com/eshelman/explainer-skills
```

Then try one of the prompts below.

## Included skills

- [`thing-explainer`](skills/thing-explainer/): explains hard things with small words and checks each word.
- [`progressive-disclosure`](skills/progressive-disclosure/): explains dense scientific, technical, and philosophical material through progressively deeper layers.
- [`thing-explainer-diagrams`](skills/thing-explainer-diagrams/): explains hard subjects with original black-ink schematic drawings, simple labels, and a rendered-image review loop.

## Try it

### Thing Explainer

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

### Progressive Disclosure

- Use the `progressive-disclosure` skill on mixture of experts versus diffusion language models.
- Use the `progressive-disclosure` skill on DNA methylation.
- Use the `progressive-disclosure` skill on what an AI agent is.
- Use the `progressive-disclosure` skill on emergent capability in AI.
- Use the `progressive-disclosure` skill on Goodhart's law.
- Use the `progressive-disclosure` skill on the ontology of thought.

### Thing Explainer Diagrams

- Use the `thing-explainer-diagrams` skill on mixture of experts.
- Use the `thing-explainer-diagrams` skill on how a transformer operates.
- Use the `thing-explainer-diagrams` skill on dark matter.
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
