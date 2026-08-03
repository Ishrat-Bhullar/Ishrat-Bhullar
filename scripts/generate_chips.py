#!/usr/bin/env python3
"""Render the technology stack as a custom SVG chip sheet.

Shields.io badges are a third-party request per chip and cannot be themed to
match the diagrams. These are drawn locally instead, from the technology table
in Section 5.6 / Appendix A of the Project Semester Report, so the stack section
uses the same palette and typography as everything else on the page.

Usage:  python3 scripts/generate_chips.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,"
        "Helvetica,Arial,sans-serif")

THEMES = {
    "dark":  {"accent": "#58A6FF", "chip": "#161B22", "border": "#30363D",
              "text": "#E6EDF3", "label": "#8B949E"},
    "light": {"accent": "#0969DA", "chip": "#F6F8FA", "border": "#D0D7DE",
              "text": "#1F2328", "label": "#57606A"},
}

# Grouped exactly as the report groups them.
GROUPS = [
    ("Languages",           ["Python", "JavaScript", "TypeScript", "SQL"]),
    ("Backend",             ["FastAPI", "REST APIs", "PostgreSQL"]),
    ("Frontend",            ["React", "Streamlit"]),
    ("Retrieval & Indexes", ["BM25", "FAISS", "ChromaDB", "Reciprocal Rank Fusion",
                             "Multilingual Embeddings"]),
    ("AI & Runtimes",       ["Retrieval-Augmented Generation", "Multi-Agent Systems",
                             "Ollama (local)", "Configurable cloud providers"]),
    ("Document Processing", ["OCR", "PDF Parsing", "Chunking"]),
    ("Tooling",             ["Git", "Docker"]),
]

WIDTH, PAD = 880, 4
CHIP_H, CHIP_GAP, ROW_GAP = 30, 8, 12
GROUP_GAP, LABEL_H = 20, 22
CHAR_W = 6.4          # ≈ advance width at 11.5px in the stack above
CHIP_PAD = 15


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chip_width(text: str) -> float:
    return len(text) * CHAR_W + CHIP_PAD * 2


def render(palette: dict) -> str:
    parts, y, idx = [], 8, 0

    for label, items in GROUPS:
        parts.append(
            f'<text x="{PAD}" y="{y + 12}" fill="{palette["label"]}" font-size="10" '
            f'font-weight="700" letter-spacing="1.1" opacity="1">{esc(label.upper())}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" '
            f'begin="{0.05*idx:.2f}s" fill="freeze"/></text>')
        idx += 1
        y += LABEL_H

        x = PAD
        for item in items:
            w = chip_width(item)
            if x + w > WIDTH - PAD:                 # wrap to a new chip row
                x = PAD
                y += CHIP_H + ROW_GAP
            parts.append(
                f'<g opacity="1">'
                f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" '
                f'begin="{0.04*idx:.2f}s" fill="freeze"/>'
                f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{CHIP_H}" '
                f'rx="{CHIP_H/2}" fill="{palette["chip"]}" stroke="{palette["border"]}"/>'
                f'<circle cx="{x + CHIP_PAD - 3}" cy="{y + CHIP_H/2}" r="2.6" '
                f'fill="{palette["accent"]}" opacity="0.9"/>'
                f'<text x="{x + CHIP_PAD + 7}" y="{y + CHIP_H/2 + 4}" '
                f'fill="{palette["text"]}" font-size="11.5">{esc(item)}</text>'
                f'</g>')
            x += w + CHIP_GAP
            idx += 1
        y += CHIP_H + GROUP_GAP

    height = y - GROUP_GAP + 8
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
            f'viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Technology stack">'
            f'<style>text{{font-family:{FONT};}}</style>'
            + "".join(parts) + "</svg>")


def main() -> int:
    out = ROOT / "assets" / "icons"
    out.mkdir(parents=True, exist_ok=True)
    for theme, palette in THEMES.items():
        (out / f"stack-{theme}.svg").write_text(render(palette))
    print(f"Wrote chip sheets for {len(THEMES)} themes "
          f"({sum(len(i) for _, i in GROUPS)} chips).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
