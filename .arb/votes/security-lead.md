---
name: Security Lead
vote: conditional
voted_at: 2026-06-01T11:15:00Z
rationale: "Managed identity approach is correct. But ADR-003 doesn't specify how local development authenticates. Need a documented fallback (DefaultAzureCredential or Azurite) before Phase 2. Also missing: network security perimeter for Cosmos DB."
---

# Vote: Security Lead

**Proposal:** Phase 1 → 2 Gate: LinkSnap architecture sign-off

## Decision

Conditional — two mandatory revisions required before Phase 2 begins.

## Mandatory Revisions

1. **ADR-003 amendment**: Document the local development auth path. Must specify Azure CLI credential fallback and that no connection strings are used in dev either.
2. **Add network perimeter note**: State whether Cosmos DB will use a private endpoint or public access with IP firewall. Quickstart can use public with IP firewall, but it must be decided, not assumed.

## Rationale

The managed identity direction is correct. But an ADR that says "use managed identity" without specifying the local dev path creates a gap where a developer will inevitably drop a connection string into a `.env` file and commit it. I've seen it happen. Let's close both gaps before code starts.
