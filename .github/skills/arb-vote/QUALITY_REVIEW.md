# Quality Review - arb-vote

**Version:** 1.0.0  
**Reviewed:** 2026-05-30  
**Score:** 8/10

## What works well

- **Anti-hallucination rules are explicit and testable.** Each rule has a clear "NEVER" statement and a corresponding check that can be verified by reading config or vote files.
- **Exit codes are documented and consistent.** `tally_votes.py` exit codes match CI gate conventions (0 = success, non-zero = failure or advisory state).
- **Immutability contract is clear.** The rule that outcomes are immutable (new round required to re-vote) prevents common governance anti-patterns.
- **Optional-voter semantics are explicit.** The decision map distinguishes optional rejections (advisory) from required rejections (blocking) - a common point of confusion in governance workflows.
- **Scripts use stdlib + PyYAML only.** No heavy dependencies; installable in any Python 3.10+ environment.

## Known gaps (honest assessment)

- **No delegation support yet.** If a required voter is unavailable, there is no formal proxy/delegation mechanism in config or scripts. Workaround: edit config to substitute the delegate before running `create_vote.py`.
- **No notification system.** The skill generates files but does not send emails, Slack messages, or GitHub @-mentions to voters. Integration with notification systems is out of scope for v1.0 but would improve adoption.
- **No vote amendment tracking.** If a voter edits their vote file after initially casting, there is no diff or audit log of the change beyond git history. Downstream governance may require a stricter amendment trail.
- **Quorum formula assumes integer votes.** Weighted voting (where some voters count more than others) is not supported. This is a deliberate scope constraint for v1.0.
- **arb-outcome.md can be manually edited.** Nothing prevents a human from editing the outcome file after it is written. Enforcement relies on PR review and commit signing, not technical controls.

## What was not included (intentional)

- GUI or web interface - out of scope; this is a files-first skill.
- Integration with GitHub PR status checks - partially addressed by `references/workflows/arb-vote.yml` but full integration requires repo-specific setup.
- Multi-round vote tracking - each vote is a single round; archive-and-re-initiate is the pattern for re-votes.
