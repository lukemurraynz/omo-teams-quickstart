---
last_verified: "2026-05-30"
---

# Action: Tally Votes

Compute the final outcome from all cast votes, apply quorum rules, and write the outcome report.

## Prerequisites

- All required voters have a vote file in `.arb/votes/` with a non-pending vote.
- Or `quorum.allow_partial: true` is set in config.
- Python 3.10+ and PyYAML are available.

## Steps

### 1. Check quorum first (non-destructive)

Before finalizing, confirm quorum is met:

```bash
python .github/skills/arb-vote/scripts/check_quorum.py .arb/config.yml
```

If any required voter is still pending, chase them before proceeding. Exit code 1 means quorum is not met.

### 2. Run the tally

```bash
python .github/skills/arb-vote/scripts/tally_votes.py .arb/config.yml
```

The script:
1. Reads `config.yml` for voter list and quorum rules.
2. Reads every `votes/<name>.md` file.
3. Validates `vote:` fields (rejects invalid values).
4. Applies the quorum formula.
5. Determines outcome: `approved` / `rejected` / `deadlock` / `insufficient-quorum`.
6. Writes `.arb/arb-outcome.md`.

### 3. Dry-run mode (preview without writing)

```bash
python .github/skills/arb-vote/scripts/tally_votes.py .arb/config.yml --dry-run
```

Prints the outcome to stdout without writing the outcome file. Use to preview before committing.

### 4. Review the outcome file

```bash
cat .arb/arb-outcome.md
```

Verify:
- The `outcome:` frontmatter field is correct.
- The vote table lists every voter with their actual vote.
- The quorum check section shows ✓ for all requirements met.
- The next-steps section matches the outcome.

### 5. Act on the outcome

| Outcome | Action |
|---------|--------|
| `approved` | Merge the PR, archive votes to `votes/archive/`, close ARB ticket |
| `rejected` | Do not merge; review rejection rationales; revise and re-initiate |
| `insufficient-quorum` | Chase pending voters; re-run tally when all have voted |
| `deadlock` | Follow [Escalate Deadlock](escalate-deadlock.md) |

### 6. Commit the outcome

```bash
git add .arb/arb-outcome.md
git commit -m "arb: outcome for ADR-2026-001 — [approved|rejected|deadlock]"
```

## Exit codes for CI use

| Code | Meaning |
|------|---------|
| `0` | Approved |
| `1` | Rejected |
| `2` | Insufficient quorum |
| `3` | Deadlock |
| `4` | Config/file error |

Use in a GitHub Actions workflow to gate merges on approval:

```yaml
- name: Tally ARB votes
  run: python .github/skills/arb-vote/scripts/tally_votes.py .arb/config.yml
  # Fails (non-zero exit) on anything other than approved
```

## What to do if a vote file is invalid

If `tally_votes.py` warns about an invalid vote value, the affected file must be corrected by the voter:

1. Voter updates their file with a valid `vote:` value.
2. Voter commits the corrected file.
3. Re-run the tally.

Do not correct another voter's file on their behalf.
