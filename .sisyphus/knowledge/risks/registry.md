# Risk Register — LinkSnap URL Shortener

Seeded during Phase 0 Intake. Updated through lifecycle.

| ID | Risk | Likelihood | Impact | Score | Mitigation | Owner | Status |
|----|------|-----------|--------|-------|------------|-------|--------|
| R01 | Team has no production experience with Azure Container Apps secrets | High | High | 9 | Spike on ACA managed identity + Key Vault in Phase 1 | Delivery Lead | Mitigated |
| R02 | Cosmos DB RU cost overrun under load | Medium | High | 6 | Autoscale with max RU cap; load test in Phase 3 | Principal Architect | Open |
| R03 | No existing CI/CD pipeline for containerised Python apps | Medium | Medium | 4 | Use GitHub Actions starter template; verified in Phase 1 | Delivery Lead | Mitigated |
| R04 | URL shortener analytics dependency may require SQL for reporting | Low | Medium | 3 | Restrict Phase 1 to Cosmos DB only; defer analytics to v2 | Product Owner | Accepted |
| R05 | Container image may contain CVEs if base image not pinned | Medium | High | 6 | Pin Python 3.12-slim digest; Trivy scan in CI | Security Lead | Mitigated |
| R06 | No DR plan for single-region ACA deployment | Low | High | 3 | Accept for Quickstart; document in runbook as known gap | Delivery Lead | Accepted |
| R07 | Agent token budget may be exceeded by LLM-heavy phases | Medium | Medium | 4 | Track per-phase token spend; switch to Sonnet for Phase 3 | Delivery Lead | Open |
