---
last_verified: "2026-05-30"
---

# Standard: Quorum Rules

Quorum rules determine whether enough voters have participated for an outcome to be valid.

## Quorum formula

```
quorum_met = (required_voted >= min_required_voters)
          AND (counted_votes >= min_total_votes)
```

Where:
- `required_voted` = number of required voters who cast a non-pending vote
- `counted_votes` = approve + reject (+ abstain if `count_abstain: true`)
- `min_required_voters` = from `quorum.min_required_voters` in config (defaults to total required voters)
- `min_total_votes` = from `quorum.min_total_votes` in config (defaults to 1)

## Approval formula (applied only when quorum is met)

```
approval_rate = approve_count / counted_votes
rejection_rate = reject_count / counted_votes

outcome = "approved"  if approval_rate  >= approval_threshold
outcome = "rejected"  if rejection_rate >= approval_threshold
outcome = "deadlock"  if neither threshold is met
```

Default `approval_threshold` is `0.51` (simple majority). A two-thirds majority uses `0.67`.

## Config parameters

```yaml
quorum:
  min_required_voters: 2      # Minimum required voters who must vote (default: all)
  min_total_votes: 3          # Minimum total votes counted (default: 1)
  approval_threshold: 0.67    # Fraction of counted votes needed to approve (default: 0.51)
  count_abstain: false        # Whether abstain counts in the denominator (default: false)
  allow_partial: false        # Allow outcome before all required voters vote (default: false)
```

## Edge cases

### Required voter absent

If a required voter's file is missing or their vote is `pending`:
- `quorum_met` will be `false` unless `allow_partial: true`.
- The outcome is `insufficient-quorum`, not deadlock.
- Chase the voter or set `allow_partial: true` to proceed with those who voted.

### All required voters abstain

- `required_voted` is met (abstain counts as participation).
- `counted_votes` is 0 unless `count_abstain: true`.
- With `count_abstain: false`, outcome is `insufficient-quorum` (no approvable votes).
- With `count_abstain: true`, outcome is `deadlock` (all abstain = 0% approve and 0% reject).

### Unanimous approve

- `approval_rate = 1.0` ≥ any threshold.
- Outcome: `approved`.

### Unanimous reject

- `rejection_rate = 1.0` ≥ any threshold.
- Outcome: `rejected`.

### Tie (equal approve and reject)

- Neither side reaches `approval_threshold` (assuming threshold > 0.5).
- Outcome: `deadlock`. Escalate.

### Optional voters only

- Optional voters' votes are included in the tally.
- They do not affect the `required_voted` count.
- If only optional voters have voted and required voters are all pending, outcome is `insufficient-quorum`.

### Concurrent edits before tally

- If two voters update their files simultaneously, git merge handles conflicts.
- The tally script reads each file independently; race conditions in file creation do not affect correctness.
- Always commit vote files individually (`git add votes/<name>.md`), not all at once.

## Raising the quorum threshold

For high-stakes decisions, set a stricter threshold:

```yaml
quorum:
  min_required_voters: 3       # All three required voters must vote
  min_total_votes: 4           # At least 4 total votes
  approval_threshold: 0.75     # Three-quarter supermajority
```

## Lowering the threshold (emergency use only)

Setting `allow_partial: true` allows outcome determination even if not all required voters have voted. Use sparingly - document the reason in the outcome file.
