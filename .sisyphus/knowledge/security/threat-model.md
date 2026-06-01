# Threat Model — LinkSnap URL Shortener

**Date:** 2026-06-01
**Phase:** 1

## Scope

- LinkSnap FastAPI on ACA
- Cosmos DB for NoSQL
- GitHub Actions CI/CD pipeline
- ACR container registry

## Data Flow

```
User → HTTPS → ACA (FastAPI) → Cosmos DB (via managed identity)
                            ↘ ACR (pull image via managed identity)
```

## STRIDE Analysis

| Threat | Component | Risk | Mitigation |
|--------|-----------|------|------------|
| Spoofing — attacker impersonates API | ACA ingress | Medium | HTTPS enforced by ACA default; no custom domain in Quickstart |
| Tampering — request manipulation | API → Cosmos | Low | Managed identity authenticates all DB calls; input validation on destination_url |
| Repudiation — missing audit trail | All | Low | Container insights + Cosmos DB diagnostic logs; no user auth in v1 |
| Information disclosure — PII leak in logs | API | Medium | Data model marks PII fields; must not log destination_url contents |
| Denial of service — excessive short code creation | ACA + Cosmos | Medium | No auth in Quickstart means unauthenticated create; accepted risk |
| Elevation of privilege — container breakout | ACA sandbox | Low | Consumption tier sandbox; no privileged operations |

## OWASP API Security Top 10

| API Security Risk | Status | Evidence |
|-------------------|--------|----------|
| API1: Broken object-level authorisation | Not addressed | No auth in Quickstart — accepted for demo scope |
| API8: Lack of protection from automated threats | Partial | Rate limiting not configured — backlog |
| API9: Improper assets management | Addressed | ADR-001 documents the API surface |
| API10: Unsafe consumption of APIs | Addressed | Input validation on destination_url |

## Agentic Threats (ASI01-ASI10)

N/A — no AI agents in the LinkSnap runtime. (OCI: The OMO Teams building the Quickstart are AI agents, but the application itself has no agentic surface.)

## Containers

| Check | Status |
|-------|--------|
| Base image pinned to digest | Addressed — Python 3.12-slim with SHA pin |
| Trivy scan in CI | Planned for Phase 3 |
| Image signing | Out of scope for Quickstart |
