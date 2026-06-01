---
applyTo: "**/.arb/config.yml,**/arb-config.yml"
last_verified: "2026-05-30"
---

# ARB Vote Config Instructions

This file applies when editing `.arb/config.yml` or any file named `arb-config.yml`.

## Required fields

```yaml
arb:
  proposal: "ADR-2026-001: Short title of the proposal"

  required_voters:
    - name: alice           # Lowercase, no spaces; becomes vote filename
      role: "Principal Architect"
      email: "alice@example.com"

  quorum:
    approval_threshold: 0.67   # Must be > 0.5 to avoid perpetual deadlock risk
```

## Full schema with defaults

```yaml
arb:
  proposal: ""                    # REQUIRED — proposal title or ADR ID

  required_voters: []             # REQUIRED — at least one entry
    # - name: string              # REQUIRED
    #   role: string              # REQUIRED
    #   email: string             # Optional

  optional_voters: []             # Optional — advisory voters
    # - name: string
    #   role: string
    #   email: string

  quorum:
    min_required_voters: ~        # Default: len(required_voters) — all must vote
    min_total_votes: 1            # Minimum counted votes for quorum
    approval_threshold: 0.51      # Fraction of counted votes needed to approve
    count_abstain: false          # Whether abstain counts in denominator
    allow_partial: false          # Allow outcome before all required voters vote

  deadlock:
    escalate_to: ""               # REQUIRED if deadlock is possible — role or name
    escalation_contact: ""        # Email/Slack handle of escalation owner
    escalation_days: 3            # Working days before timeout escalation
    escalation_backup: ""         # Secondary escalation owner if primary is unavailable
```

## Naming constraints

- `name` values must be unique across `required_voters` and `optional_voters`.
- `name` must match `[a-z0-9_-]+` (lowercase, no spaces or special characters).
- The `name` becomes the vote filename: `votes/<name>.md`.

## Common configurations

### Simple two-person approval (simple majority)

```yaml
arb:
  proposal: "ADR-2026-005: Use Azure Event Grid for notifications"
  required_voters:
    - name: alice
      role: "Principal Architect"
    - name: bob
      role: "Security Lead"
  quorum:
    approval_threshold: 0.51
  deadlock:
    escalate_to: "VP Engineering"
    escalation_days: 2
```

### Three-person board with two-thirds majority

```yaml
arb:
  proposal: "ADR-2026-010: Adopt Kubernetes for all workloads"
  required_voters:
    - name: alice
      role: "Principal Architect"
    - name: bob
      role: "Security Lead"
    - name: dave
      role: "Platform Lead"
  optional_voters:
    - name: carol
      role: "Domain Expert"
  quorum:
    min_required_voters: 3
    min_total_votes: 3
    approval_threshold: 0.67
    count_abstain: false
  deadlock:
    escalate_to: "CTO"
    escalation_contact: "cto@example.com"
    escalation_days: 3
```

### Emergency partial-quorum (allow vote to proceed without all required voters)

```yaml
quorum:
  allow_partial: true
  min_required_voters: 2    # Only need 2 of 3 required voters
  approval_threshold: 0.67
```

Document why `allow_partial: true` was used in `arb-outcome.md`.
