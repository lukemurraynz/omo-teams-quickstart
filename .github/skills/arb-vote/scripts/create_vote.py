#!/usr/bin/env python3
"""
create_vote.py — Initialize ARB vote files for all voters in config.

Usage:
    python scripts/create_vote.py [config_path]

    config_path: path to arb config yaml (default: .arb/config.yml)

Creates votes/<voter_name>.md for each required and optional voter.
Skips existing files to preserve already-cast votes.

Exit codes:
    0 — all vote files created (or already exist)
    1 — config file not found or invalid YAML
    2 — no voters defined in config
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


VOTE_TEMPLATE = """\
---
voter: {name}
role: {role}
voter_type: {voter_type}
proposal: {proposal}
vote: pending
voted_at: null
---

# Vote: {name}

**Proposal:** {proposal}
**Role:** {role}

## Decision

Replace `vote: pending` in the frontmatter above with one of:
- `approve` — in favour of this proposal
- `reject` — opposed to this proposal (rationale required below)
- `abstain` — not casting a directional vote

Also update `voted_at` with the current UTC time: `"YYYY-MM-DDTHH:MM:SSZ"`

## Rationale

<!-- Required if vote: reject. Optional for approve/abstain. -->

"""


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        print(f"ERROR: Config not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    with open(config_path, encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"ERROR: Invalid YAML in {config_path}: {e}", file=sys.stderr)
            sys.exit(1)
    if not data or "arb" not in data:
        print(f"ERROR: Missing 'arb' key in {config_path}", file=sys.stderr)
        sys.exit(1)
    return data


def collect_voters(config: dict) -> list[dict]:
    arb = config["arb"]
    voters = []
    for v in arb.get("required_voters", []):
        voters.append({**v, "voter_type": "required"})
    for v in arb.get("optional_voters", []):
        voters.append({**v, "voter_type": "optional"})
    return voters


def create_vote_files(config: dict, votes_dir: Path) -> None:
    arb = config["arb"]
    proposal = arb.get("proposal") or "Unnamed Proposal"
    voters = collect_voters(config)

    if not voters:
        print("ERROR: No voters defined in config (required_voters and optional_voters are both empty).", file=sys.stderr)
        sys.exit(2)

    votes_dir.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    skipped: list[str] = []

    for voter in voters:
        name = voter.get("name", "unknown").strip()
        role = voter.get("role", "Unknown Role")
        voter_type = voter.get("voter_type", "optional")
        vote_file = votes_dir / f"{name}.md"

        if vote_file.exists():
            skipped.append(name)
            continue

        content = VOTE_TEMPLATE.format(
            name=name,
            role=role,
            voter_type=voter_type,
            proposal=proposal,
        )
        vote_file.write_text(content, encoding="utf-8")
        created.append(name)

    print(f"Proposal  : {proposal}")
    print(f"Votes dir : {votes_dir}")
    print()

    if created:
        print(f"Created ({len(created)}):")
        for name in created:
            print(f"  + votes/{name}.md")
    if skipped:
        print(f"Skipped — already exist ({len(skipped)}):")
        for name in skipped:
            print(f"  ~ votes/{name}.md")

    print()
    print(f"Total voters : {len(voters)}  ({len(created)} created, {len(skipped)} skipped)")


def main() -> None:
    config_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".arb/config.yml")
    config = load_config(config_path)
    votes_dir = config_path.parent / "votes"
    create_vote_files(config, votes_dir)


if __name__ == "__main__":
    main()
