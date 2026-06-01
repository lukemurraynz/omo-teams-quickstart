---
last_verified: "2026-05-30"
---

# Standard: Vote States

## Valid states

| State | Frontmatter value | Meaning |
|-------|-------------------|---------|
| Pending | `pending` | Voter has not yet cast their vote |
| Approve | `approve` | Voter is in favour of the proposal |
| Reject | `reject` | Voter is opposed to the proposal |
| Abstain | `abstain` | Voter acknowledges the vote but is not casting a directional decision |

## State transitions

```
pending → approve
        → reject   (rationale body required)
        → abstain
```

There is no transition back to `pending` after a non-pending vote is committed. To change a vote, update the file before the final tally is run. Once `arb-outcome.md` is committed, the vote is immutable for that round.

## Rules per state

### `pending`

- Default state for a newly created vote file.
- Treated as "not voted" for quorum purposes.
- Required voters with `pending` votes prevent quorum from being met (unless `allow_partial: true`).

### `approve`

- Voter endorses the proposal as described.
- Rationale is optional but encouraged for traceability.
- Counted in `approve_count`.

### `reject`

- Voter opposes the proposal.
- **Rationale is mandatory.** The `## Rationale` section must contain at least one non-empty line.
- If rationale is blank, `tally_votes.py` warns and treats the vote as `pending`.
- Counted in `reject_count`.
- For required voters: any `reject` causes outcome to be `rejected` when quorum is met.
- For optional voters: recorded in outcome as advisory dissent.

### `abstain`

- Voter explicitly opts out of the directional vote.
- May count toward quorum participation (configurable via `count_abstain`).
- Does **not** count in `approve_count` or `reject_count`.
- Does not block approval if `count_abstain: false`.
- Use abstain rather than leaving a vote pending - pending implies the voter was never notified.

## Invalid states

Any value other than the four above is treated as `pending` with a warning. Common mistakes:

| Invalid value | Likely intent | Correct value |
|---------------|---------------|---------------|
| `yes` | Approval | `approve` |
| `no` | Rejection | `reject` |
| `lgtm` | Approval | `approve` |
| `nack` | Rejection | `reject` |
| `skip` | Abstention | `abstain` |

## Voted-at timestamp

- Set `voted_at` to the UTC time when the vote is cast: `"2026-05-30T14:23:00Z"`.
- Leave as `null` only if vote is `pending`.
- Timestamps are informational - they do not affect quorum or outcome logic in the tally script, but they appear in the outcome table for audit purposes.
