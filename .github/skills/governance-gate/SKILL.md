---
name: governance-gate
description: >-
  Orchestrate ARB phase gate reviews: author the gate readiness checklist,
  inventory evidence, track CONDITIONAL revision cycles, format APPROVED /
  CONDITIONAL / REJECTED outcomes, and maintain the audit trail across the
  five-phase OMO governance lifecycle.
compatibility: Any Markdown editor; used by arb-review team
last_verified: "2026-05-30"
---

# Governance Gate Skill

## Anti-Hallucination Rule (MANDATORY)

- **NEVER declare a gate APPROVED without checking every checklist item.** A gate is only approved when the checklist has no blocking items.
- **NEVER invent evidence.** Every checklist item must reference an actual file path. If the file does not exist, the item is FAIL.
- **NEVER produce a CONDITIONAL outcome without listing the exact mandatory revisions.** Vague "needs improvement" notes are not actionable.
- **NEVER allow a phase to proceed after a REJECTED gate.** The phase must be redone; do not re-interpret a rejection as conditional.

## Gate Readiness Checklist Template

Write to `.sisyphus/knowledge/arb/{phase}-gate/checklist.md`:

```markdown
# Gate Readiness Checklist — Phase N Gate

**Phase:** N  
**Review date:** YYYY-MM-DD  
**Chair:** Janus  
**Voters:** Product Owner, Security Lead, Cloud Economics

## Evidence Inventory

| Item | Required File | Status | Notes |
|------|--------------|--------|-------|
| ADR registry | .sisyphus/knowledge/adrs/registry.md | PASS/FAIL | All ADRs Accepted/Amended |
| Threat model | .sisyphus/knowledge/security/threat-model.md | PASS/FAIL | |
| Risk register | .sisyphus/knowledge/risks/registry.md | PASS/FAIL | No unaccepted High/Critical |
| Cost estimate | .sisyphus/knowledge/cost-estimates/architecture-azure.md | PASS/FAIL | Within budget |
| Agent economics | .sisyphus/knowledge/agent-economics/phaseN-report.md | PASS/FAIL | Within token budget |
| Data model | .sisyphus/knowledge/data/data-model.md | PASS/FAIL | PII fields identified |
| Phase evidence | .sisyphus/evidence/phaseN/ | PASS/FAIL | All expected artefacts present |

## ADR Gate Check

| Requirement | Status | Blocking |
|-------------|--------|---------|
| All ADRs in registry are Accepted or Amended | PASS/FAIL | Yes |
| No ADR with status Proposed | PASS/FAIL | Yes |
| All amended ADRs have amendment artefact | PASS/FAIL | Yes |

## Risk Gate Check (use risk-register skill)

| Requirement | Status | Blocking |
|-------------|--------|---------|
| All Critical risks: Mitigated or Accepted | PASS/FAIL | Yes |
| All High risks: Mitigated or Accepted | PASS/FAIL | Yes |
| All Accepted risks have named authority | PASS/FAIL | Yes |
| No Open risks without mitigation plan + owner | PASS/FAIL | Yes |

## Security Gate Check

| Requirement | Status | Blocking |
|-------------|--------|---------|
| Threat model complete (all components covered) | PASS/FAIL | Yes |
| OWASP Top 10 addressed with evidence | PASS/FAIL | Yes |
| Container supply chain (signing, SBOM) — if applicable | PASS/FAIL | Yes |
| Agentic threats (ASI01-ASI10) — if AI agent in scope | PASS/FAIL | Yes |
| Defender for Cloud enabled | PASS/FAIL | Yes |

## WAF Gate Check (use azure-well-architected-assessment)

| Pillar | Score | Threshold | Status |
|--------|-------|-----------|--------|
| Reliability | N/5 | ≥3 | PASS/FAIL |
| Security | N/5 | ≥4 | PASS/FAIL |
| Cost Optimization | N/5 | ≥3 | PASS/FAIL |
| Operational Excellence | N/5 | ≥3 | PASS/FAIL |
| Performance Efficiency | N/5 | ≥3 | PASS/FAIL |

## Economics Gate Check

| Requirement | Status | Blocking |
|-------------|--------|---------|
| Azure cost within Phase 0 budget (or variance approved) | PASS/FAIL | Yes |
| Agent token spend within phase budget | PASS/FAIL | Yes |
| Phase economics report exists and is reconciled | PASS/FAIL | Yes |

## Gate Readiness Summary

**Blocking items:** N  
**Non-blocking findings:** N  
**Gate-ready:** YES / NO
```

## Outcome Format

Write to `.sisyphus/knowledge/arb/{phase}-gate/outcome.md`:

```markdown
---
phase: N
outcome: approved | conditional | rejected
decided_at: YYYY-MM-DDTHH:MM:SSZ
votes:
  product-owner: approved | conditional | rejected
  security-lead: approved | conditional | rejected
  cloud-economics: approved | conditional | rejected
tally: 3/3 | 2/3 | 1/3 | 0/3
---

# ARB Gate Outcome — Phase N

## Result: APPROVED / CONDITIONAL / REJECTED

## Vote Summary

| Voter | Vote | Rationale summary |
|-------|------|------------------|
| Product Owner | APPROVED | [1-line summary] |
| Security Lead | CONDITIONAL | [1-line summary] |
| Cloud Economics | APPROVED | [1-line summary] |

## Tally

Votes: X/3 approved.
Outcome threshold: 3/3 = APPROVED, 2/3 = CONDITIONAL, ≤1/3 = REJECTED.

## Mandatory Revisions (CONDITIONAL only)

1. [Specific revision with owner and deadline]
2. [Specific revision with owner and deadline]

## Re-review Trigger (CONDITIONAL only)

Re-review scheduled when:
- [ ] [Revision 1] completed — evidence at [path]
- [ ] [Revision 2] completed — evidence at [path]

Lead notifies ARB chair when all revisions complete. Chair re-runs checklist before approving.

## Next Steps

[APPROVED]: Phase N+1 may begin. Archive gate artefacts.
[CONDITIONAL]: Complete mandatory revisions. Do not begin Phase N+1.
[REJECTED]: Phase N must be redone. Review rejection rationales with lead.
```

## CONDITIONAL Revision Cycle

1. Gate produces CONDITIONAL with revision list.
2. Lead assigns revisions to relevant team members with deadlines.
3. Each revision is tracked as a risk in `.sisyphus/knowledge/risks/registry.md` (status: In Progress).
4. When revisions complete: chair re-runs the checklist items that were FAIL.
5. If all FAIL items are now PASS: chair upgrades outcome to APPROVED.
6. If any FAIL item cannot be resolved within agreed deadline: gate reverts to REJECTED.

## Audit Trail Requirements

The following must be committed and immutable after gate close:
- `checklist.md` - gate readiness evidence
- `outcome.md` - final decision with votes
- `votes/product-owner-vote.md`, `votes/security-lead-vote.md`, `votes/cloud-economics-vote.md`
- `waf-assessment.md` - WAF pillar scores

Do not edit outcome files after they are committed. For re-reviews, create a new `outcome-v2.md`.

## Phase-Specific Config Templates

For each gate, copy the matching template from the `arb-vote` skill to `.arb/config.yml`:

| Gate | Config Template | Key Voters |
|------|----------------|------------|
| Phase 0 → 1 | [phase0-intake.yml](../arb-vote/templates/phase-gates/phase0-intake.yml) | Product Owner, Cloud Economics |
| Phase 1 → 2 | [phase1-architecture.yml](../arb-vote/templates/phase-gates/phase1-architecture.yml) | Principal Architect, Security Lead, Product Owner |
| Phase 2 → 3 | [phase2-build.yml](../arb-vote/templates/phase-gates/phase2-build.yml) | Principal Architect, Product Owner |
| Phase 3 → 4 | [phase3-validate.yml](../arb-vote/templates/phase-gates/phase3-validate.yml) | Security Lead, Product Owner, Cloud Economics |
| Phase 4 → Prod | [phase4-prod.yml](../arb-vote/templates/phase-gates/phase4-prod.yml) | Product Owner, Security Lead, Cloud Economics |

Each template sets the right voters, quorum thresholds, and escalation path for that phase. Copy the appropriate one:

```bash
cp .github/skills/arb-vote/templates/phase-gates/phase1-architecture.yml .arb/config.yml
```

## Phase-Specific Gate Requirements

| Gate | Additional Requirements | Required Voters |
|------|------------------------|-----------------|
| Phase 0 → 1 | Business case approved; budget set; risk register seeded | Product Owner, Cloud Economics |
| Phase 1 → 2 | All architecture ADRs Accepted; data model PII-flagged; threat model complete | Principal Architect, Security Lead, Product Owner |
| Phase 2 → 3 | Code committed to feature branch; all member evidence present | Principal Architect, Product Owner |
| Phase 3 → 4 | All E2E tests pass; security hardening evidence complete; no open High risks | Security Lead, Product Owner, Cloud Economics |
| Phase 4 → Prod | DR test executed; runbooks complete; SLOs defined and dashboards live | Product Owner, Security Lead, Cloud Economics |
