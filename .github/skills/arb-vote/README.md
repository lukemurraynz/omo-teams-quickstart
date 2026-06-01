# ARB Vote Skill

Run a structured Architecture Review Board vote entirely from Markdown files.

## What's in this skill

| Path | Purpose |
|------|---------|
| `SKILL.md` | Master specification, decision map, non-negotiable rules |
| `templates/arb-config.yml` | Copy to `.arb/config.yml` and fill in voters and quorum |
| `templates/phase-gates/` | Per-gate config templates for the OMO 5-phase lifecycle |
| `templates/vote-record.md` | Per-voter vote file (auto-generated) |
| `templates/arb-outcome.md` | Outcome report (auto-generated) |
| `scripts/create_vote.py` | Create vote files from config |
| `scripts/tally_votes.py` | Tally votes and write outcome |
| `scripts/check_quorum.py` | Check quorum status without finalizing |
| `actions/` | Step-by-step procedures for each phase |
| `standards/` | Quorum rules, voter roles, escalation policy |
| `prompts/` | Copilot prompt fragments |

## Quick start

**1. Configure voters**

For a standalone ARB vote, copy the general template:

```bash
mkdir .arb
cp .github/skills/arb-vote/templates/arb-config.yml .arb/config.yml
# Edit .arb/config.yml — add voters, set quorum thresholds
```

For a phase gate in the OMO 5-phase lifecycle, copy the matching gate template:

```bash
# Phase 1 → 2 example: architecture sign-off
cp .github/skills/arb-vote/templates/phase-gates/phase1-architecture.yml .arb/config.yml
```

Available phase-gate templates: `phase0-intake`, `phase1-architecture`, `phase2-build`, `phase3-validate`, `phase4-prod`.

**2. Create vote files**

```bash
python .github/skills/arb-vote/scripts/create_vote.py .arb/config.yml
# Creates .arb/votes/<name>.md for each voter
```

**3. Each voter casts their vote**

Edit `.arb/votes/<your-name>.md` and change `vote: pending` to:
- `vote: approve`
- `vote: reject` (add rationale below)
- `vote: abstain`

Commit the file.

**4. Check quorum status (at any time)**

```bash
python .github/skills/arb-vote/scripts/check_quorum.py .arb/config.yml
```

**5. Tally and finalize**

```bash
python .github/skills/arb-vote/scripts/tally_votes.py .arb/config.yml
# Writes .arb/arb-outcome.md
# Exit 0=approved, 1=rejected, 2=insufficient-quorum, 3=deadlock
```

## When to use this skill

- An ADR (Architecture Decision Record) requires formal sign-off before merging
- A cross-team change needs approval from multiple architecture stakeholders
- An organization's governance policy mandates a recorded vote before a major design change
- You need an auditable paper trail of who approved what and when
- You are running an OMO 5-phase governance gate and need a phase-appropriate voter set
- A proposal involves AI agents or LLMs and requires an AI Ethics / RAI voter

## When *not* to use this skill

- Informal peer review (use a standard PR review instead)
- Single-approver sign-off (a PR approval is sufficient)
- Lightweight team decisions that don't require governance audit trails

## Definition of done

- [ ] `.arb/config.yml` exists with all required voters and quorum rules filled in
- [ ] All required voters have a vote file in `.arb/votes/`
- [ ] All required voters have cast a non-pending vote
- [ ] Quorum is met per config thresholds
- [ ] `tally_votes.py` has written `.arb/arb-outcome.md`
- [ ] Outcome file is committed to the branch
- [ ] If deadlocked: escalation owner has been notified per `standards/escalation-policy.md`

## Versioning

Current version: **1.0.0** - 2026-05-30. See [CHANGELOG.md](CHANGELOG.md).
