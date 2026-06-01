#!/usr/bin/env python3
"""
tally_votes.py — Tally ARB votes and write the outcome report.

Usage:
    python scripts/tally_votes.py [config_path] [--dry-run]

    config_path : path to arb config yaml (default: .arb/config.yml)
    --dry-run   : print outcome without writing arb-outcome.md

Reads all votes/<name>.md files, applies quorum rules, determines outcome,
and writes arb-outcome.md alongside the config file.

Exit codes:
    0 — approved
    1 — rejected
    2 — insufficient quorum
    3 — deadlock
    4 — config or vote-file error
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required.  pip install pyyaml", file=sys.stderr)
    sys.exit(4)


VALID_VOTES = {"approve", "reject", "abstain", "conditional", "pending"}

OUTCOME_LABELS: dict[str, str] = {
    "approved": "APPROVED",
    "rejected": "REJECTED",
    "conditional": "CONDITIONAL",
    "deadlock": "DEADLOCK",
    "insufficient-quorum": "INSUFFICIENT QUORUM",
}

EXIT_CODES: dict[str, int] = {
    "approved": 0,
    "rejected": 1,
    "insufficient-quorum": 2,
    "deadlock": 3,
    "conditional": 5,
}

OUTCOME_TEMPLATE = """\
---
proposal: {proposal}
outcome: {outcome}
tallied_at: {tallied_at}
quorum_met: {quorum_met}
approve_count: {approve_count}
reject_count: {reject_count}
conditional_count: {conditional_count}
abstain_count: {abstain_count}
pending_count: {pending_count}
evidence_failed_count: {evidence_failed_count}
---

# ARB Outcome: {proposal}

## Result: {outcome_label}

{outcome_note}

## Vote Summary

| Voter | Role | Type | Vote | Voted At |
|-------|------|------|------|----------|
{vote_rows}

## Tally

| Decision | Count |
|----------|-------|
| Approve  | {approve_count} |
| Reject   | {reject_count} |
| Abstain  | {abstain_count} |
| Pending  | {pending_count} |

## Quorum Check

{quorum_detail}

## Next Steps

{next_steps}
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_config(path: Path) -> dict:
    if not path.exists():
        print(f"ERROR: Config not found: {path}", file=sys.stderr)
        sys.exit(4)
    with open(path, encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(f"ERROR: Invalid YAML in {path}: {exc}", file=sys.stderr)
            sys.exit(4)
    if not data or "arb" not in data:
        print(f"ERROR: Missing 'arb' key in {path}", file=sys.stderr)
        sys.exit(4)
    return data


def parse_frontmatter(path: Path) -> dict:
    """Return YAML frontmatter dict from a Markdown file, or {} on failure."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def has_rationale(path: Path) -> bool:
    """Return True if the vote file contains non-empty rationale text."""
    text = path.read_text(encoding="utf-8")
    # Strip frontmatter
    body = re.sub(r"^---[ \t]*\n.*?\n---[ \t]*\n", "", text, count=1, flags=re.DOTALL)
    # Find Rationale section
    m = re.search(r"##\s+Rationale\s*\n(.*?)(?=\n##|\Z)", body, re.DOTALL | re.IGNORECASE)
    if not m:
        return False
    rationale_body = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.DOTALL).strip()
    return bool(rationale_body)


def check_evidence(config_path: Path, voter: dict) -> list[str]:
    """Check evidence_required paths exist. Returns list of missing paths."""
    # Project root: walk up from config until we find .sisyphus/ or .git/
    project_root = config_path.parent
    while project_root.parent != project_root:
        if (project_root / ".sisyphus").exists() or (project_root / ".git").exists():
            break
        project_root = project_root.parent

    missing = []
    for ev_path in voter.get("evidence_required", []):
        full = (project_root / ev_path).resolve()
        if not full.exists():
            missing.append(ev_path)
    return missing


def load_votes(votes_dir: Path, all_voters: list[dict], config_path: Path) -> list[dict]:
    results: list[dict] = []
    for voter in all_voters:
        name = voter.get("name", "unknown").strip()
        vote_file = votes_dir / f"{name}.md"

        if not vote_file.exists():
            results.append({
                "name": name,
                "role": voter.get("role", "Unknown"),
                "voter_type": voter["voter_type"],
                "vote": "pending",
                "voted_at": None,
                "evidence_missing": [],
            })
            continue

        fm = parse_frontmatter(vote_file)
        raw_vote = str(fm.get("vote", "pending")).strip().lower()

        if raw_vote not in VALID_VOTES:
            print(f"WARNING: Invalid vote '{raw_vote}' in {vote_file} — treating as pending.", file=sys.stderr)
            raw_vote = "pending"

        # Validate reject has rationale
        if raw_vote == "reject" and not has_rationale(vote_file):
            print(f"WARNING: {name} voted reject but rationale is blank — treating as pending.", file=sys.stderr)
            raw_vote = "pending"

        # Evidence gate — check evidence_required before counting the vote
        evidence_missing = check_evidence(config_path, voter)
        if evidence_missing:
            print(f"WARNING: {name} missing required evidence: {', '.join(evidence_missing)} — treating as pending.", file=sys.stderr)
            raw_vote = "pending"

        results.append({
            "name": name,
            "role": voter.get("role", fm.get("role", "Unknown")),
            "voter_type": voter["voter_type"],
            "vote": raw_vote,
            "voted_at": fm.get("voted_at"),
            "evidence_missing": evidence_missing,
        })
    return results


# ---------------------------------------------------------------------------
# Quorum and outcome
# ---------------------------------------------------------------------------

def compute_quorum(config: dict, votes: list[dict]) -> dict:
    arb = config["arb"]
    qcfg = arb.get("quorum", {})
    required_names = {v["name"] for v in arb.get("required_voters", [])}
    count_abstain: bool = bool(qcfg.get("count_abstain", False))
    min_req: int = int(qcfg.get("min_required_voters", len(required_names)))
    min_total: int = int(qcfg.get("min_total_votes", 1))
    threshold: float = float(qcfg.get("approval_threshold", 0.51))

    approve    = [v for v in votes if v["vote"] == "approve"]
    reject     = [v for v in votes if v["vote"] == "reject"]
    abstain    = [v for v in votes if v["vote"] == "abstain"]
    condition  = [v for v in votes if v["vote"] == "conditional"]
    pending    = [v for v in votes if v["vote"] == "pending"]

    # Evidence gate — voters with missing evidence stay in the required count
    # but cannot vote. This means the gate HARD BLOCKS: evidence-failed voters
    # count toward quorum requirements but never toward voted.
    evidence_failed = [v for v in votes if v["name"] in required_names and v.get("evidence_missing")]
    evidence_failed_count = len(evidence_failed)
    evidence_failed_names = [v["name"] for v in evidence_failed]

    required_voted   = [v for v in votes if v["name"] in required_names and v["vote"] != "pending"]
    required_pending = [v for v in votes if v["name"] in required_names and v["vote"] == "pending"]

    # Conditional votes count toward quorum but not toward approve/reject rate
    counted = len(approve) + len(reject) + len(condition) + (len(abstain) if count_abstain else 0)
    quorum_met = len(required_voted) >= min_req and counted >= min_total

    return {
        "quorum_met":          quorum_met,
        "approve_count":       len(approve),
        "reject_count":        len(reject),
        "abstain_count":       len(abstain),
        "conditional_count":   len(condition),
        "pending_count":       len(pending),
        "counted":             counted,
        "required_voted":      len(required_voted),
        "required_total":      len(required_names),
        "evidence_failed_count": evidence_failed_count,
        "evidence_failed_names": evidence_failed_names,
        "required_pending":    [v["name"] for v in required_pending if v["name"] not in evidence_failed_names],
        "min_req":             min_req,
        "min_total":           min_total,
        "threshold":           threshold,
        "count_abstain":       count_abstain,
    }


def determine_outcome(q: dict) -> str:
    if not q["quorum_met"]:
        return "insufficient-quorum"
    if q["counted"] == 0:
        return "insufficient-quorum"

    # Reject takes priority over conditional
    if q["reject_count"] > 0:
        return "rejected"

    # If any voter cast a conditional vote, the outcome is conditional
    if q["conditional_count"] > 0:
        return "conditional"

    # Standard approve/reject rate check
    decision_count = q["approve_count"] + q["reject_count"]
    if decision_count == 0:
        return "insufficient-quorum"
    approve_rate = q["approve_count"] / decision_count
    if approve_rate >= q["threshold"]:
        return "approved"
    return "deadlock"


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def fmt_quorum_detail(q: dict) -> str:
    chk = lambda ok: "✓" if ok else "✗"
    req_ok   = q["required_voted"] >= q["min_req"]
    total_ok = q["counted"] >= q["min_total"]
    lines = [
        f"- Required voters voted   : {q['required_voted']}/{q['required_total']} "
        f"(effective minimum: {q['min_req']}) {chk(req_ok)}",
        f"- Total votes counted     : {q['counted']} "
        f"(effective minimum: {q['min_total']}) {chk(total_ok)}",
    ]
    if q["evidence_failed_count"]:
        lines.append(f"- Evidence gate blocked  : {q['evidence_failed_count']} voter(s) — {', '.join(q['evidence_failed_names'])}")
    if q["pending_count"] and q["required_pending"]:
        lines.append(f"- Required pending       : {', '.join(q['required_pending'])}")
    if q["counted"] > 0:
        pct = q["approve_count"] / q["counted"]
        lines.append(f"- Approval rate          : {pct:.0%} (threshold: {q['threshold']:.0%})")
    lines.append(f"- Quorum met             : {'Yes' if q['quorum_met'] else 'No'}")
    return "\n".join(lines)


def fmt_outcome_note(outcome: str) -> str:
    return {
        "approved":            "> This proposal has been **approved** by the Architecture Review Board.",
        "rejected":            "> This proposal has been **rejected**. See rejection rationales in the vote files.",
        "conditional":         "> This proposal has been **conditionally approved**. Mandatory revisions are listed below.",
        "deadlock":            "> The vote is in **deadlock**. No threshold was reached. Escalation is required.",
        "insufficient-quorum": "> **Insufficient quorum.** Not all required voters have cast their vote. Outcome is not final.",
    }.get(outcome, "")


def fmt_next_steps(outcome: str, q: dict, config: dict) -> str:
    arb = config["arb"]
    dl = arb.get("deadlock", {})
    escalate_to   = dl.get("escalate_to", "escalation owner")
    escalate_days = dl.get("escalation_days", 3)

    if outcome == "approved":
        return (
            "- Merge the proposal.\n"
            "- Archive vote files to `votes/archive/`.\n"
            "- Close the ARB review ticket."
        )
    if outcome == "rejected":
        return (
            "- Do not merge.\n"
            "- Review rejection rationales in the vote files.\n"
            "- Revise the proposal and re-initiate a new ARB vote if appropriate."
        )
    if outcome == "insufficient-quorum":
        lines = ["- Chase pending required voters:"]
        for name in q["required_pending"]:
            lines.append(f"  - {name}: update `votes/{name}.md`")
        lines.append("- Re-run `tally_votes.py` once all required voters have voted.")
        return "\n".join(lines)
    if outcome == "deadlock":
        return (
            f"- Escalate to **{escalate_to}** within {escalate_days} working days.\n"
            f"- See [Escalation Policy](standards/escalation-policy.md).\n"
            f"- Follow [Escalate Deadlock](actions/escalate-deadlock.md) checklist."
        )
    return "- Review outcome and follow up accordingly."


def fmt_vote_rows(votes: list[dict]) -> str:
    rows = []
    for v in votes:
        voted_at = str(v["voted_at"]) if v["voted_at"] else "—"
        row = f"| {v['name']} | {v['role']} | {v['voter_type']} | {v['vote'].upper()} | {voted_at} |"
        rows.append(row)
    return "\n".join(rows)


def fmt_evidence_details(votes: list[dict]) -> str:
    """Return evidence gate detail lines."""
    lines = []
    for v in votes:
        if v.get("evidence_missing"):
            lines.append(f"- **{v['name']}**: missing evidence — {', '.join(v['evidence_missing'])}")
    if lines:
        lines.insert(0, "\n## Evidence Gate\n")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_outcome(
    config_path: Path,
    config: dict,
    votes: list[dict],
    q: dict,
    outcome: str,
    dry_run: bool,
) -> None:
    proposal = config["arb"].get("proposal") or "Unnamed Proposal"
    tallied_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    content = OUTCOME_TEMPLATE.format(
        proposal=proposal,
        outcome=outcome,
        outcome_label=OUTCOME_LABELS.get(outcome, outcome.upper()),
        tallied_at=tallied_at,
        quorum_met=str(q["quorum_met"]).lower(),
        approve_count=q["approve_count"],
        reject_count=q["reject_count"],
        conditional_count=q["conditional_count"],
        abstain_count=q["abstain_count"],
        pending_count=q["pending_count"],
        evidence_failed_count=q["evidence_failed_count"],
        outcome_note=fmt_outcome_note(outcome),
        vote_rows=fmt_vote_rows(votes),
        quorum_detail=fmt_quorum_detail(q),
        next_steps=fmt_next_steps(outcome, q, config),
    )

    if dry_run:
        print("=== DRY RUN — arb-outcome.md would contain: ===\n")
        print(content)
        return

    outcome_path = config_path.parent / "arb-outcome.md"
    outcome_path.write_text(content, encoding="utf-8")
    print(f"Wrote: {outcome_path}")


def print_summary(outcome: str, q: dict) -> None:
    label = OUTCOME_LABELS.get(outcome, outcome.upper())
    print(f"\nOutcome  : {label}")
    print(f"  Approve  : {q['approve_count']}")
    print(f"  Reject   : {q['reject_count']}")
    print(f"  Conditional : {q['conditional_count']}")
    print(f"  Abstain  : {q['abstain_count']}")
    print(f"  Pending  : {q['pending_count']} (includes {q['evidence_failed_count']} evidence failures)")
    print(f"  Quorum   : {'met' if q['quorum_met'] else 'NOT MET'}")


# ---------------------------------------------------------------------------
# Phase auto-advance
# ---------------------------------------------------------------------------

def try_advance_phase(config_path: Path, outcome: str) -> None:
    """Auto-advance the phase lock if the outcome allows it."""
    if outcome not in ("approved", "conditional"):
        return
    # Walk up from config to find project root
    project = config_path.parent
    while project.parent != project:
        if (project / ".sisyphus").exists():
            break
        project = project.parent
    adv = project / ".sisyphus" / "advance_phase.py"
    if not adv.exists():
        return
    import subprocess
    print("  Advancing phase lock...")
    result = subprocess.run(
        [sys.executable, str(adv), str(config_path)],
        capture_output=True, text=True, cwd=project
    )
    for line in result.stdout.splitlines():
        print(f"    {line}")
    if result.returncode != 0:
        print(f"    Phase advance skipped (exit {result.returncode}): {result.stderr.strip()}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    raw_args = sys.argv[1:]
    dry_run = "--dry-run" in raw_args
    no_advance = "--no-advance" in raw_args
    positional = [a for a in raw_args if not a.startswith("--")]

    config_path = Path(positional[0]) if positional else Path(".arb/config.yml")
    config = load_config(config_path)
    arb = config["arb"]

    all_voters: list[dict] = [
        {**v, "voter_type": "required"} for v in arb.get("required_voters", [])
    ] + [
        {**v, "voter_type": "optional"} for v in arb.get("optional_voters", [])
    ]

    votes_dir = config_path.parent / "votes"
    votes = load_votes(votes_dir, all_voters, config_path)
    q = compute_quorum(config, votes)
    outcome = determine_outcome(q)

    write_outcome(config_path, config, votes, q, outcome, dry_run)
    print_summary(outcome, q)

    if not dry_run and not no_advance:
        try_advance_phase(config_path, outcome)

    sys.exit(EXIT_CODES.get(outcome, 4))


if __name__ == "__main__":
    main()
