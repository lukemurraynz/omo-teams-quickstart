---
last_verified: "2026-05-30"
---

# Tally ARB Vote

Use `SKILL.md`, `actions/tally-votes.md`, and `standards/quorum-rules.md` to compute the outcome.

Ask or infer:
- where is `.arb/config.yml`?
- have all required voters committed their vote files?
- is a dry-run preview wanted, or should the outcome be written to `arb-outcome.md`?

Before running the tally:
- run `check_quorum.py` and report who is still pending;
- confirm quorum is met or that `allow_partial: true` is set.

After running the tally:
- report the outcome (approved / rejected / deadlock / insufficient-quorum);
- show the vote breakdown table;
- describe the appropriate next step per the decision map in `SKILL.md`.

If outcome is `deadlock`:
- identify the escalation owner from config;
- outline the escalation checklist from `actions/escalate-deadlock.md`.

Do not report an outcome without running the script or reading all vote files.
Do not modify any voter's vote file.
