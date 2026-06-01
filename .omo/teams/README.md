# OMO Team Configs — Enterprise Governance Architecture

Five-phase lifecycle with ARB gate reviews between phases. Start with the `orchestrator` team for any new project.

## Team Catalog

| Team | Lead | Members | Gate Required |
|------|------|---------|---------------|
| [orchestrator](orchestrator/config.json) | atlas | 1 (delivery-orchestrator) | Entry point — drives all phases |
| [phase0-intake](phase0-intake/config.json) | atlas | 1 (product-owner) | ARB Gate 0 after |
| [phase1-architecture](phase1-architecture/config.json) | atlas | 6 (backend-arch, infra-arch, data-arch, agent-arch, security-arch, cloud-economics) | ARB Gate 1 after |
| [phase2-build](phase2-build/config.json) | atlas | 6 (frontend, backend, infra, data-engineer, ai-engineer, mcp-server) | ARB Gate 2 after |
| [phase3-verification](phase3-verification/config.json) | atlas | 3 (integration, qa, security-engineering) | ARB Gate 3 after |
| [phase4-operational-readiness](phase4-operational-readiness/config.json) | atlas | 3 (reliability, runbooks, cloud-economics) | Final ARB gate → Production |
| [arb-review](arb-review/config.json) | **janus** | 4 (janus-chair, product-owner, security, cloud-economics) | Spawned at each gate |

## Lifecycle Flow

```
[orchestrator]
      │
      ▼
Phase 0: Intake          ──► ARB Gate 0 ──► Phase 1: Architecture
Phase 1: Architecture    ──► ARB Gate 1 ──► Phase 2: Build
Phase 2: Build           ──► ARB Gate 2 ──► Phase 3: Verification
Phase 3: Verification    ──► ARB Gate 3 ──► Phase 4: Operational Readiness
Phase 4: Op Readiness    ──► Final Gate  ──► Production Release
```

The orchestrator detects the current phase from `.sisyphus/state/`, sequences wave ordering within phases, invokes `arb-review` at each gate, and routes CONDITIONAL/REJECTED outcomes back to the responsible members.

## Wave Ordering

Two phases have intra-phase dependencies that the lead must enforce:

### Phase 1 — Architecture

| Wave | Members | Prerequisite |
|------|---------|-------------|
| Wave 1 | backend-arch + infra-arch | None — run in parallel |
| Wave 2 | data-arch + agent-arch | 2+ ADRs in `adrs/` (backend + hosting) |
| Wave 3 | security-arch + cloud-economics | 4+ ADRs + `data/data-model.md` |

Members self-report missing prerequisites by writing `*-waiting.md` to `.sisyphus/evidence/phase1/` and stopping.

### Phase 2 — Build

| Wave | Members | Output |
|------|---------|--------|
| Wave 1 | backend + mcp-server (contracts only) | `api-contracts/openapi.yaml`, `tool-contracts/tools.json`, state marker |
| Wave 2 | all 6 members | Full implementation — frontend + ai-engineer unblocked by Wave 1 |

Write `.sisyphus/state/phase2-contracts-ready.md` after Wave 1 completes. Frontend and ai-engineer check for their contract files and write `*-waiting.md` + stop if absent.

## Knowledge Repository

All teams read from and write to `.sisyphus/knowledge/`:

```
.sisyphus/
├── state/                        # Orchestrator phase markers
│   ├── phase0-gate-approved.md
│   ├── phase1-gate-approved.md
│   ├── phase2-contracts-ready.md
│   ├── phase2-gate-approved.md
│   ├── phase3-gate-approved.md
│   ├── production-approved.md
│   ├── economics-summary.md
│   └── escalated.md              # Written if ARB deadlocks
├── knowledge/
│   ├── business-intent/          # Phase 0 outputs
│   │   ├── problem-statement.md
│   │   └── success-metrics.md
│   ├── constraints/              # Phase 0 outputs
│   │   ├── budget.md
│   │   └── compliance-scope.md
│   ├── adrs/                     # Phase 1 outputs, amended in Phase 2+
│   │   ├── registry.md
│   │   └── ADR-NNN-title.md
│   ├── data/                     # Phase 1 data-arch output
│   │   └── data-model.md
│   ├── api-contracts/            # Phase 2 Wave 1 — backend output
│   │   ├── openapi.yaml
│   │   └── contract-summary.md
│   ├── tool-contracts/           # Phase 2 Wave 1 — mcp-server output
│   │   ├── tools.json
│   │   └── contract-summary.md
│   ├── security/                 # Phase 1 + Phase 3 outputs
│   │   ├── threat-model.md
│   │   ├── security-review.md
│   │   └── sentinel-design.md
│   ├── cost-estimates/           # Phase 1 + Phase 4 outputs
│   │   ├── architecture-azure.md
│   │   ├── agent-economics/
│   │   │   ├── budget-baseline.md
│   │   │   ├── phase1-report.md
│   │   │   ├── phase2-report.md
│   │   │   ├── phase3-report.md
│   │   │   └── phase4-final.md
│   │   └── final-azure-report.md
│   ├── agent-economics/          # Phase 1 planning outputs
│   │   ├── budget-baseline.md
│   │   └── eval-plan.md
│   ├── reliability/              # Phase 4
│   │   └── slos.md
│   ├── risks/                    # Initialized Phase 0, updated each phase
│   │   └── registry.md
│   ├── runbooks/                 # Phase 4
│   │   ├── deployment-runbook.md
│   │   ├── incident-response.md
│   │   └── backup-restore.md
│   └── arb/                      # Gate review outputs
│       └── {phase}-gate/
│           ├── checklist.md
│           ├── outcome.md
│           └── votes/
│               ├── product-owner-vote.md
│               ├── security-vote.md
│               └── cloud-economics-vote.md
└── evidence/
    ├── phase1/                   # Waiting files from stalled members
    │   └── *-waiting.md
    ├── phase2/                   # Build artifacts + waiting files
    │   ├── backend-contracts-ready.md
    │   ├── mcp-contracts-ready.md
    │   ├── *-waiting.md
    │   ├── frontend/
    │   ├── backend/
    │   ├── infra/
    │   ├── data/
    │   ├── ai-agent/
    │   └── mcp-server/
    ├── phase3/                   # Verification results
    │   ├── integration/
    │   ├── qa/
    │   └── security/
    └── phase4/                   # Operational readiness evidence
        ├── reliability/
        └── runbooks/
```

## ARB Vote Outcomes

Gate outcomes: `APPROVED` / `CONDITIONAL` / `REJECTED` / `ESCALATED`

- **APPROVED** (4/5 required): write state marker, proceed to next phase
- **CONDITIONAL** (3/5): mandatory revisions listed; re-invoke only affected members; fast-track re-review (Janus + Cloud Economics for minor changes)
- **REJECTED** (2+/5): phase must be partially or fully redone; orchestrator maps rejection reasons to responsible members
- **ESCALATED**: ARB deadlock → write `escalated.md` → surface to human arbiter

## Agent Economics Budgets

These are baseline estimates. Adjust `budget-baseline.md` in Phase 0 for your actual project scope.

| Phase | Token Budget | Max Retry Loops | Max Human Interventions |
|-------|-------------|-----------------|------------------------|
| Phase 0 | 20k | 3 | 2 |
| Phase 1 | 250k | 5 | 3 |
| Phase 2 | 800k | 5 | 3 |
| Phase 3 | 300k | 5 | 3 |
| Phase 4 | 200k | 5 | 3 |
| **Total** | **~1.6M** | | |

At current Claude Opus pricing (~$15/$75 input/output per million tokens, ~40% output ratio), a full lifecycle costs approximately $60–$120 USD depending on retry frequency.

## ADR Amendment Process

If a Phase 2+ builder finds an ADR is impractical:

1. Builder notifies the lead — does not silently deviate
2. Orchestrator invokes `arb-review` for a targeted ADR amendment review
3. Fast-track (Janus + Cloud Economics only) if: < 10% cost impact, no new security risks, no new scope
4. Full ARB if: > 10% cost impact OR new security risks OR scope change
5. ADR is updated and re-versioned in `adrs/registry.md` before build resumes
