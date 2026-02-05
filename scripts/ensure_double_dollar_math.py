#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FENCE_RE = re.compile(r"^\s*(```|~~~)")

# Matches inline math: $...$ but NOT $$...$$ and NOT escaped \$.
# We intentionally keep it single-line and disallow $ inside, because in this repo
# math is expected to be simple inline snippets.
INLINE_SINGLE_DOLLAR_MATH_RE = re.compile(r"(?<!\\)\$(?!\$)([^$\n]+?)(?<!\\)\$")
TOO_MANY_DOLLARS_RE = re.compile(r"\${3,}")


def _split_inline_code(line: str) -> list[tuple[bool, str]]:
    """
    Split a line into [(is_code, text)] parts based on backticks.
    This is a simple, practical splitter for Markdown inline code.
    """
    parts: list[tuple[bool, str]] = []
    buf: list[str] = []
    in_code = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "`":
            # Flush current buffer.
            if buf:
                parts.append((in_code, "".join(buf)))
                buf = []

            # Consume a run of backticks.
            j = i
            while j < len(line) and line[j] == "`":
                j += 1

            # Keep the delimiter itself as part of the output (code or non-code).
            parts.append((False, line[i:j]))
            in_code = not in_code
            i = j
            continue

        buf.append(ch)
        i += 1

    if buf:
        parts.append((in_code, "".join(buf)))
    return parts


def _fix_line(line: str) -> tuple[str, bool]:
    changed = False
    out: list[str] = []

    for is_code, chunk in _split_inline_code(line):
        if is_code:
            out.append(chunk)
            continue

        new_chunk = INLINE_SINGLE_DOLLAR_MATH_RE.sub(r"$$\1$$", chunk)
        new_chunk = TOO_MANY_DOLLARS_RE.sub("$$", new_chunk)
        if new_chunk != chunk:
            changed = True
        out.append(new_chunk)

    return "".join(out), changed


def process_file(path: Path, fix: bool) -> tuple[bool, bool, list[tuple[int, str]]]:
    """Returns (changed, failed, violations)."""
    violations: list[tuple[int, str]] = []
    in_fence = False
    changed = False

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as exc:  # pragma: no cover
        print(f"[double-dollar-math] Could not read {path}: {exc}", file=sys.stderr)
        return False, True, [(0, "unreadable file")]

    for idx, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # Detect violations first (on the original line), so we can report even if fix=False.
        # Skip inline code chunks.
        for is_code, chunk in _split_inline_code(line):
            if is_code:
                continue
            if INLINE_SINGLE_DOLLAR_MATH_RE.search(chunk):
                violations.append((idx, line.rstrip()))
                break
            if TOO_MANY_DOLLARS_RE.search(chunk):
                violations.append((idx, line.rstrip()))
                break

        if fix:
            new_line, line_changed = _fix_line(line)
            if line_changed:
                lines[idx - 1] = new_line
                changed = True

    if fix and changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    failed = bool(violations)
    return changed, failed, violations


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true", help="Auto-fix $...$ -> $$...$$ (and normalize $$$)")
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
        if has_violations and not args.fix:
            failed = True
            for line_no, line in violations:
                print(
                    f"[double-dollar-math] {path}:{line_no} inline math uses single '$'.",
                    file=sys.stderr,
                )
                print(f"  {line}", file=sys.stderr)

    if args.fix and changed_any:
        print(
            "[double-dollar-math] Normalized math dollars. Please re-stage changes.",
            file=sys.stderr,
        )
        return 1

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
