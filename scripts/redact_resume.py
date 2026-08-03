#!/usr/bin/env python3
"""Remove the phone number from the published résumé PDF.

This deletes the glyphs from the page content stream, so the digits are gone
from the text layer entirely. Drawing a white box over them would leave the
number fully extractable with any PDF reader — the classic redaction failure,
and worse than useless for a privacy fix.

The résumé sets each contact field as its own absolutely-positioned text block,
so simply dropping the phone block would leave a gap in the middle of the line.
The separator preceding it is removed too, and every field to its right is
shifted left by the exact width freed, closing the line up cleanly.

Usage:  python3 scripts/redact_resume.py [--check]
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pikepdf

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "assets" / "resume" / "Ishrat-Bhullar-Resume.pdf"

PHONE = re.compile(r"\+?\s*(?:91)?[\s\-]*\d{5}[\s\-]*\d{5}")
DIGITS = ("9878775757", "919878775757")


def tounicode_map(page) -> dict[int, str]:
    """Glyph id -> character, parsed from each font's ToUnicode CMap."""
    mapping: dict[int, str] = {}
    resources = page.Resources
    if "/Font" not in resources:
        return mapping
    for _, font in resources.Font.items():
        if "/ToUnicode" not in font:
            continue
        cmap = bytes(font.ToUnicode.read_bytes()).decode("latin-1", "replace")
        for block in re.findall(r"beginbfchar(.*?)endbfchar", cmap, re.S):
            for src, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block):
                mapping[int(src, 16)] = bytes.fromhex(dst).decode("utf-16-be", "replace")
        for block in re.findall(r"beginbfrange(.*?)endbfrange", cmap, re.S):
            for lo, hi, dst in re.findall(
                    r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block):
                start = int(dst, 16)
                for offset, gid in enumerate(range(int(lo, 16), int(hi, 16) + 1)):
                    mapping[gid] = chr(start + offset)
    return mapping


def glyph_bytes(operands, operator: str) -> bytes:
    if operator == "Tj":
        return bytes(operands[0])
    return b"".join(bytes(e) for e in operands[0] if isinstance(e, pikepdf.String))


def decode(raw: bytes, table: dict[int, str]) -> str:
    return "".join(
        table.get(int.from_bytes(raw[i:i + 2], "big"), "")
        for i in range(0, len(raw), 2)
    )


def redact(pdf_path: Path) -> int:
    pdf = pikepdf.open(pdf_path, allow_overwriting_input=True)
    removed = 0

    for page in pdf.pages:
        table = tounicode_map(page)
        ops = list(pikepdf.parse_content_stream(page))

        # Group into BT..ET blocks, recording each block's Tm position and text.
        blocks, current = [], None
        for i, (operands, operator) in enumerate(ops):
            name = str(operator)
            if name == "BT":
                current = {"start": i, "x": None, "y": None, "text": "", "tm": None}
            elif name == "Tm" and current is not None:
                current["tm"] = i
                current["x"] = float(operands[4])
                current["y"] = float(operands[5])
            elif name in ("Tj", "TJ") and current is not None:
                current["text"] += decode(glyph_bytes(operands, name), table)
            elif name == "ET" and current is not None:
                current["end"] = i
                blocks.append(current)
                current = None

        phone = next((b for b in blocks if PHONE.fullmatch(b["text"].strip())), None)
        if phone is None:
            continue

        line = sorted([b for b in blocks if b["y"] == phone["y"]], key=lambda b: b["x"])
        index = line.index(phone)
        separator = line[index - 1] if index > 0 and line[index - 1]["text"].strip() == "|" else None
        following = line[index + 1] if index + 1 < len(line) else None
        if separator is None or following is None:
            print("unexpected contact-line layout; aborting", file=sys.stderr)
            pdf.close()
            return 0

        # Width freed by dropping "| <phone>". The contact line is centred under
        # a centred header, so closing the gap is not enough: fields to the right
        # move left and fields to the left move right, each by half the freed
        # width, which keeps the shortened line centred on the same axis.
        delta = following["x"] - separator["x"]
        half = delta / 2
        drop = {j for b in (separator, phone) for j in range(b["start"], b["end"] + 1)}

        for block in line:
            if block["tm"] is None or block in (separator, phone):
                continue
            if block["x"] >= following["x"]:
                new_x = block["x"] - half
            elif block["x"] < separator["x"]:
                new_x = block["x"] + half
            else:
                continue
            operands, operator = ops[block["tm"]]
            shifted = list(operands)
            shifted[4] = pikepdf.Object.parse(f"{new_x:.6f}".encode())
            ops[block["tm"]] = (shifted, operator)

        ops = [op for j, op in enumerate(ops) if j not in drop]
        page.Contents = pdf.make_stream(pikepdf.unparse_content_stream(ops))
        removed += 1

    if removed:
        pdf.save(pdf_path)
    pdf.close()
    return removed


def verify() -> bool:
    text = subprocess.run(["pdftotext", str(PDF), "-"],
                          capture_output=True, text=True).stdout
    digits = re.sub(r"\D", "", text)
    for needle in DIGITS:
        if needle in digits:
            print(f"FAIL: {needle} still present in the text layer", file=sys.stderr)
            return False
    print("Verified: no phone number in the extracted text layer.")
    print("Contact line now reads:")
    for row in text.splitlines()[:4]:
        if "@" in row:
            print("   ", row.strip())
    return True


def main() -> int:
    if not PDF.exists():
        print(f"missing {PDF}", file=sys.stderr)
        return 1
    if "--check" not in sys.argv:
        print(f"Redacted {redact(PDF)} page(s).")
    return 0 if verify() else 1


if __name__ == "__main__":
    raise SystemExit(main())
