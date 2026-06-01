# OMO Teams Quickstart

A reference implementation of the Oh My OpenAgent (omo) Teams governance model — 5 AI-powered teams, 5 ARB gates, one deployed application. Built using the model it demonstrates.

## The project

LinkSnap is a URL shortener API on Azure Container Apps with Cosmos DB for NoSQL. It's deliberately simple so the methodology is the story.

## What's inside

```
.sisyphus/                    # Governance artifacts
  knowledge/
    adrs/                     # Architecture Decision Records (3 ADRs)
    risks/                    # Risk register (7 items)
    agent-economics/          # Token budget tracking
    security/                 # Threat model (STRIDE + OWASP)
    data/                     # Data model with PII classification
    cost-estimates/           # Azure cost estimate ($60/month)
    arb/                      # ARB gate checklists and outcomes
    evidence/                 # Load test + security scan results
    runbooks/                 # Operations runbook
  teams/registry.md           # Team definitions
src/api/                      # FastAPI application
infra/main.bicep              # Bicep infrastructure
.github/workflows/ci.yml      # CI/CD pipeline
src/tests/test_api.py         # Integration tests
```

## The 5 gates

| Gate                       | Voters                                            | Outcome                         |
| -------------------------- | ------------------------------------------------- | ------------------------------- |
| Phase 0 → 1 — Intake       | Product Owner, Cloud Economics                    | Approved                        |
| Phase 1 → 2 — Architecture | Principal Architect, Security Lead, Product Owner | **Conditional** (Security Lead) |
| Phase 2 → 3 — Build        | Principal Architect, Product Owner                | Approved                        |
| Phase 3 → 4 — Validate     | Security Lead, Product Owner, Cloud Economics     | Approved                        |
| Phase 4 → Prod — Release   | Product Owner, Security Lead, Cloud Economics     | Approved                        |

## Quickstart

```bash
# Clone the repo
git clone https://github.com/lukemurraynz/omo-teams-quickstart
cd omo-teams-quickstart

# Deploy infrastructure
az deployment group create --resource-group rg-linksnap --template-file infra/main.bicep

# Build and push container
az acr build --registry <acr-name> --image linksnap src/api/

# Deploy container app
az containerapp update --name linksnap --image <acr-name>.azurecr.io/linksnap:latest
```

## Prerequisites

- Python 3.12+
- Azure CLI
- Bicep CLI
- An Azure subscription

## References

- [Oh My OpenAgent Team Mode](https://omo.dev/docs#team-mode)
- [Azure Container Apps documentation](https://learn.microsoft.com/azure/container-apps/?WT.mc_id=AZ-MVP-5004796)
- [Cosmos DB for NoSQL](https://learn.microsoft.com/azure/cosmos-db/nosql/?WT.mc_id=AZ-MVP-5004796)
