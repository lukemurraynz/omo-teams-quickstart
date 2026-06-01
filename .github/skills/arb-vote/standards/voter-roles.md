---
last_verified: "2026-05-30"
---

# Standard: Voter Roles

## Required vs optional voters

| Type | Meaning | Effect on outcome |
|------|---------|------------------|
| `required` | Must vote for quorum to be met | Any required `reject` blocks approval |
| `optional` | Advisory voice; quorum does not depend on them | Rejection is recorded but does not block required-voter approval |

## Config structure

```yaml
arb:
  required_voters:
    - name: alice           # Username or unique ID — used as vote file name
      role: "Principal Architect"
      email: "alice@example.com"
    - name: bob
      role: "Security Lead"
      email: "bob@example.com"

  optional_voters:
    - name: carol
      role: "Domain Expert"
      email: "carol@example.com"
```

## Role definitions (defaults - override in your organization's config)

| Role | Type | Typical voter | Rationale |
|------|------|---------------|-----------|
| Principal Architect | required | Overall design authority | Cross-cutting concerns, architectural fit |
| Security Lead | required | InfoSec representative | Threat model, compliance, data handling |
| Product Owner | required | Business authority | Feature value, trade-off acceptance |
| Cloud Economics | required | FinOps / cost owner | Cost governance, budget variance, WAF Cost Optimization |
| Platform Lead | optional | Infrastructure/ops owner | Operability, SLA impact, tooling fit |
| Domain Expert | optional | Subject-matter owner | Correctness of domain-specific decisions |
| Delivery Lead | optional | Engineering / delivery lead | Evidence presenter — recused from approving own phase |
| AI Ethics / RAI | conditional | Responsible AI lead | Required when AI/agents, LLMs, or automated decisions are in scope |

These are examples. Define your own roles in config to match your organization's ARB charter.

### Conditional roles

A *conditional* role is required only when specific criteria are met. The most common conditional role is:

- **AI Ethics / RAI** — add this voter when the proposal involves AI agents, LLM integration, Copilot extensions, automated decision-making, or any system that could produce AI-generated content affecting users. This maps to the [Responsible AI Operating Model](../../responsible-ai-operating-model/SKILL.md).

Conditional voters should be documented in the gate checklist rationale so the audit trail shows whether they applied.

## Voter skill dependencies

Each voter loads domain skills that produce the evidence they need to cast an informed vote. The skills are loaded from the repository's `.github/skills/` directory. The ARB chair (governance-gate) verifies that the evidence each skill produces exists before allowing the gate to proceed.

| Role | Skills to load | Evidence produced | Validated at gate |
|------|---------------|-------------------|-------------------|
| Principal Architect | [adr-management](../../adr-management/SKILL.md) | ADR structural check, drift detection | 1→2, 2→3 |
| Security Lead | [threat-modelling](../../threat-modelling/SKILL.md), [owasp-agentic](../../owasp-agentic/SKILL.md), [container-operations](../../container-operations/SKILL.md) | STRIDE analysis, dependency audit, container scan | 1→2, 3→4 |
| Cloud Economics | [cost-optimization](../../cost-optimization/SKILL.md) | Cost estimate validation, budget variance check | 0→1, 3→4, 4→Prod |
| Product Owner | [decision-record](../../decision-record/SKILL.md) | Business case trace, scope compliance | 0→1, 4→Prod |
| Delivery Lead | [agent-economics](../../agent-economics/SKILL.md) | Token budget vs actual report | All phases |
| ARB Chair (Janus) | [governance-gate](../../governance-gate/SKILL.md), [arb-vote](../../arb-vote/SKILL.md) | Gate checklist, vote tally, outcome | All gates |

### Evidence dependency enforcement

The tally script checks that each voter's required evidence files exist before counting their vote. Voter config can specify `evidence_required` paths:

```yaml
required_voters:
  - name: security-lead
    role: "Security Lead"
    evidence_required:
      - "docs/evidence/threat-model-validation.md"
      - "docs/evidence/dependency-audit.md"
```

If the evidence file does not exist, the tally script treats the voter as `pending` — the voter has not done their job. This prevents narrative-only reviews.

## Voter name convention

- `name` must be a single word, lowercase, no spaces (used as the vote filename: `votes/<name>.md`).
- Use username or initials if names conflict: `alice`, `bob_security`, `carol_domain`.
- Names must be unique across required and optional voters.

## Delegation

If a required voter is unavailable:

1. Confirm delegation is permitted by your ARB charter.
2. Update `name` in `.arb/config.yml` to the delegate's name and set `role` to the original role.
3. Add a comment in the vote file body noting the delegation:
   ```
   Note: casting vote on behalf of [original voter] who is on leave.
   Delegation authorized by [authority] on YYYY-MM-DD.
   ```
4. Re-run `create_vote.py` to generate the new file.

Do not cast a vote in someone else's name without documented authorization.

## Adding voters after vote creation

1. Add the new voter to `.arb/config.yml`.
2. Re-run `create_vote.py` - it will create only the new voter's file, not overwrite existing ones.
3. Notify the new voter.
4. If they are required, quorum calculation updates automatically.

## Removing voters after vote creation

1. Remove from `.arb/config.yml`.
2. Do not delete their vote file - it is part of the audit trail.
3. The tally script reads voters from config; a file with no matching config entry is ignored in the quorum calculation (but is preserved on disk).
