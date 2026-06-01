# Changelog - governance-gate

## 1.0.0 - 2026-05-30

Initial release.

### Added
- **SKILL.md.** Gate readiness checklist template (evidence inventory, ADR gate check, risk gate check, security gate check, WAF gate check, economics gate check), outcome format (APPROVED/CONDITIONAL/REJECTED with vote table and tally), CONDITIONAL revision cycle procedure, audit trail requirements, and phase-specific gate requirements table.
- Anti-hallucination rules: never approve without full checklist, never invent evidence, never produce vague CONDITIONAL revisions, never allow phase progression after REJECTED.
- Outcome immutability: re-reviews produce `outcome-v2.md` rather than editing committed outcomes.
- CONDITIONAL revision cycle: explicit 6-step process from revision assignment through re-approval or reversion to REJECTED.
