#!/usr/bin/env python3
"""Sync autoformalization taxonomy with summaries.

- Adds missing agents/tools with names ending in '*' (needs human review).
- Removes agents/tools not referenced in any summary.
- Fails (exit 1) if any changes were made or any entry name ends with '*'.
"""

import sys
import re
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TAXONOMY_PATH = REPO_ROOT / "_data" / "autoformalization_taxonomy.yml"
SUMMARIES_DIR = REPO_ROOT / "_summaries"


def id_to_name(id_str: str) -> str:
    """Convert snake_case / mixed-case id to Title Case name with trailing '*'."""
    return " ".join(word.capitalize() for word in re.split(r"[_\-]", id_str)) + "*"


def parse_frontmatter(content: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def collect_used_ids():
    used_agents: set[str] = set()
    used_tools: set[str] = set()
    used_datasets: set[str] = set()

    for md_path in SUMMARIES_DIR.glob("*.md"):
        content = md_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        if "autoformalization" not in (fm.get("categories") or []):
            continue
        for agent_id in fm.get("af_agents") or []:
            used_agents.add(str(agent_id))
        for tool_id in fm.get("af_tools") or []:
            used_tools.add(str(tool_id))
        for dataset_id in fm.get("af_datasets") or []:
            used_datasets.add(str(dataset_id))

    return used_agents, used_tools, used_datasets


def dump_taxonomy(data: dict) -> str:
    lines = []
    for section in ("agents", "tools", "datasets"):
        lines.append(f"{section}:")
        for entry in data.get(section, []):
            lines.append(f"  - id: {entry['id']}")
            lines.append(f"    name: {entry['name']}")
    return "\n".join(lines) + "\n"


def main():
    used_agents, used_tools, used_datasets = collect_used_ids()

    raw = TAXONOMY_PATH.read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}

    changed = False
    has_star = False
    messages = []

    for section, used_ids in [("agents", used_agents), ("tools", used_tools), ("datasets", used_datasets)]:
        existing = list(data.get(section) or [])
        existing_ids = {e["id"] for e in existing}

        # Add missing entries with '*' name to signal they need review
        for mid in sorted(used_ids - existing_ids):
            name = id_to_name(mid)
            existing.append({"id": mid, "name": name})
            messages.append(f"  [ADDED] {section[:-1]} '{mid}' -> '{name}'")
            changed = True

        # Remove entries not referenced in any summary
        unused = existing_ids - used_ids
        if unused:
            existing = [e for e in existing if e["id"] not in unused]
            for uid in sorted(unused):
                messages.append(f"  [REMOVED] {section[:-1]} '{uid}' (unused)")
            changed = True

        data[section] = existing

        for e in existing:
            if str(e["name"]).endswith("*"):
                has_star = True
                messages.append(
                    f"  [NEEDS REVIEW] {section[:-1]} '{e['id']}' has name '{e['name']}'"
                )

    if changed:
        TAXONOMY_PATH.write_text(dump_taxonomy(data), encoding="utf-8")
        print("Taxonomy was updated — stage the changes and commit again.")
        for m in messages:
            print(m)
        sys.exit(1)

    if has_star:
        print("Taxonomy has entries whose names end with '*' — replace them with real names first.")
        for m in messages:
            print(m)
        sys.exit(1)

    print("Taxonomy OK.")
    sys.exit(0)


if __name__ == "__main__":
    main()
