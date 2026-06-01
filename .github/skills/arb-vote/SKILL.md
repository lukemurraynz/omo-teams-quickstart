---
name: arb-vote
description: >-
  Manages the Architecture Review Board (ARB) voting workflow: defines required/optional
  voters from project config, creates per-member vote files, tallies results, enforces
  quorum rules, and escalates deadlocks. Works entirely from Markdown files and YAML
  config - no external service required.
compatibility: Python 3.10+ for scripts; any Markdown editor for manual workflow
last_verified: "2026-05-30"
---

# ARB Vote Skill

## Anti-Hallucination Rule (MANDATORY)

- **NEVER invent voter names, roles, or email addresses.** Read them exclusively from `.arb/config.yml` in the project root.
- **NEVER fabricate vote outcomes.** Always run `scripts/tally_votes.py` or read all `votes/*.md` files before reporting results.
- **NEVER assume quorum is met** without computing it. Always run `scripts/check_quorum.py` or count explicitly.
- **NEVER modify a voter's `votes/<name>.md` file on their behalf.** Vote casting is the voter's own act.
- **NEVER escalate without first reading** `arb.deadlock.escalate_to` in the project config.
- **NEVER produce an outcome when votes are pending** for required voters unless `quorum.allow_partial` is explicitly `true` in config.

## What This Skill Does

| Task | Action Document | Script |
|------|----------------|--------|
| Initialize a vote session | [create-vote](actions/create-vote.md) | `scripts/create_vote.py` |
| Cast an individual vote | [cast-vote](actions/cast-vote.md) | edit `votes/<name>.md` |
| Tally and finalize outcome | [tally-votes](actions/tally-votes.md) | `scripts/tally_votes.py` |
| Check quorum status (non-final) | - | `scripts/check_quorum.py` |
| Escalate a deadlocked vote | [escalate-deadlock](actions/escalate-deadlock.md) | output from tally |

## Non-Negotiable Rules

1. **Config is the single source of truth.** All voter lists, quorum thresholds, and escalation paths come from `.arb/config.yml`. Never hard-code them.
2. **Required voters must all vote** before an outcome is final, unless `quorum.allow_partial: true` is set.
3. **Reject votes require written rationale.** A `vote: reject` with a blank or absent rationale body is invalid; treat it as pending.
4. **Outcomes are immutable.** Once `arb-outcome.md` is written and committed, do not edit vote files. Open a new ARB round instead.
5. **Abstain does not count toward approval or rejection.** It counts toward quorum participation only if `quorum.count_abstain: true`.
6. **Deadlock is not a failure.** Escalate per `standards/escalation-policy.md` - do not invent a resolution.
7. **Timestamps are UTC ISO-8601.** All `voted_at` fields must be `YYYY-MM-DDTHH:MM:SSZ`.
8. **Optional voters' rejections are advisory.** They are recorded and surfaced in the outcome but do not override required-voter approval.

## Decision Map

| Situation | Outcome | Next Action |
|-----------|---------|-------------|
| All required voters approved, threshold met | **Approved** | Write outcome, merge |
| Any required voter rejected | **Rejected** | Write outcome, do not merge |
| Quorum not met - pending votes remain | **Insufficient Quorum** | Chase pending voters |
| Votes tied; neither threshold reached | **Deadlock** | Escalate per config |
| Optional voter rejects; required voters approve | **Approved** (with dissent noted) | Log optional dissent in outcome |
| `allow_partial: true`, enough required voted | Evaluate with who voted | Run tally with `--allow-partial` |

## Vote State Machine

```
pending → approve
        → reject   (rationale required)
        → abstain
```

Once a vote file is committed with a non-pending state, it is final for that round. To change a vote, the voter must explicitly update the file before `tally_votes.py` is run for the final time.

## Quorum Formula

```
quorum_met = (required_voted >= min_required_voters)
          AND (counted_votes >= min_total_votes)

counted_votes = approve_count + reject_count
              + (abstain_count if count_abstain else 0)

outcome = "approved"   if approve / counted >= approval_threshold
outcome = "rejected"   if reject  / counted >= approval_threshold
outcome = "deadlock"   if neither threshold reached (and quorum met)
```

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/create_vote.py` | Create `votes/<name>.md` for every voter | `python scripts/create_vote.py .arb/config.yml` |
| `scripts/tally_votes.py` | Read all votes, apply quorum, write outcome | `python scripts/tally_votes.py .arb/config.yml` |
| `scripts/check_quorum.py` | Report status without finalizing | `python scripts/check_quorum.py .arb/config.yml` |

Exit codes for `tally_votes.py`: `0` approved · `1` rejected · `2` insufficient quorum · `3` deadlock · `4` error.

## Standards

- [Quorum Rules](standards/quorum-rules.md) - thresholds, counting logic, edge cases
- [Voter Roles](standards/voter-roles.md) - required vs optional, role definitions
- [Vote States](standards/vote-states.md) - valid states and transition rules
- [Escalation Policy](standards/escalation-policy.md) - deadlock and override procedures

## Actions

- [Create Vote](actions/create-vote.md) - initialize a new ARB vote session
- [Cast Vote](actions/cast-vote.md) - record an individual vote
- [Tally Votes](actions/tally-votes.md) - compute final outcome
- [Escalate Deadlock](actions/escalate-deadlock.md) - escalation procedure

## Prompts

- [Initiate ARB Vote](prompts/initiate-arb-vote.prompt.md)
- [Tally ARB Vote](prompts/tally-arb-vote.prompt.md)

## Templates

### General
- [arb-config.yml](templates/arb-config.yml) - copy to `.arb/config.yml` and fill in
- [vote-record.md](templates/vote-record.md) - individual vote file (generated by script)
- [arb-outcome.md](templates/arb-outcome.md) - outcome report (generated by tally script)

### Phase-Gate Templates (for OMO 5-phase lifecycle)

Copy the matching template for your current governance gate:

| Gate | Template | Key Voters |
|------|----------|------------|
| Phase 0 → 1 | [phase0-intake.yml](templates/phase-gates/phase0-intake.yml) | Product Owner, Cloud Economics |
| Phase 1 → 2 | [phase1-architecture.yml](templates/phase-gates/phase1-architecture.yml) | Principal Architect, Security Lead, Product Owner |
| Phase 2 → 3 | [phase2-build.yml](templates/phase-gates/phase2-build.yml) | Principal Architect, Product Owner |
| Phase 3 → 4 | [phase3-validate.yml](templates/phase-gates/phase3-validate.yml) | Security Lead, Product Owner, Cloud Economics |
| Phase 4 → Prod | [phase4-prod.yml](templates/phase-gates/phase4-prod.yml) | Product Owner, Security Lead, Cloud Economics |

```bash
# Example: copy the architecture gate template
cp .github/skills/arb-vote/templates/phase-gates/phase1-architecture.yml .arb/config.yml
```

## File Layout

```
.arb/
├── config.yml          # Project ARB configuration (voters, quorum, deadlock)
├── votes/
│   ├── alice.md        # Vote file per voter (created by create_vote.py)
│   ├── bob.md
│   └── carol.md
└── arb-outcome.md      # Final outcome (written by tally_votes.py)
```
