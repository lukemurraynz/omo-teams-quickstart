#!/usr/bin/env python3
"""
check_quorum.py — Report quorum status without writing the outcome.

Usage:
    python scripts/check_quorum.py [config_path]

    config_path: path to arb config yaml (default: .arb/config.yml)

Reads all votes/<name>.md files and prints a quorum status report.
Does NOT write arb-outcome.md. Use tally_votes.py to finalize.

Exit codes:
    0 — quorum met
    1 — quorum not met (pending votes remain or threshold not reachable)
    2 — config error
"""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required.  pip install pyyaml", file=sys.stderr)
    sys.exit(2)


VALID_VOTES = {"approve", "reject", "abstain", "pending"}
ICON = {"approve": "✓", "reject": "✗", "abstain": "~", "pending": "?"}


def load_config(path: Path) -> dict:
    if not path.exists():
        print(f"ERROR: Config not found: {path}", file=sys.stderr)
        sys.exit(2)
    with open(path, encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(f"ERROR: Invalid YAML in {path}: {exc}", file=sys.stderr)
            sys.exit(2)
    if not data or "arb" not in data:
        print(f"ERROR: Missing 'arb' key in {path}", file=sys.stderr)
        sys.exit(2)
    return data


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def read_vote(name: str, votes_dir: Path) -> str:
    vote_file = votes_dir / f"{name}.md"
    if not vote_file.exists():
        return "pending"
    fm = parse_frontmatter(vote_file)
    raw = str(fm.get("vote", "pending")).strip().lower()
    return raw if raw in VALID_VOTES else "pending"


def main() -> None:
    config_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".arb/config.yml")
    config = load_config(config_path)
    arb = config["arb"]
    qcfg = arb.get("quorum", {})

    proposal = arb.get("proposal") or "Unnamed Proposal"
    required_voters = arb.get("required_voters", [])
    optional_voters = arb.get("optional_voters", [])
    required_names  = {v["name"] for v in required_voters}

    min_req: int    = int(qcfg.get("min_required_voters", len(required_voters)))
    min_total: int  = int(qcfg.get("min_total_votes", 1))
    threshold: float = float(qcfg.get("approval_threshold", 0.51))
    count_abstain: bool = bool(qcfg.get("count_abstain", False))

    votes_dir = config_path.parent / "votes"
    all_voters = (
        [{**v, "voter_type": "required"} for v in required_voters]
        + [{**v, "voter_type": "optional"} for v in optional_voters]
    )

    print(f"ARB Quorum Status: {proposal}")
    print("=" * 60)
    print()

    approve = reject = abstain = pending = 0
    required_voted_count = 0
    pending_required: list[str] = []

    print("Voters:")
    for voter in all_voters:
        name  = voter.get("name", "unknown").strip()
        role  = voter.get("role", "Unknown")
        vtype = voter["voter_type"]
        vote  = read_vote(name, votes_dir)

        icon = ICON.get(vote, "?")
        req_label = "[REQUIRED]" if vtype == "required" else "[optional]"
        print(f"  {icon} {req_label:10s} {name} ({role}): {vote}")

        if vote == "approve":
            approve += 1
        elif vote == "reject":
            reject += 1
        elif vote == "abstain":
            abstain += 1
        else:
            pending += 1

        if name in required_names:
            if vote != "pending":
                required_voted_count += 1
            else:
                pending_required.append(name)

    counted = approve + reject + (abstain if count_abstain else 0)

    print()
    print("Tally:")
    print(f"  Approve  : {approve}")
    print(f"  Reject   : {reject}")
    print(f"  Abstain  : {abstain}")
    print(f"  Pending  : {pending}")

    print()
    print("Quorum:")
    req_ok   = required_voted_count >= min_req
    total_ok = counted >= min_total
    chk = lambda ok: "✓" if ok else "✗"
    print(f"  Required voters voted : {required_voted_count}/{len(required_voters)} "
          f"(need {min_req}) {chk(req_ok)}")
    print(f"  Total votes counted   : {counted} (need {min_total}) {chk(total_ok)}")
    if counted > 0:
        rate = approve / counted
        print(f"  Approval rate         : {rate:.0%} (threshold: {threshold:.0%})")

    quorum_met = req_ok and total_ok

    print()
    if quorum_met:
        print("Status: QUORUM MET — run tally_votes.py to finalize the outcome.")
    else:
        print("Status: QUORUM NOT MET")
        if pending_required:
            print("  Waiting on required voters:")
            for name in pending_required:
                vfile = votes_dir / f"{name}.md"
                if not vfile.exists():
                    print(f"    - {name}: vote file missing (run create_vote.py)")
                else:
                    print(f"    - {name}: vote is still pending in votes/{name}.md")

    sys.exit(0 if quorum_met else 1)


if __name__ == "__main__":
    main()
