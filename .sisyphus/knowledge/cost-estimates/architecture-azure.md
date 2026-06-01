# Azure Cost Estimate — LinkSnap URL Shortener

Estimated monthly run rate for production deployment in New Zealand North.

## Resources

| Resource | SKU | Estimated Monthly Cost |
|----------|-----|-----------------------|
| Azure Container Apps — 2 apps × 1 replica | Consumption | $25 |
| Azure Cosmos DB for NoSQL — Serverless | 400 RU/s autoscale | $30 |
| Azure Container Registry — Basic | 1 registry | $5 |
| GitHub Actions — Public repo | Free | $0 |
| **Total** | | **$60/month** |

## Assumptions

- Low traffic: <10,000 requests/day.
- Single-region deployment (New Zealand North).
- Cosmos DB serverless mode — no minimum RU spend.
- No Azure Front Door or DNS (demo only).
- No log analytics workspace cost included (<5 GB/month).

## Comparison

| Option | Monthly Cost | Notes |
|--------|-------------|-------|
| ACA Consumption + Cosmos Serverless | $60 | Selected — best fit for Quickstart |
| ACA Consumption + Cosmos Provisioned 400 RU | $70 | Higher base cost, no benefit at this scale |
| AKS + Cosmos Serverless | $120+ | Overkill for single API |

## Approval

Budget approved by Product Owner and Cloud Economics at Gate 0→1.
Variance of +20% allowed without re-approval.
