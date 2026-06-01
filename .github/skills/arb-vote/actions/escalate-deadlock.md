---
last_verified: "2026-05-30"
---

# Action: Escalate Deadlock

A deadlock occurs when quorum is met but neither `approve` nor `reject` reaches the configured approval threshold. Escalation is the formal path to resolution.

## When this action applies

`tally_votes.py` exits with code `3` and produces an outcome file with `outcome: deadlock`.

This means:
- Quorum was met (enough voters participated).
- The vote is split such that no side reached the threshold.
- A human decision-maker must break the tie.

## Escalation checklist

### 1. Confirm deadlock

```bash
python .github/skills/arb-vote/scripts/tally_votes.py .arb/config.yml --dry-run
```

Verify the outcome is `deadlock` and note the exact vote counts.

### 2. Identify the escalation owner

Read `arb.deadlock.escalate_to` from `.arb/config.yml`:

```yaml
deadlock:
  escalate_to: "CTO"
  escalation_contact: "cto@example.com"
  escalation_days: 3
```

The escalation owner is the named role or individual. Never invent an escalation owner.

### 3. Prepare the escalation brief

Draft a brief (email, ticket, or Slack message) containing:

- **Proposal:** the `arb.proposal` value from config
- **Vote counts:** approve / reject / abstain / pending
- **Voter breakdown:** who voted what (reference `arb-outcome.md`)
- **Core disagreement:** summarize the key objection from reject rationales
- **Deadline:** `today + escalation_days` working days

### 4. Notify the escalation owner

Send the brief through the appropriate channel for your organization. Attach or link `.arb/arb-outcome.md`.

### 5. Record the escalation in the outcome file

Append to `.arb/arb-outcome.md`:

```markdown
## Escalation

- Escalated to: [name/role]
- Escalated at: YYYY-MM-DDTHH:MM:SSZ
- Escalation deadline: YYYY-MM-DD
- Contact: [email/Slack/ticket]
```

Commit this addition:

```bash
git add .arb/arb-outcome.md
git commit -m "arb: escalate deadlock on ADR-2026-001 to [name]"
```

### 6. Escalation owner decides

The escalation owner has three options:

| Decision | Outcome | Action |
|----------|---------|--------|
| Override approve | `approved (escalated)` | Owner documents decision in outcome; merge proceeds |
| Override reject | `rejected (escalated)` | Owner documents decision; proposal is withdrawn |
| Request re-vote | New round | Initiator opens new vote with clarified proposal |

### 7. Record the escalation decision

Once the escalation owner decides, record it in `.arb/arb-outcome.md` under a new `## Escalation Decision` section:

```markdown
## Escalation Decision

- Decision: approved (escalated)
- Decided by: [name], [role]
- Decided at: YYYY-MM-DDTHH:MM:SSZ
- Rationale: [explanation from escalation owner]
```

Update `outcome:` in the frontmatter to `approved (escalated)` or `rejected (escalated)`.

Commit and merge (or close) accordingly.

## What NOT to do

- Do not re-run `tally_votes.py` after escalation without a new vote round.
- Do not edit individual vote files after the outcome is written.
- Do not declare approval unilaterally without the escalation owner's recorded decision.

## Reference

See [Escalation Policy](../standards/escalation-policy.md) for the full governance policy.
