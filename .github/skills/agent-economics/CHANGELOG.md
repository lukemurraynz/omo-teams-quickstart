# Changelog - agent-economics

## 1.0.0 - 2026-05-30

Initial release.

### Added
- **SKILL.md.** Budget baseline format per phase (token budget, model tier ceiling, retry loops, human interventions, estimated cost), per-phase report format (budget vs actual, model breakdown, carry-forward, observations), model tier selection guide, context compaction economics, budget overrun protocol, and gate integration requirements.
- Anti-hallucination rules: never report token counts without data, never recommend a model tier without stating trade-offs, never carry over budget silently.
- 2026 model pricing reference table (Haiku, Sonnet, Opus) with $/1M input/output rates.
- Integration: gate check by cloud-economics voter at each ARB gate.
