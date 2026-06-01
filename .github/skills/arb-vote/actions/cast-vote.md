---
last_verified: "2026-05-30"
---

# Action: Cast Vote

Record your vote in your assigned vote file. This is done by the voter themselves - no one else should edit your vote file.

## Prerequisites

- A vote file exists at `.arb/votes/<your-name>.md` (created by the vote initiator via `create_vote.py`).
- You have write access to the branch.

## Steps

### 1. Open your vote file

```bash
# Example: if your name is alice
open .arb/votes/alice.md
```

The file starts with:

```yaml
---
voter: alice
role: Principal Architect
voter_type: required
proposal: ADR-2026-001
vote: pending
voted_at: null
---
```

### 2. Choose your vote

Replace `vote: pending` with one of:

| Value | Meaning |
|-------|---------|
| `approve` | You are in favour of the proposal |
| `reject` | You are opposed (rationale required in `## Rationale`) |
| `abstain` | You are not voting; you acknowledge the proposal exists |

### 3. Set the timestamp

Replace `voted_at: null` with the current UTC time in ISO-8601:

```yaml
voted_at: "2026-05-30T14:23:00Z"
```

### 4. Write your rationale (required for reject)

In the `## Rationale` section, explain your decision. For `reject`, this is **mandatory** - the tally script will treat a blank rationale on a rejection as an invalid vote.

Example:

```markdown
## Rationale

Rejecting because the proposal does not address credential rotation for the
service principal. Once a rotation strategy is documented in the ADR, I will
re-cast as approve.
```

### 5. Commit your vote

```bash
git add .arb/votes/alice.md
git commit -m "arb: alice votes [approve|reject|abstain] on ADR-2026-001"
```

## Rules for voting

- **Vote once.** Once you commit a non-pending vote, it is final for this round. To change your vote, update the file before the tally is run.
- **Rationale on reject is mandatory.** See [Vote States](../standards/vote-states.md).
- **Do not vote on behalf of another person.** Each voter must commit their own file.
- **Abstain does not equal approval.** It removes you from the approve/reject count; whether it counts toward quorum depends on `quorum.count_abstain` in config.

## Next action

The vote initiator monitors quorum status via:

```bash
python .github/skills/arb-vote/scripts/check_quorum.py .arb/config.yml
```

Once all required voters have voted: [Tally Votes](tally-votes.md).
