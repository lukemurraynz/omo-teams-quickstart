# ADR-002: Use Cosmos DB for NoSQL with partition key on tenant_id

**Status:** Accepted
**Date:** 2026-06-01
**Phase:** 1

## Context

LinkSnap stores shortened URLs and their destination targets. The access pattern is: given a short code, return the destination URL. The data model also needs to support per-tenant analytics (count of clicks per short code).

## Options Considered

| Option | Pro | Con |
|--------|-----|-----|
| Cosmos DB for NoSQL | Serverless mode, low cost at low volume, SQL-like queries | Partition key must be chosen carefully |
| Azure SQL Database — Serverless | Relational, familiar | Higher minimum cost, more overhead for simple KV pattern |
| Azure Redis Cache | Blazing fast lookups | No persistence guarantee, no query capability |

## Decision

Use Cosmos DB for NoSQL with a `partition_key` of `/tenant_id`. The container has a composite index on `(short_code, tenant_id)` for fast lookups.

## Rationale

- Serverless mode means $0 minimum spend — critical for the $60/month budget.
- The tenant_id partition key evenly distributes writes if we ever multi-tenant.
- Single-document reads by short_code + tenant_id are point reads (1 RU each).
- Cosmos DB change feed gives us an analytics path for v2 without migrating.

## Consequences

- Must design all queries to include tenant_id to avoid cross-partition scans.
- Serverless has throughput limits (though well above Quickstart needs).
- RU monitoring needed in Phase 3 validation.

## Compliance

- Azure Well-Architected Framework: Performance Efficiency (point reads), Cost Optimization (serverless).
