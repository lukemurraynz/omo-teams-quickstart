---
last_verified: "2026-05-30"
---

# Standard: Escalation Policy

## When escalation applies

Escalation is triggered by two conditions:

| Condition | Trigger |
|-----------|---------|
| **Deadlock** | Quorum met but neither approve nor reject reached threshold |
| **Timeout** | Required voters have not voted within `escalation_days` working days |

Escalation is **not** triggered by:
- Insufficient quorum (this is a chase-voters problem, not an escalation problem)
- Optional-only rejections
- A unanimous decision in either direction

## Escalation owner

Defined in `.arb/config.yml`:

```yaml
deadlock:
  escalate_to: "CTO"                    # Role or name
  escalation_contact: "cto@example.com" # Contact address
  escalation_days: 3                    # Working days before timeout escalation
```

The escalation owner must be a named role or individual with authority to override the ARB outcome. They are not a voter - they are a tie-breaker or timeout-resolver.

## Escalation owner options

| Option | Result | Requirements |
|--------|--------|--------------|
| Override approve | `approved (escalated)` | Written rationale recorded in outcome file |
| Override reject | `rejected (escalated)` | Written rationale recorded in outcome file |
| Request re-vote | New round | Initiator revises proposal and re-creates vote session |
| Extend deadline | Deadline extended | Escalation owner sets new `escalation_days` in config |

## Mandatory audit trail

Every escalation must produce a documented trail. Required fields in `arb-outcome.md`:

```markdown
## Escalation

- Escalated to: [name or role]
- Escalated at: YYYY-MM-DDTHH:MM:SSZ
- Reason: deadlock | timeout
- Contact method: email | Slack | ticket

## Escalation Decision

- Decision: approved (escalated) | rejected (escalated) | re-vote | extended
- Decided by: [full name], [role]
- Decided at: YYYY-MM-DDTHH:MM:SSZ
- Rationale: [text]
```

Outcome without this trail is not considered complete for governance purposes.

## Timeout escalation (voter non-response)

If required voters have not voted after `escalation_days` working days:

1. Run `check_quorum.py` to confirm who is still pending.
2. Send a reminder with a 24-hour final deadline.
3. If still no response, escalate to the escalation owner.
4. The escalation owner may:
   - Set `allow_partial: true` in config and approve the tally proceeding without the absent voter.
   - Substitute a delegate (see [Voter Roles - Delegation](voter-roles.md)).
   - Cancel the vote and reschedule.

## Override conditions

An escalation owner may only override when:

1. The override is consistent with organizational ARB charter.
2. The override rationale is documented in `arb-outcome.md`.
3. The overriding party is the designated `escalate_to` owner, not another voter.

An override by anyone other than the designated escalation owner is not a valid governance outcome.

## Escalation escalation (meta-escalation)

If the escalation owner is unavailable or conflicted:

```yaml
deadlock:
  escalate_to: "CTO"
  escalation_backup: "Board Chair"   # Secondary escalation owner
```

Follow the same procedure with the backup contact. Document both attempts in the outcome file.
