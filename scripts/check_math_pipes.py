#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PIPE_IN_SINGLE_LINE_DISPLAY = re.compile(r"\$\$[^$]*\|[^$]*\$\$")
INLINE_MATH_RE = re.compile(r"\$(?!\$)([^$]+)\$")
DISPLAY_MATH_INLINE_RE = re.compile(r"\$\$([^$]+)\$\$")
COMMAND_RE = re.compile(r"\\([A-Za-z]+)")
DOUBLE_BACKSLASH_RE = re.compile(r"\\\\")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
PIPE_WITH_SPACES = re.compile(r"\s\|\s")
ABS_BAR = re.compile(r"\|([^|\n]+?)\|")

COMMANDS_PATH = Path(__file__).with_name("latex_commands.txt")


def _fix_line(line: str) -> str:
    fixed = PIPE_WITH_SPACES.sub(lambda _: " \\mid ", line)
    fixed = ABS_BAR.sub(lambda m: f"\\lvert {m.group(1)} \\rvert", fixed)
    return fixed


def _load_commands() -> set[str]:
    if not COMMANDS_PATH.exists():
        return set()
    return {
        line.strip()
        for line in COMMANDS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def _math_segments(line: str, in_display: bool) -> tuple[list[str], bool]:
    segments: list[str] = []
    if in_display:
        segments.append(line)

    for match in DISPLAY_MATH_INLINE_RE.finditer(line):
        segments.append(match.group(1))

    for match in INLINE_MATH_RE.finditer(line):
        segments.append(match.group(1))

    if line.count("$$") % 2 == 1:
        in_display = not in_display

    return segments, in_display


def process_file(path: Path, fix: bool, commands: set[str]) -> tuple[bool, bool, list[tuple[int, str, str]]]:
    """Returns (changed, failed, violations)."""
    violations: list[tuple[int, str, str]] = []
    in_fence = False
    in_display = False
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

        segments, in_display = _math_segments(line, in_display)
        for segment in segments:
            if DOUBLE_BACKSLASH_RE.search(segment):
                violations.append((idx, line.rstrip(), "double-backslash"))

            for cmd in COMMAND_RE.findall(segment):
                if cmd not in commands:
                    violations.append((idx, line.rstrip(), f"unknown-command: \\{cmd}"))

        if PIPE_IN_SINGLE_LINE_DISPLAY.search(line):
            violations.append((idx, line.rstrip(), "pipe-in-display-math"))
            if fix:
                new_line = _fix_line(line)
                if new_line != line:
                    lines[idx - 1] = new_line
                    changed = True

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

    commands = _load_commands()
    if not commands:
        print(
            f"[math-pipes] Missing command list at {COMMANDS_PATH}.",
            file=sys.stderr,
        )
        return 1

    failed = False
    changed_any = False
    for path in files:
        changed, has_violations, violations = process_file(path, fix=args.fix, commands=commands)
        changed_any = changed_any or changed
        if has_violations:
            failed = True
            for line_no, line, reason in violations:
                print(
                    f"[math-pipes] {path}:{line_no} invalid math: {reason}.",
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
