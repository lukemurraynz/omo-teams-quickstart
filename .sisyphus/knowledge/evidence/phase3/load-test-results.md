# Load Test Results — LinkSnap API

**Date:** 2026-06-01
**Tool:** Locust (local)
**Target:** ACA staging revision

## Configuration

| Parameter | Value |
|-----------|-------|
| Users | 50 |
| Spawn rate | 5 users/sec |
| Duration | 5 minutes |
| Endpoint | POST /links + GET /links/{code} |

## Results

| Metric | Value | Target | Pass? |
|--------|-------|--------|-------|
| Avg response time (POST) | 180ms | <500ms | PASS |
| Avg response time (GET) | 45ms | <200ms | PASS |
| P99 response time | 620ms | <1000ms | PASS |
| Error rate | 0% | <1% | PASS |
| Requests/sec (peak) | 28 | N/A | - |

## Observations

- Cosmos DB serverless handled the load without throttling (no 429s observed).
- ACA scaled from 1 to 2 replicas during the test.
- The 620ms P99 was a cold-start on the second replica — expected for Consumption tier.
