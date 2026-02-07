#!/usr/bin/env python3
from __future__ import annotations

import io
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image

MAX_BYTES = 500 * 1024
TARGET_BYTES = 480 * 1024


@dataclass(frozen=True)
class Candidate:
    label: str
    rank: int
    size: int
    data: bytes


def _encode_png(img: Image.Image, *, optimize: bool = True) -> bytes:
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=optimize, compress_level=9)
    return buffer.getvalue()


def _add_candidate(candidates: list[Candidate], label: str, rank: int, img: Image.Image) -> None:
    data = _encode_png(img)
    candidates.append(Candidate(label=label, rank=rank, size=len(data), data=data))


def _quantize_candidates(base: Image.Image, colors: Iterable[int]) -> list[Image.Image]:
    base_mode = "RGBA" if "A" in base.getbands() else "RGB"
    base = base.convert(base_mode)
    quantized = []
    for count in colors:
        quantized.append(
            base.quantize(
                colors=count,
                method=Image.FASTOCTREE,
                dither=Image.FLOYDSTEINBERG,
            )
        )
    return quantized


def _resize(base: Image.Image, scale: float) -> Image.Image:
    width, height = base.size
    new_size = (max(1, int(width * scale)), max(1, int(height * scale)))
    return base.resize(new_size, resample=Image.LANCZOS)


def _select_best(candidates: list[Candidate]) -> Candidate | None:
    valid = [c for c in candidates if c.size <= MAX_BYTES]
    if not valid:
        return None

    prefer = [c for c in valid if c.size >= TARGET_BYTES]
    pool = prefer if prefer else valid
    return min(pool, key=lambda c: (c.rank, abs(c.size - TARGET_BYTES), -c.size))


def _process_file(path: Path) -> bool:
    original_size = path.stat().st_size
    if original_size <= MAX_BYTES:
        return True

    try:
        img = Image.open(path)
        img.load()
    except Exception as exc:  # pragma: no cover - diagnostics only
        print(f"[shrink-png] Failed to read {path}: {exc}", file=sys.stderr)
        return False

    candidates: list[Candidate] = []
    _add_candidate(candidates, "optimize", 0, img)

    for idx, quantized in enumerate(_quantize_candidates(img, [256, 128, 64]), start=1):
        _add_candidate(candidates, f"quantize-{idx}", 1, quantized)

    base = img.convert("RGBA") if "A" in img.getbands() else img.convert("RGB")
    for scale in (0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4):
        resized = _resize(base, scale)
        _add_candidate(candidates, f"resize-{scale:.2f}", 2, resized)
        for quantized in _quantize_candidates(resized, [256]):
            _add_candidate(candidates, f"resize-{scale:.2f}-quant256", 3, quantized)

    best = _select_best(candidates)
    if best is None:
        print(
            f"[shrink-png] Could not reduce {path} below {MAX_BYTES // 1024}KB",
            file=sys.stderr,
        )
        return False

    if best.size >= original_size:
        print(
            f"[shrink-png] {path} remains {best.size / 1024:.1f}KB; no reduction found",
            file=sys.stderr,
        )
        return False

    path.write_bytes(best.data)
    print(
        f"[shrink-png] {path} {original_size / 1024:.1f}KB -> {best.size / 1024:.1f}KB ({best.label})"
    )
    return True


def main(argv: list[str]) -> int:
    if not argv:
        return 0

    ok = True
    for arg in argv:
        if not arg.lower().endswith(".png"):
            continue
        path = Path(arg)
        if path.exists():
            ok = _process_file(path) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
