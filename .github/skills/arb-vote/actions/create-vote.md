---
last_verified: "2026-05-30"
---

# Action: Create Vote

Initialize a new ARB vote session by creating a vote file for every voter defined in `.arb/config.yml`.

## Prerequisites

- `.arb/config.yml` exists and has at least one entry in `arb.required_voters`.
- Python 3.10+ is available.
- PyYAML is installed (`pip install pyyaml`).

## Steps

### 1. Verify config exists

```bash
cat .arb/config.yml
```

Confirm `arb.proposal`, `arb.required_voters`, and `arb.quorum` are present. If config does not exist, copy the template:

```bash
mkdir -p .arb
cp .github/skills/arb-vote/templates/arb-config.yml .arb/config.yml
# Edit .arb/config.yml with your voters and thresholds
```

### 2. Run create_vote.py

```bash
python .github/skills/arb-vote/scripts/create_vote.py .arb/config.yml
```

Expected output:

```
Proposal: ADR-2026-001: Migrate auth to managed identity
Votes directory: .arb/votes

Created (3):
  + votes/alice.md
  + votes/bob.md
  + votes/carol.md

Total voters: 3 (3 created, 0 skipped)
```

### 3. Review created files

Each `votes/<name>.md` contains:
- Frontmatter with `vote: pending` and the voter's role
- Instructions for the voter on how to cast their vote
- A `## Rationale` section (required on reject)

### 4. Notify voters

Notify each voter that their vote file has been created. Share the path (`votes/<name>.md`) and the tally deadline from `arb.deadlock.escalation_days`.

A suitable notification message:

> Your ARB vote for **{proposal}** is ready at `votes/{name}.md`.
> Please update `vote: pending` to `approve`, `reject`, or `abstain` and commit by **{deadline}**.
> If you reject, add your rationale under `## Rationale`.

### 5. Commit the vote files

```bash
git add .arb/
git commit -m "arb: initialize vote for {proposal}"
```

## What the script does NOT do

- It does not overwrite existing vote files (preserves previously cast votes if re-run).
- It does not send notifications - that is the vote initiator's responsibility.
- It does not validate the config beyond checking that it can be parsed.

## Next action

Once all required voters have cast their votes: [Tally Votes](tally-votes.md).
