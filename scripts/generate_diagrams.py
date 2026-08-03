#!/usr/bin/env python3
"""Rebuild the architecture, workflow and timeline diagrams as themed SVGs.

Every diagram here is a clean re-drawing of a figure from the Project Semester
Report ("Enterprise AI Systems: Document Intelligence and Autonomous Multi-Agent
Software Delivery at Ernst & Young"), not a screenshot of it. Each is emitted
twice — once per palette — so the README can serve the right variant through
<picture> and read correctly in both GitHub themes.

Animation is deliberately restrained: a one-shot staggered fade for nodes and a
slow dash drift along connectors. Every animated attribute also carries its
final value statically, so a renderer that ignores SMIL shows a finished
diagram rather than a blank one.

Usage:  python3 scripts/generate_diagrams.py
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

THEMES = {
    "dark": {
        "accent": "#58A6FF",
        "accent_soft": "#1F6FEB",
        "ok": "#3FB950",
        "warn": "#D29922",
        "surface": "#161B22",
        "surface_alt": "#1C2430",
        "border": "#30363D",
        "text": "#E6EDF3",
        "muted": "#8B949E",
        "faint": "#6E7681",
    },
    "light": {
        "accent": "#0969DA",
        "accent_soft": "#218BFF",
        "ok": "#1A7F37",
        "warn": "#9A6700",
        "surface": "#F6F8FA",
        "surface_alt": "#EAEEF2",
        "border": "#D0D7DE",
        "text": "#1F2328",
        "muted": "#57606A",
        "faint": "#6E7681",
    },
}

FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,"
        "Helvetica,Arial,sans-serif")

# Rough advance width per character, as a fraction of font size.
W_REG, W_BOLD = 0.52, 0.56


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text: str, width_px: float, size: float, bold: bool = False) -> list[str]:
    """Greedy wrap using an estimated advance width (no font metrics available)."""
    per = size * (W_BOLD if bold else W_REG)
    limit = max(6, int(width_px / per))
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if len(trial) <= limit:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fade(index: int, dur: float = 0.5) -> str:
    """Staggered one-shot fade. Static opacity stays 1 for non-SMIL renderers."""
    return (f'<animate attributeName="opacity" from="0" to="1" dur="{dur}s" '
            f'begin="{0.07 * index:.2f}s" fill="freeze"/>')


def drift() -> str:
    """Slow dash drift that reads as flow without pulling the eye."""
    return ('<animate attributeName="stroke-dashoffset" from="10" to="0" '
            'dur="2.4s" repeatCount="indefinite"/>')


def node(x, y, w, h, title, sub, p, idx, accent=False, tone=None):
    """A rounded card with a bold title and optional wrapped sub-label."""
    fill = p["surface_alt"] if accent else p["surface"]
    stroke = tone or (p["accent"] if accent else p["border"])
    parts = [f'<g opacity="1">{fade(idx)}',
             f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
             f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>']

    sub_lines = wrap(sub, w - 24, 10.5) if sub else []
    block = 15 + (len(sub_lines) * 13)
    ty = y + (h - block) / 2 + 12

    parts.append(f'<text x="{x + w/2}" y="{ty}" fill="{p["text"]}" font-size="12.5" '
                 f'font-weight="600" text-anchor="middle">{esc(title)}</text>')
    for i, line in enumerate(sub_lines):
        parts.append(f'<text x="{x + w/2}" y="{ty + 15 + i*13}" fill="{p["muted"]}" '
                     f'font-size="10.5" text-anchor="middle">{esc(line)}</text>')
    parts.append("</g>")
    return "".join(parts)


def arrow(x1, y1, x2, y2, p, idx, flow=True):
    """Connector with an arrowhead; horizontal or vertical only."""
    head = 5
    if abs(y2 - y1) > abs(x2 - x1):          # vertical
        ey = y2 - head
        tip = f'{x2},{y2} {x2-head},{ey} {x2+head},{ey}'
    else:                                     # horizontal
        ex = x2 - head
        tip = f'{x2},{y2} {ex},{y2-head} {ex},{y2+head}'
        ey = y2
    dash = f' stroke-dasharray="5 5"' if flow else ""
    anim = drift() if flow else ""
    end_x = x2 - head if abs(x2 - x1) >= abs(y2 - y1) else x2
    end_y = y2 - head if abs(y2 - y1) > abs(x2 - x1) else y2
    return (f'<g opacity="1">{fade(idx)}'
            f'<line x1="{x1}" y1="{y1}" x2="{end_x}" y2="{end_y}" '
            f'stroke="{p["faint"]}" stroke-width="1.4"{dash} opacity="0.75">{anim}</line>'
            f'<polygon points="{tip}" fill="{p["faint"]}" opacity="0.85"/></g>')


def document(width, height, label, body, p, title=None, note=None):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(label)}">',
           f'<style>text{{font-family:{FONT};}}</style>']
    if title:
        out.append(f'<text x="{width/2}" y="24" fill="{p["accent"]}" font-size="14.5" '
                   f'font-weight="700" text-anchor="middle" opacity="1">'
                   f'{esc(title)}{fade(0)}</text>')
    out.append(body)
    if note:
        out.append(f'<text x="{width/2}" y="{height-10}" fill="{p["faint"]}" '
                   f'font-size="10.5" font-style="italic" text-anchor="middle" '
                   f'opacity="1">{esc(note)}{fade(12)}</text>')
    out.append("</svg>")
    return "\n".join(out)


# ─────────────────────────────────────────────────────────────── layouts ──

def layered(title, layers, note, p, width=880):
    """Vertical layer stack — used for both RAG system architectures."""
    x, bw, bh, gap, top = 92, width - 92 - 40, 60, 26, 46
    body, idx = [], 1
    for i, (name, sub) in enumerate(layers):
        y = top + i * (bh + gap)
        body.append(f'<g opacity="1">{fade(idx)}'
                    f'<circle cx="{x-32}" cy="{y+bh/2}" r="14" fill="{p["surface_alt"]}" '
                    f'stroke="{p["accent"]}" stroke-width="1.2"/>'
                    f'<text x="{x-32}" y="{y+bh/2+4}" fill="{p["accent"]}" font-size="11.5" '
                    f'font-weight="700" text-anchor="middle">{i+1}</text></g>')
        body.append(node(x, y, bw, bh, name, sub, p, idx, accent=(i == 0)))
        idx += 1
        if i < len(layers) - 1:
            body.append(arrow(x + bw/2, y + bh, x + bw/2, y + bh + gap, p, idx))
    height = top + len(layers) * (bh + gap) - gap + 34
    return document(width, height, title, "".join(body), p, title, note)


def pipeline(title, steps, note, p, width=880, per_row=4):
    """Horizontal step flow that wraps into rows; `kind` tints a step."""
    pad, gap_x, gap_y, bh = 20, 30, 34, 56
    bw = (width - 2*pad - (per_row-1)*gap_x) / per_row
    rows = [steps[i:i+per_row] for i in range(0, len(steps), per_row)]
    body, idx, top = [], 1, 46

    for r, row in enumerate(rows):
        y = top + r * (bh + gap_y)
        for c, (label, sub, kind) in enumerate(row):
            x = pad + c * (bw + gap_x)
            tone = {"gate": p["warn"], "done": p["ok"]}.get(kind)
            body.append(node(x, y, bw, bh, label, sub or "", p, idx,
                             accent=kind in ("gate", "start"), tone=tone))
            idx += 1
            if c < len(row) - 1:
                body.append(arrow(x + bw, y + bh/2, x + bw + gap_x, y + bh/2, p, idx))
        # Wrap connector: drop from the end of this row to the start of the next.
        if r < len(rows) - 1:
            y2 = y + bh + gap_y
            ex = pad + (len(row)-1) * (bw + gap_x) + bw/2
            body.append(f'<g opacity="1">{fade(idx)}<path d="M {ex} {y+bh} '
                        f'V {y+bh+gap_y/2} H {pad+bw/2} V {y2}" fill="none" '
                        f'stroke="{p["faint"]}" stroke-width="1.4" stroke-dasharray="5 5" '
                        f'opacity="0.7">{drift()}</path>'
                        f'<polygon points="{pad+bw/2},{y2} {pad+bw/2-5},{y2-5} '
                        f'{pad+bw/2+5},{y2-5}" fill="{p["faint"]}" opacity="0.85"/></g>')
    height = top + len(rows) * (bh + gap_y) - gap_y + 34
    return document(width, height, title, "".join(body), p, title, note)


def journey(p, width=880):
    """The four-stage internship progression, as a timeline."""
    stages = [
        ("Validator", "Maharashtra AI Portal",
         "Enterprise testing and workflow validation"),
        ("Builder", "Vectorless RAG Chatbot",
         "Lightweight lexical retrieval foundation"),
        ("Architect", "Hybrid RAG Chatbot",
         "Semantic and lexical retrieval, fused"),
        ("Platform Engineer", "Autonomous SDLC Platform",
         "Multi-agent orchestration under governance"),
    ]
    pad, gap, top = 20, 22, 58
    bw = (width - 2*pad - 3*gap) / 4
    body = [f'<line x1="{pad+bw/2}" y1="{top-18}" x2="{width-pad-bw/2}" y2="{top-18}" '
            f'stroke="{p["border"]}" stroke-width="2"/>',
            f'<line x1="{pad+bw/2}" y1="{top-18}" x2="{width-pad-bw/2}" y2="{top-18}" '
            f'stroke="{p["accent"]}" stroke-width="2" stroke-dasharray="700" '
            f'stroke-dashoffset="0" opacity="0.9">'
            f'<animate attributeName="stroke-dashoffset" from="700" to="0" dur="1.6s" '
            f'fill="freeze"/></line>']

    for i, (role, project, sub) in enumerate(stages):
        x = pad + i * (bw + gap)
        cx = x + bw/2
        body.append(f'<g opacity="1">{fade(i+1)}'
                    f'<circle cx="{cx}" cy="{top-18}" r="9" fill="{p["surface"]}" '
                    f'stroke="{p["accent"]}" stroke-width="2"/>'
                    f'<text x="{cx}" y="{top-14}" fill="{p["accent"]}" font-size="10" '
                    f'font-weight="700" text-anchor="middle">{i+1}</text></g>')
        lines = wrap(sub, bw - 20, 10)
        h = 78 + (len(lines)-1) * 12
        body.append(f'<g opacity="1">{fade(i+2)}'
                    f'<rect x="{x}" y="{top}" width="{bw}" height="{h}" rx="8" '
                    f'fill="{p["surface"]}" stroke="{p["border"]}"/>'
                    f'<text x="{cx}" y="{top+21}" fill="{p["accent"]}" font-size="11" '
                    f'font-weight="700" text-anchor="middle" letter-spacing="0.6">'
                    f'{esc(role.upper())}</text>'
                    f'<text x="{cx}" y="{top+40}" fill="{p["text"]}" font-size="11.5" '
                    f'font-weight="600" text-anchor="middle">{esc(project)}</text>'
                    + "".join(
                        f'<text x="{cx}" y="{top+57+j*12}" fill="{p["muted"]}" '
                        f'font-size="10" text-anchor="middle">{esc(l)}</text>'
                        for j, l in enumerate(lines))
                    + "</g>")
    height = top + 78 + 24 + 26
    return document(width, height, "Internship progression", "".join(body), p,
                    "Engineering Journey — Validator → Builder → Architect → Platform Engineer",
                    "Increasing technical ownership and system complexity across the internship")


def sdlc_architecture(p, width=880):
    """Layered platform architecture with the specialised agent pool."""
    pad, top = 20, 46
    w = width - 2*pad
    body, idx = [], 1

    body.append(node(pad, top, w, 46, "Client Application",
                     "Project workspaces, dashboard, documentation, approval, replay, settings",
                     p, idx, accent=True)); idx += 1
    body.append(arrow(width/2, top+46, width/2, top+70, p, idx))

    body.append(node(pad, top+70, w, 46, "Orchestration Service",
                     "Pipeline sequencing, human approval checkpoints, centralized project memory",
                     p, idx)); idx += 1
    body.append(arrow(width/2, top+116, width/2, top+140, p, idx))

    # Agent pool
    pool_y, pool_h = top+140, 104
    body.append(f'<g opacity="1">{fade(idx)}'
                f'<rect x="{pad}" y="{pool_y}" width="{w}" height="{pool_h}" rx="8" '
                f'fill="{p["surface_alt"]}" stroke="{p["accent"]}" stroke-width="1"/>'
                f'<text x="{width/2}" y="{pool_y+20}" fill="{p["text"]}" font-size="12.5" '
                f'font-weight="600" text-anchor="middle">Specialized AI Agent Pool</text></g>')
    idx += 1
    agents = ["Memory", "Requirement", "Business Analyst", "Architect",
              "Database", "UI/UX", "Security", "Compliance"]
    cw = (w - 24 - 7*8) / 8
    for i, name in enumerate(agents):
        ax = pad + 12 + i * (cw + 8)
        body.append(f'<g opacity="1">{fade(idx+i)}'
                    f'<rect x="{ax}" y="{pool_y+30}" width="{cw}" height="30" rx="6" '
                    f'fill="{p["surface"]}" stroke="{p["border"]}"/>'
                    + "".join(
                        f'<text x="{ax+cw/2}" y="{pool_y+44+j*10}" fill="{p["text"]}" '
                        f'font-size="8.6" text-anchor="middle">{esc(l)}</text>'
                        for j, l in enumerate(wrap(name, cw-4, 8.6)))
                    + "</g>")
    idx += len(agents)
    body.append(f'<text x="{width/2}" y="{pool_y+80}" fill="{p["muted"]}" font-size="10" '
                f'text-anchor="middle" opacity="1">Presentation / Narration / Video '
                f'Generation Agents{fade(idx)}</text>')
    idx += 1

    # Two supporting blocks
    sy = pool_y + pool_h + 24
    hw = (w - 20) / 2
    body.append(arrow(pad + hw/2, pool_y+pool_h, pad + hw/2, sy, p, idx))
    body.append(arrow(pad + hw + 20 + hw/2, pool_y+pool_h, pad + hw + 20 + hw/2, sy, p, idx))
    body.append(node(pad, sy, hw, 46, "Configurable AI Reasoning Layer",
                     "BYOK provider routing without code changes", p, idx)); idx += 1
    body.append(node(pad + hw + 20, sy, hw, 46, "Persistent Data Store",
                     "Projects, artifacts, execution runs, approvals", p, idx))
    height = sy + 46 + 34
    return document(width, height, "SDLC platform architecture", "".join(body), p,
                    "Autonomous Multi-Agent SDLC Platform — System Architecture",
                    "Every agent shares centralized project memory and pauses at defined human checkpoints")


def retrieval_comparison(p, width=880):
    """Keyword vs semantic vs hybrid, as drawn in Figure 3.1."""
    pad, gap, top = 20, 26, 50
    bw = (width - 2*pad - 2*gap) / 3
    cards = [
        ("A", "Keyword (Lexical) Retrieval",
         ["Matches exact terms and phrasing",
          "Strong for policy numbers and codes",
          "Lightweight infrastructure",
          "Limited semantic understanding"], False),
        ("B", "Semantic (Vector) Retrieval",
         ["Matches meaning, not exact words",
          "Handles paraphrased queries",
          "Higher infrastructure overhead",
          "Can miss exact-term precision"], False),
        ("C", "Hybrid Retrieval",
         ["Combines both rankings into one set",
          "Balances precision and recall",
          "Preferred for multilingual,",
          "compliance-sensitive documents"], True),
    ]
    body = []
    h = 148
    for i, (tag, name, bullets, hero) in enumerate(cards):
        x = pad + i * (bw + gap)
        body.append(f'<g opacity="1">{fade(i+1)}'
                    f'<rect x="{x}" y="{top}" width="{bw}" height="{h}" rx="10" '
                    f'fill="{p["surface_alt"] if hero else p["surface"]}" '
                    f'stroke="{p["accent"] if hero else p["border"]}" stroke-width="1"/>'
                    f'<circle cx="{x+bw/2}" cy="{top+22}" r="11" fill="{p["surface"]}" '
                    f'stroke="{p["accent"]}" stroke-width="1.2"/>'
                    f'<text x="{x+bw/2}" y="{top+26}" fill="{p["accent"]}" font-size="10.5" '
                    f'font-weight="700" text-anchor="middle">{tag}</text>'
                    f'<text x="{x+bw/2}" y="{top+52}" fill="{p["text"]}" font-size="11.5" '
                    f'font-weight="600" text-anchor="middle">{esc(name)}</text>'
                    + "".join(
                        f'<text x="{x+bw/2}" y="{top+74+j*17}" fill="{p["muted"]}" '
                        f'font-size="10" text-anchor="middle">{esc(b)}</text>'
                        for j, b in enumerate(bullets))
                    + "</g>")
        if i < 2:
            body.append(arrow(x + bw, top + h/2, x + bw + gap, top + h/2, p, i+2))
    return document(width, top + h + 34, "Retrieval approach comparison", "".join(body), p,
                    "Conceptual Comparison of Document Retrieval Approaches",
                    "Government document repositories favour hybrid retrieval for auditability and multilingual accuracy")


def data_model(p, width=880):
    """Simplified conceptual data model from Figure 5.4.8."""
    pad, top = 20, 50
    bw, bh = 172, 52
    positions = {
        "Project":              (pad, top),
        "Generated Artifact":   (pad + 262, top),
        "Agent Execution Run":  (pad + 524, top),
        "Approval":             (pad + 262, top + 96),
        "Provider Configuration": (pad + 524, top + 96),
    }
    subs = {
        "Project": "name, type, status",
        "Generated Artifact": "type, content, timestamp",
        "Agent Execution Run": "agent name, status, timing",
        "Approval": "status, reviewer, notes",
        "Provider Configuration": "provider, scope, status",
    }
    body = []
    for i, (name, (x, y)) in enumerate(positions.items()):
        body.append(node(x, y, bw, bh, name, subs[name], p, i+1, accent=(name == "Project")))

    def link(x1, y1, x2, y2, label, idx):
        mx, my = (x1+x2)/2, (y1+y2)/2
        return (f'<g opacity="1">{fade(idx)}'
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{p["faint"]}" '
                f'stroke-width="1.3" stroke-dasharray="5 5" opacity="0.75">{drift()}</line>'
                f'<text x="{mx}" y="{my-5}" fill="{p["faint"]}" font-size="9.5" '
                f'text-anchor="middle">{esc(label)}</text></g>')

    body.append(link(pad+bw, top+bh/2, pad+262, top+bh/2, "produces", 6))
    body.append(link(pad+262+bw, top+bh/2, pad+524, top+bh/2, "recorded by", 7))
    body.append(link(pad+262+bw/2, top+bh, pad+262+bw/2, top+96, "reviewed via", 8))
    body.append(link(pad+262+bw, top+96+bh/2, pad+524, top+96+bh/2, "uses", 9))
    body.append(link(pad+bw/2, top+bh, pad+262+bw/2, top+96+bh/2, "owns", 10))
    return document(width, top + 96 + bh + 34, "Conceptual data model", "".join(body), p,
                    "Autonomous SDLC Platform — Simplified Conceptual Data Model",
                    "Structuring the schema around traceability is what makes the Documentation and Temporal Replay Centers possible")



def hero(p, width=880):
    """Title banner. No typing effect — a single settled composition instead."""
    h = 172
    body = [
        f'<defs><linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{p["accent"]}" stop-opacity="0"/>'
        f'<stop offset="30%" stop-color="{p["accent"]}" stop-opacity="0.9"/>'
        f'<stop offset="70%" stop-color="{p["accent"]}" stop-opacity="0.9"/>'
        f'<stop offset="100%" stop-color="{p["accent"]}" stop-opacity="0"/>'
        f'<animate attributeName="x1" values="-0.5;0;-0.5" dur="8s" repeatCount="indefinite"/>'
        f'<animate attributeName="x2" values="1;1.5;1" dur="8s" repeatCount="indefinite"/>'
        f'</linearGradient></defs>',
        f'<text x="{width/2}" y="62" fill="{p["text"]}" font-size="38" font-weight="700" '
        f'letter-spacing="7" text-anchor="middle" opacity="1">ISHRAT BHULLAR{fade(1,0.7)}</text>',
        f'<rect x="{width/2-190}" y="80" width="380" height="1.5" fill="url(#rule)" opacity="1">'
        f'{fade(2)}</rect>',
        f'<text x="{width/2}" y="108" fill="{p["accent"]}" font-size="13.5" font-weight="600" '
        f'letter-spacing="2.4" text-anchor="middle" opacity="1">'
        f'AI ENGINEER \u00b7 RETRIEVAL-AUGMENTED GENERATION \u00b7 BACKEND SYSTEMS{fade(3)}</text>',
        f'<text x="{width/2}" y="134" fill="{p["muted"]}" font-size="11.5" '
        f'text-anchor="middle" opacity="1">Computer Engineering, Thapar Institute of '
        f'Engineering &amp; Technology{fade(4)}</text>',
        f'<text x="{width/2}" y="152" fill="{p["faint"]}" font-size="11.5" '
        f'text-anchor="middle" opacity="1">AI Engineering Intern, Ernst &amp; Young '
        f'\u00b7 Jan\u2013Jul 2026{fade(5)}</text>',
    ]
    return document(width, h, "Ishrat Bhullar", "".join(body), p)


# ───────────────────────────────────────────────────────────── registry ──

def build(p):
    return {
        "svg/hero": hero(p),
        "svg/journey": journey(p),
        "architecture/vectorless-rag": layered(
            "Vectorless RAG Chatbot — System Architecture",
            [("Document Processing Layer",
              "PDF ingestion, text extraction, preprocessing, metadata organization"),
             ("Retrieval Layer",
              "Lightweight keyword (lexical) retrieval with metadata filtering"),
             ("AI Processing Layer",
              "Contextual prompt construction from retrieved segments, local language model inference"),
             ("Presentation Layer",
              "Conversational interface with document-grounded responses and source references")],
            "Deliberately excludes a vector database — retrieval is entirely keyword-driven", p),
        "architecture/hybrid-rag": layered(
            "Hybrid RAG Chatbot — System Architecture",
            [("Document Processing Layer",
              "Ingestion, OCR, preprocessing, metadata extraction, intelligent chunking"),
             ("Embedding Layer",
              "Multilingual semantic embeddings capturing meaning across document sections"),
             ("Retrieval Layer (Dual Path)",
              "Semantic vector search and keyword search, combined via rank fusion into one ranked result set"),
             ("AI Generation Layer",
              "Contextual prompt construction from fused results, local language model inference"),
             ("Presentation Layer",
              "Conversational interface with citations and retrieval transparency")],
            "Adds a semantic embedding path and rank fusion on top of the vectorless keyword baseline", p),
        "architecture/sdlc-platform": sdlc_architecture(p),
        "architecture/retrieval-comparison": retrieval_comparison(p),
        "architecture/data-model": data_model(p),
        "workflows/vectorless-pipeline": pipeline(
            "Vectorless RAG Chatbot — Technical Workflow",
            [("Document Upload", "", "start"), ("Text Extraction & Cleaning", "", ""),
             ("BM25 Index Construction", "", ""), ("User Query", "", ""),
             ("Keyword Retrieval", "", ""), ("Prompt Construction", "", ""),
             ("Language Model Response", "", ""), ("User Interface", "", "done")],
            "Retrieval, prompt construction and response generation all operate without a vector index", p),
        "workflows/hybrid-pipeline": pipeline(
            "Hybrid RAG Chatbot — Technical Workflow",
            [("OCR & Text Cleaning", "", "start"), ("Document Chunking", "", ""),
             ("Embeddings + Keyword Index", "parallel", ""), ("Semantic + Keyword Search", "parallel", ""),
             ("Rank Fusion & Context", "", ""), ("Prompt Engineering", "", ""),
             ("Language Model", "", ""), ("Citation Generation", "and interface display", "done")],
            "Semantic and keyword retrieval run in parallel and are fused before response generation", p),
        "workflows/sdlc-pipeline": pipeline(
            "Autonomous SDLC Platform — Implemented Pipeline Workflow",
            [("Create Project", "", "start"), ("Memory Agent", "", ""),
             ("Requirement Agent", "", ""), ("Business Analyst", "", ""),
             ("Human Approval", "checkpoint", "gate"), ("Architect Agent", "", ""),
             ("Database Agent", "", ""), ("UI/UX + Security", "parallel", ""),
             ("Compliance Agent", "", ""), ("Human Approval", "checkpoint", "gate"),
             ("Documentation Center", "", ""), ("Presentation & Video", "", "done")],
            "Every stage shares centralized project memory; two mandatory human approval checkpoints govern the pipeline",
            p, per_row=4),
        "workflows/portal-workflow": pipeline(
            "Maharashtra AI Portal — Evaluation and Clearance Workflow",
            [("Submission", "", "start"), ("Upload & Ingestion", "", ""),
             ("Post-Ingestion", "", ""), ("Classify Documents", "by type", ""),
             ("OCR & Pre-processing", "", ""), ("Data Preparation", "", ""),
             ("Index with Criteria", "", ""), ("AI Agent Evaluation", "", ""),
             ("Aggregate Outputs", "", ""), ("Generate Outputs", "", ""),
             ("Summary Report", "", ""), ("Decision", "officer authority", "gate")],
            "Automation is confined to processing and preliminary assessment — the clearance decision stays with the officer",
            p, per_row=4),
        "workflows/byok-resolution": pipeline(
            "BYOK AI Provider Resolution Order",
            [("Project-Level BYOK Key", "", "start"), ("Platform Default", "Azure OpenAI", ""),
             ("Fallback Provider", "OpenAI / Groq", ""), ("Local Fallback", "locally hosted model", "done")],
            "Each tier is tried only if the one before it is unavailable — the platform degrades gracefully rather than failing",
            p, per_row=4),
        "workflows/media-pipeline": pipeline(
            "Media Generation Pipeline — Presentation to Video",
            [("Story Planning", "", "start"), ("Slide Rendering Engine", "", ""),
             ("Narration Script", "AI narration module", ""), ("Text-to-Speech Engine", "", ""),
             ("Presenter Avatar", "optional", ""), ("Video Composition", "", "done")],
            "Each stage is a swappable component, so any one part can be revised without regenerating the rest",
            p, per_row=3),
    }


def main() -> int:
    written = 0
    for theme, palette in THEMES.items():
        for rel, svg in build(palette).items():
            path = ROOT / "assets" / f"{rel}-{theme}.svg"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(svg)
            written += 1
    print(f"Wrote {written} SVG files across {len(THEMES)} themes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
