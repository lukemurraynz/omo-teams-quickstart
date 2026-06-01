---
voter: VOTER_NAME
role: VOTER_ROLE
voter_type: required
proposal: ADR-YYYY-NNN
vote: pending
voted_at: null
---

# Vote: VOTER_NAME

**Proposal:** ADR-YYYY-NNN  
**Role:** VOTER_ROLE

## Decision

Replace `vote: pending` in the frontmatter above with one of:

- `approve` - in favour of this proposal
- `reject` - opposed to this proposal (rationale required below)
- `abstain` - not casting a directional vote

Also update `voted_at` with the current UTC time: `"YYYY-MM-DDTHH:MM:SSZ"`

## Rationale

<!-- 
Required if vote: reject.
Optional (but encouraged) for approve and abstain.
Explain your reasoning, concerns, or conditions.
-->
