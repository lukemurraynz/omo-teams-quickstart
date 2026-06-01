---
last_verified: "2026-05-30"
---

# Initiate ARB Vote

Use `SKILL.md` and `actions/create-vote.md` to initialize a new ARB vote.

Ask or infer:
- what is the proposal title and ID (e.g., `ADR-2026-001: Migrate auth to managed identity`)?
- who are the required voters (names and roles)?
- who are the optional voters, if any?
- what quorum threshold is required (simple majority, two-thirds, unanimous)?
- what is the escalation owner if the vote deadlocks?
- what is the voting deadline (in working days)?

If `.arb/config.yml` already exists, read it before asking - do not ask for information already present.

Return:
1. confirmation of voters and quorum settings to be written to config;
2. the `create_vote.py` command to run;
3. a sample notification message the initiator can send to voters;
4. a reminder of the deadline and escalation path.

Do not create vote files directly - always use `scripts/create_vote.py`.
Do not invent voter email addresses if not provided.
