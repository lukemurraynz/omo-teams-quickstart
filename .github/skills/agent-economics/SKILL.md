---
name: agent-economics
description: >-
  Plan, track, and reconcile AI agent token budgets across a project lifecycle.
  Covers per-phase token budget allocation, model tier selection trade-offs,
  cost-per-task estimation, retry loop economics, context compaction strategy,
  and phase-end reconciliation reporting.
compatibility: Any Markdown editor; Python 3.10+ for budget tracking scripts
last_verified: "2026-05-30"
---

# Agent Economics Skill

## Anti-Hallucination Rule (MANDATORY)

- **NEVER report token counts or costs without reading actual usage data.** Estimates must be labelled as estimates; actuals must come from telemetry or provider billing.
- **NEVER recommend a model tier without stating the trade-off.** Every tier recommendation must include a cost-vs-capability rationale.
- **NEVER carry over unspent budget silently.** Document carry-forward explicitly in the phase report.

## What This Skill Covers

Agent economics is the cost governance layer for AI agents operating within a project. It is distinct from Azure infrastructure cost (see `finops` and `cost-optimization`) - it covers the cost of the agents themselves: the tokens they consume, the models they call, and the loops they run.

## Budget Baseline Format

Initialized at Phase 0, maintained at `.sisyphus/knowledge/agent-economics/budget-baseline.md`:

```markdown
# Agent Economics Budget Baseline

## Phase Budgets

| Phase | Token Budget | Model Tier Ceiling | Max Retry Loops | Max Human Interventions | Est. Cost |
|-------|-------------|-------------------|-----------------|------------------------|-----------|
| Phase 0 | 20k | Sonnet | 3 | 2 | ~$0.10 |
| Phase 1 | 80k | Opus (lead), Sonnet (members) | 5 | 3 | ~$4.00 |
| Phase 2 | 200k | Opus (lead), mixed members | 5 | 3 | ~$8.00 |
| Phase 3 | 100k | Sonnet (most), Opus (security) | 5 | 3 | ~$3.50 |
| Phase 4 | 110k | Sonnet (most), Haiku (writing) | 5 | 3 | ~$2.50 |
| **Total** | **510k** | | | | **~$18.10** |

## Model Tier Reference (2026 pricing guide — verify against current rates)

| Tier | Model | Input $/1M | Output $/1M | Use when |
|------|-------|-----------|------------|---------|
| Haiku | claude-haiku-4-5 | $0.80 | $4.00 | Writing, formatting, quick tasks |
| Sonnet | claude-sonnet-4-6 | $3.00 | $15.00 | Most technical members |
| Opus | claude-opus-4-6 | $15.00 | $75.00 | Lead, ultrabrain, critical reasoning |

## Retry Loop Economics

Each retry loop iteration costs ~(average_task_tokens × model_rate).
Default: 5 loops max per phase. At loop 5 without resolution: escalate to human.
Human intervention cost: ~30 min engineer time (~$25 equivalent). Budget 3 per phase.
```

## Per-Phase Report Format

At the end of each phase, write to `.sisyphus/knowledge/agent-economics/phase{N}-report.md`:

```markdown
# Agent Economics: Phase N Report

## Budget vs Actual

| Metric | Budget | Actual | Variance |
|--------|--------|--------|---------|
| Total tokens | 80k | 73k | -9% (under) |
| Estimated cost | $4.00 | $3.65 | -$0.35 |
| Retry loops used | ≤5 | 3 | OK |
| Human interventions | ≤3 | 1 | OK |

## Model Breakdown

| Member | Model | Tokens | Cost |
|--------|-------|--------|------|
| backend-arch | claude-sonnet-4-6 | 22k | $0.88 |
| infra-arch | claude-opus-4-6 | 18k | $2.07 |
| ... | | | |

## Carry-Forward

Remaining budget from this phase: 7k tokens ($0.35).
Carry-forward to Phase N+1: [yes/no — state policy].

## Observations

- [Any model tier that was over/under selected for the task]
- [Any retry storm patterns]
- [Recommendations for next phase]
```

## Model Tier Selection Guide

| Task type | Recommended tier | Rationale |
|-----------|-----------------|-----------|
| Governance, reasoning, cross-cutting decisions | Opus | Needs deepest reasoning |
| Technical implementation (architecture, code) | Sonnet | Strong capability, 5× cheaper than Opus |
| Writing, formatting, documentation | Haiku or Sonnet | Writing doesn't need Opus-level reasoning |
| Quick lookups, search, summarization | Haiku | Cheapest for low-complexity tasks |
| Security review, threat model | Opus or Sonnet | High stakes; don't cut corners |
| Agent evaluation, test running | Haiku | Mechanical execution, not reasoning |

## Context Compaction Economics

Long conversations accumulate tokens. Compaction (summarizing earlier turns) reduces cost:
- Use `durable-work` skill to offload tasks that survive session boundaries rather than holding all context in one session.
- Target: compaction when conversation exceeds 50k tokens in a single session.
- Compaction saves ~40–60% on re-read costs when context is dense.

## Budget Overrun Protocol

If a phase is tracking to exceed budget by >20%:
1. Stop non-critical work immediately.
2. Report to lead with current spend and projection.
3. Lead approves budget extension or descopes work.
4. Document in phase report with rationale.

Never silently exceed budget. Token overruns compound: Phase 2 overruns leave less headroom for Phase 3 debugging loops.

## Gate Integration

At each ARB gate, cloud-economics voter checks:
- Phase token spend vs budget-baseline allocation.
- Phase report exists and is reconciled.
- Total cumulative spend vs total project budget.

A phase where the report is missing or shows >20% overrun without documented approval is a gate condition.
