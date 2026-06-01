# Business Case — OMO Teams Quickstart

## Problem

Engineering teams adopting multi-agent AI workflows have no reference implementation for governance. They either skip governance entirely (shipping unapproved ADRs, no threat models, no cost oversight) or add so much process that the agents become overhead.

## Solution

Build a Quickstart repo that demonstrates the OMO Teams governance model end-to-end on a real (but trivial) Azure application. The Quickstart itself is built using OMO Teams — proving the model works by eating our own dog food.

## Success Criteria

| Criterion | Target |
|-----------|--------|
| Time from Phase 0 to production | 2 weeks |
| ARB gates passed | All 5 |
| ADRs written and accepted | 3 |
| Risk register seeded and tracked | 7+ items |
| Working Azure application deployed | LinkSnap API on ACA |
| Quickstart repo published | Public GitHub repo |
| Blog post published | luke.geek.nz |

## Budget

| Item | Cost |
|------|------|
| Azure resources (1 month) | $60 |
| Agent token budget (all phases) | $18.10 |
| **Total** | **$78.10** |

## Risks

- See risk register (R01-R07). Key risk: R01 (ACA secrets experience) — mitigated by Phase 1 spike.
