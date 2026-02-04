#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PIPE_IN_SINGLE_LINE_DISPLAY = re.compile(r"\$\$[^$]*\|[^$]*\$\$")
DOUBLE_BACKSLASH_MATH = re.compile(r"\$\$[^$]*\\\\[^$]*\$\$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
PIPE_WITH_SPACES = re.compile(r"\s\|\s")
ABS_BAR = re.compile(r"\|([^|\n]+?)\|")


def _fix_line(line: str) -> str:
    fixed = PIPE_WITH_SPACES.sub(lambda _: " \\mid ", line)
    fixed = ABS_BAR.sub(lambda m: f"\\lvert {m.group(1)} \\rvert", fixed)
    return fixed


def process_file(path: Path, fix: bool) -> tuple[bool, bool, list[tuple[int, str]]]:
    """Returns (changed, failed, violations)."""
    violations: list[tuple[int, str]] = []
    in_fence = False
    changed = False

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as exc:  # pragma: no cover - pre-commit expects stderr
        print(f"[math-pipes] Could not read {path}: {exc}", file=sys.stderr)
        return False, True, [(0, "unreadable file")]

    for idx, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue

        if in_fence:
            continue

        if PIPE_IN_SINGLE_LINE_DISPLAY.search(line):
            violations.append((idx, line.rstrip()))
            if fix:
                new_line = _fix_line(line)
                if new_line != line:
                    lines[idx - 1] = new_line
                    changed = True

        if DOUBLE_BACKSLASH_MATH.search(line):
            violations.append((idx, line.rstrip()))

    if fix and changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    failed = bool(violations)
    return changed, failed, violations


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true", help="Auto-fix simple cases")
    parser.add_argument("files", nargs="*")
    args = parser.parse_args(argv)

    files = [Path(p) for p in args.files if p.strip()]
    if not files:
        return 0

    failed = False
    changed_any = False
    for path in files:
        changed, has_violations, violations = process_file(path, fix=args.fix)
        changed_any = changed_any or changed
        if has_violations:
            failed = True
            for line_no, line in violations:
                print(
                    f"[math-pipes] {path}:{line_no} contains a '|' inside "
                    "$$...$$ on one line. This can render as a table. "
                    "Use \\mid / \\lvert \\rvert or put $$ on its own lines.",
                    file=sys.stderr,
                )
                print(f"  {line}", file=sys.stderr)

    if args.fix and changed_any:
        print(
            "[math-pipes] Applied fixes. Please re-stage changes.",
            file=sys.stderr,
        )
        return 1

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
