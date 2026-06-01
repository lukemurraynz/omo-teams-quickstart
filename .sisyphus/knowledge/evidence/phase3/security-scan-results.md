# Security Scan Results — LinkSnap API

**Date:** 2026-06-01
**Tools:** Trivy (container), pip-audit (dependencies)

## Trivy — Container Image

| Scan Target | Vulnerabilities | Critical | High | Medium | Low |
|------------|----------------|----------|------|--------|-----|
| Python 3.12-slim base image | 3 | 0 | 0 | 1 | 2 |
| pip packages | 0 | 0 | 0 | 0 | 0 |

All findings are in the OS base layer (Debian bookworm). No application-level findings.

## pip-audit — Dependencies

| Package | Version | Advisory | Severity | Fixed In |
|---------|---------|----------|----------|----------|
| No known vulnerabilities found | | | | |

## OWASP Top 10 Check

| Category | Status | Notes |
|----------|--------|-------|
| API1: Broken object-level authorisation | Not addressed | No auth in Quickstart — accepted scope gap |
| API8: Automated threats | Not addressed | Rate limiting not configured — logged in risk register |
| API9: Improper assets management | PASS | ADR-001 documents the API surface |
| API10: Unsafe consumption of APIs | PASS | Input validation on destination_url via Pydantic |

## Verdict

No blocking security findings. The two accepted gaps (no auth, no rate limiting) are documented in the threat model and risk register.
