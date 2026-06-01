# ADR-003: Use managed identity for all Azure resource authentication

**Status:** Accepted
**Date:** 2026-06-01
**Phase:** 1

## Context

LinkSnap needs to authenticate to Cosmos DB from ACA. The default approach is a connection string with a primary key. This is a security risk (key in config, no rotation, no audit).

## Options Considered

| Option | Pro | Con |
|--------|-----|-----|
| Managed identity + RBAC | No secrets in config, role-based access, audit trail | Requires Data Plane RBAC role assignment for Cosmos DB |
| Connection string (primary key) | Simple, works immediately | Secret in config, no rotation, no audit, security finding |
| Key Vault reference | Better than plaintext key | Still a static secret, still needs rotation |

## Decision

Use ACA system-assigned managed identity with Cosmos DB Data Plane RBAC (Cosmos DB Built-in Data Contributor role).

## Rationale

- Zero secrets in configuration — the ACA runtime handles token acquisition.
- RBAC provides audit trail of which identity accessed which resource.
- Aligns with Security Lead's requirement from Gate 0→1.
- ACA managed identity is a first-class feature, no additional setup.

## Consequences

- Must assign Cosmos DB role to the ACA workload identity at deploy time (Bicec).
- Local development uses Azure CLI credential fallback (Azure.Identity.DefaultAzureCredential).
- No connection strings anywhere in the codebase.

## Compliance

- OWASP API Security Top 10: API8 (lack of protection from automated threats — mitigated by managed identity).
- Microsoft CAF: security baseline — identity as perimeter.
