# ADR-001: Host URL shortener API on Azure Container Apps

**Status:** Accepted
**Date:** 2026-06-01
**Phase:** 1

## Context

LinkSnap is a lightweight Python/FastAPI URL shortener. It needs a managed container runtime with HTTPS, scaling, and minimal operational overhead. The team is familiar with containers but wants to avoid Kubernetes complexity for a single API.

## Options Considered

| Option | Pro | Con |
|--------|-----|-----|
| Azure Container Apps (Consumption) | Serverless, HTTP ingress built in, revision management, <$30/month | No direct VNet egress without workload profile |
| Azure App Service | Easy deployment, built-in auth | No container-native revision management, higher cost at $50+ |
| AKS | Full Kubernetes control, extensibility | Operational overhead for single API, $70+ cluster cost |

## Decision

Use Azure Container Apps (Consumption tier) with managed identities and GitHub Actions CI/CD.

## Rationale

- ACA maps directly to the deployment model: a FastAPI container behind an HTTPS ingress.
- Consumption tier cost matches the Quickstart budget.
- Revision management gives us blue-green deploy without extra tooling.
- The single-region limitation is accepted (R06 in risk register).

## Consequences

- Must use managed identity (no connection strings) — see ADR-003.
- Container must be stateless and pass through to Cosmos DB.
- Can't use filesystem or local storage for sessions.

## Compliance

- Azure Well-Architected Framework: Reliability (single-region gap accepted), Cost Optimization (Consumption tier).
