# Changelog

All notable changes to `arb-vote`.

## 1.1.0 - 2026-06-01

### Added

- **Extended voter roles.** Added Cloud Economics (required), Delivery Lead (optional), and AI Ethics / RAI (conditional) to `standards/voter-roles.md`.
- **Conditional roles.** New role type for voters only required in specific contexts (e.g., AI Ethics / RAI when AI agents are in scope).
- **Per-gate ARB config templates.** Five phase-gate templates under `templates/phase-gates/` matching the OMO 5-phase lifecycle: `phase0-intake`, `phase1-architecture`, `phase2-build`, `phase3-validate`, `phase4-prod`. Each pre-configures the right voter set, quorum thresholds, and escalation path for that gate.
- **Governance-gate integration.** Governance-gate SKILL.md now links to the per-gate templates and references consistent voter role names.
- **Template config extended.** General `arb-config.yml` now includes Cloud Economics and Delivery Lead as example optional voters.

### Changed

- **Voter role consistency.** Governance-gate voter references updated from "Security" to "Security Lead" to match arb-vote conventions.

## 1.0.0 - 2026-05-30

Initial release.

### Added

- **SKILL.md.** Master specification with anti-hallucination rules, decision map, quorum formula, and non-negotiable rules.
- **`scripts/create_vote.py`.** Creates `votes/<name>.md` per voter from config; skips existing files to preserve cast votes. Exit code 0 on success, 1 on config error, 2 if no voters defined.
- **`scripts/tally_votes.py`.** Reads all vote files, applies quorum rules, determines outcome (approved / rejected / deadlock / insufficient-quorum), writes `arb-outcome.md`. Exit codes 0–4 for CI gate use.
- **`scripts/check_quorum.py`.** Non-finalizing quorum status report with per-voter icons. Exit 0 if quorum met, 1 if not.
- **`templates/arb-config.yml`.** Project config template covering voter lists (required/optional), quorum thresholds, and deadlock escalation.
- **`templates/vote-record.md`.** Individual vote file template with frontmatter fields and guidance.
- **`templates/arb-outcome.md`.** Outcome report template with tally table, quorum check, and next-steps section.
- **`actions/create-vote.md`.** Step-by-step procedure for initializing a vote session.
- **`actions/cast-vote.md`.** Procedure for recording an individual vote.
- **`actions/tally-votes.md`.** Procedure for tallying votes and producing the outcome.
- **`actions/escalate-deadlock.md`.** Deadlock escalation procedure with checklist.
- **`standards/quorum-rules.md`.** Quorum thresholds, counting logic, and edge cases (abstain, partial quorum, concurrent edits).
- **`standards/voter-roles.md`.** Required vs optional voter definitions, role assignments, and delegation rules.
- **`standards/vote-states.md`.** Valid vote states (approve / reject / abstain / pending) and transition rules.
- **`standards/escalation-policy.md`.** When and how to escalate a deadlock, override conditions, and audit trail requirements.
- **`prompts/initiate-arb-vote.prompt.md`.** Copilot prompt fragment for starting a vote.
- **`prompts/tally-arb-vote.prompt.md`.** Copilot prompt fragment for tallying a vote.
- **`references/arb-vote-config.instructions.md`.** Guidance on writing and maintaining `.arb/config.yml`.
- **`references/workflows/arb-vote.yml`.** GitHub Actions CI workflow: runs quorum check on push, tally on manual trigger.

### Validation

- Scripts tested with PyYAML 6.x and Python 3.11 on Windows 11.
- Quorum formula verified against: unanimous approve, unanimous reject, split vote (deadlock), missing required voter (insufficient quorum), optional-only rejection.
- CI workflow exit codes verified for gate use: `tally_votes.py` exits 0 only on approval.
