# LinkSnap Operations Runbook

## Application Overview

LinkSnap is a URL shortener API running on Azure Container Apps with Cosmos DB for NoSQL.

## Useful Commands

```bash
# View container app logs
az containerapp logs show --name linksnap-prod --resource-group rg-linksnap-prod

# Check Cosmos DB metrics
az monitor metrics list --resource <cosmos-id> --metric "TotalRequests" --interval 5m

# Restart the container app (new revision)
az containerapp revision activate --revision linksnap-prod--xxx --resource-group rg-linksnap-prod

# Scale to zero (outside business hours)
az containerapp update --name linksnap-prod --resource-group rg-linksnap-prod --min-replicas 0
```

## Health Check

```http
GET /health
Response: {"status": "ok"}
```

## Known Gaps (from risk register)

| Risk | Impact | Workaround |
|------|--------|------------|
| No DR plan (single-region ACA) | Regional outage = downtime | Accept for Quickstart. Redeploy to alternate region manually. |
| No auth on API | Anyone can create short links | Rate limiting on roadmap. Cosmos RU cap limits damage. |

## Monitoring

- Azure Monitor alerts configured for: 5xx rate > 5%, P99 latency > 1s, Cosmos 429 rate > 0
- SLO target: 99.5% uptime (single-region, best-effort)

## Escalation

| Severity | Response Time | Contact |
|----------|--------------|---------|
| Critical (down) | 30 min | Delivery Lead |
| High (degraded) | 2 hours | Delivery Lead |
| Low (question) | Next business day | Product Owner |
