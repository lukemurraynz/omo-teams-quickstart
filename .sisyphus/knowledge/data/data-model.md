# Data Model — LinkSnap URL Shortener

## Entity: ShortLink

| Field | Type | PK | Partition Key | Notes |
|-------|------|----|---------------|-------|
| tenant_id | string | ✓ | ✓ | Logical tenant identifier |
| short_code | string | ✓ | | 7-character base62 code |
| destination_url | string | | | Target URL (validated) |
| created_at | datetime | | | UTC timestamp |
| created_by | string | | | User or system identifier |
| click_count | int | | | Denormalised counter |
| is_active | bool | | | Soft delete flag |

## Access Patterns

| Pattern | Query | RU Estimate |
|---------|-------|-------------|
| Resolve short code | SELECT * FROM c WHERE c.tenant_id = @tid AND c.short_code = @code | 1 (point read) |
| List URLs for tenant | SELECT * FROM c WHERE c.tenant_id = @tid ORDER BY c.created_at DESC | 2-3 (cross-partition if no index) |
| Update click count | Patch c.click_count += 1 WHERE c.tenant_id = @tid AND c.short_code = @code | 1 (point read + replace) |

## PII Classification

| Field | PII | Classification | Notes |
|-------|-----|---------------|-------|
| tenant_id | No | Internal | Opaque identifier, not a customer name |
| destination_url | Possibly | Confidential | May contain PII in query parameters |
| created_by | Possibly | Confidential | Could be a user identifier or email |

All PII-classified fields must be logged only in approved audit paths. No PII in application logs.
