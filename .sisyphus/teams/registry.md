# OMO Teams Registry

This Quickstart uses the OMO 5-phase lifecycle with the following teams.

| Phase | Team | Chair | Voters | Purpose |
|-------|------|-------|--------|---------|
| Phase 0 → 1 | intake | Janus | Product Owner, Cloud Economics | Business case, budget, risk readiness |
| Phase 1 → 2 | architecture | Janus | Principal Architect, Security Lead, Product Owner | ADR sign-off, threat model, data model |
| Phase 2 → 3 | build | Janus | Principal Architect, Product Owner | Code complete, evidence present |
| Phase 3 → 4 | validate | Janus | Security Lead, Product Owner, Cloud Economics | E2E tests pass, security hardened |
| Phase 4 → Prod | release | Janus | Product Owner, Security Lead, Cloud Economics | DR tested, runbooks ready, SLOs live |

## Roles

| Role | Persona | Responsibility |
|------|---------|----------------|
| ARB Chair | Janus | Chairs gate reviews, enforces checklist, publishes outcome |
| Product Owner | Business owner | Approves business value, trade-off decisions |
| Principal Architect | Design authority | Signs off on architecture decisions |
| Security Lead | InfoSec | Threat model, compliance, OWASP, agentic risk |
| Cloud Economics | FinOps | Cost governance, budget variance, WAF Cost Optimization |
| Delivery Lead | Project lead | Presents evidence at gates, recused from approving own phase |
