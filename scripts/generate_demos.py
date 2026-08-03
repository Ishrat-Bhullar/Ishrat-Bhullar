#!/usr/bin/env python3
"""Compose the interface screenshots into short demonstration GIFs.

The report's figures are stills, so a "walkthrough" is synthesised here: each
shot either holds or pans slowly down a tall screenshot, and consecutive shots
cross-fade. Motion is linear and slow on purpose — the goal is a readable
product tour, not a highlight reel.

Requires ffmpeg on PATH (palette-based quantisation keeps dark UI gradients
from banding). Reads only from assets/images, so it reproduces from the
repository alone.

Usage:  python3 scripts/generate_demos.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "images"
OUT = ROOT / "assets" / "gifs"

FPS = 10
VIEW_W, VIEW_H = 760, 430
FADE_FRAMES = 5

# name -> [(screenshot, mode, seconds)]  where mode is "hold" or "pan"
DEMOS = {
    "vectorless-rag": [
        ("vectorless-interface", "hold", 1.7),
        ("vectorless-response",  "pan",  4.2),
    ],
    "hybrid-rag": [
        ("hybrid-interface",  "hold", 1.7),
        ("hybrid-citations",  "pan",  3.4),
    ],
    "sdlc-platform": [
        ("sdlc-dashboard",    "pan",  3.0),
        ("sdlc-requirements", "hold", 1.8),
        ("sdlc-architecture", "hold", 1.8),
    ],
}


def load(name: str) -> Image.Image:
    """Fit a screenshot to the viewport width on a flat dark backing."""
    im = Image.open(SRC / f"{name}.png").convert("RGBA")
    flat = Image.new("RGB", im.size, (13, 17, 23))
    flat.paste(im, mask=im.split()[3])
    h = int(flat.height * VIEW_W / flat.width)
    return flat.resize((VIEW_W, h), Image.LANCZOS)


def frames_for(im: Image.Image, mode: str, seconds: float) -> list[Image.Image]:
    count = max(1, int(seconds * FPS))
    travel = max(0, im.height - VIEW_H)
    out = []
    for i in range(count):
        if mode == "pan" and travel:
            # Ease-in-out so the pan starts and stops gently.
            t = i / max(1, count - 1)
            eased = t * t * (3 - 2 * t)
            top = int(eased * travel)
        else:
            top = 0
        canvas = Image.new("RGB", (VIEW_W, VIEW_H), (13, 17, 23))
        canvas.paste(im.crop((0, top, VIEW_W, min(top + VIEW_H, im.height))), (0, 0))
        out.append(canvas)
    return out


def build(shots) -> list[Image.Image]:
    """Join shots with a dip to the backing colour.

    A straight cross-fade between two dense text interfaces double-exposes them
    into an unreadable frame, so each transition fades out and back in instead.
    """
    backing = Image.new("RGB", (VIEW_W, VIEW_H), (13, 17, 23))
    sequence: list[Image.Image] = []
    for index, (name, mode, seconds) in enumerate(shots):
        shot = frames_for(load(name), mode, seconds)
        if index and sequence:
            tail, head = sequence[-1], shot[0]
            half = max(1, FADE_FRAMES // 2)
            for f in range(1, half + 1):
                sequence.append(Image.blend(tail, backing, f / half))
            for f in range(1, half + 1):
                sequence.append(Image.blend(backing, head, f / half))
        sequence.extend(shot)
    return sequence


def encode(frames: list[Image.Image], target: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for i, frame in enumerate(frames):
            frame.save(tmpdir / f"f{i:04d}.png")
        palette = tmpdir / "palette.png"
        common = ["-v", "error", "-framerate", str(FPS), "-i", str(tmpdir / "f%04d.png")]
        subprocess.run(["ffmpeg", *common, "-vf", "palettegen=max_colors=96:stats_mode=diff",
                        "-y", str(palette)], check=True)
        subprocess.run(["ffmpeg", *common, "-i", str(palette), "-lavfi",
                        "paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle", "-loop", "0",
                        "-y", str(target)], check=True)


def main() -> int:
    if not shutil.which("ffmpeg"):
        print("ffmpeg is required and was not found on PATH", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    for name, shots in DEMOS.items():
        frames = build(shots)
        target = OUT / f"{name}.gif"
        encode(frames, target)
        print(f"{name+'.gif':<24} {len(frames):>4} frames  "
              f"{target.stat().st_size // 1024:>5} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
