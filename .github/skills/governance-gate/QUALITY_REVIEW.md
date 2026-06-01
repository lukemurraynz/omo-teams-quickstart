# Quality Review - governance-gate

**Version:** 1.0.0  
**Reviewed:** 2026-05-30  
**Score:** 8/10

## What works well

- Checklist template covers ADR status, risk burn-down, security, WAF, and economics in one pass. No pillar is missed.
- CONDITIONAL revision cycle is explicit: revision list → owner assignment → re-checklist → upgrade or reject. No ambiguity.
- Outcome file format has frontmatter for machine-readability alongside human narrative.
- Audit trail requirements prevent post-hoc editing of gate decisions.
- Phase-specific gate requirements call out the different thresholds per gate (Phase 0→1 vs Phase 4→Prod).

## Known gaps

- No automated checklist runner. A Python script reading from `.sisyphus/knowledge/` and `.sisyphus/evidence/` would make gate checks faster and consistent.
- WAF pillar thresholds (≥3, ≥4) are defaults. Projects should calibrate these in a project-level config.
- REJECTED gate handling is brief - the full redoing of a phase needs its own workflow guidance.
- No guidance for partial gates (e.g., approving architecture but not security, then allowing a security-only re-review).

## Intentionally excluded

- Voter management and quorum rules - covered by `arb-vote` skill.
- Risk register scoring - covered by `risk-register` skill.
- WAF assessment execution - covered by `azure-well-architected-assessment` skill.
