#!/usr/bin/env python3
"""Render GitHub statistics cards as self-hosted SVGs.

The public github-readme-stats instance is a shared Vercel deployment that is
frequently rate-limited or paused, which shows up as broken images on the
profile. This queries the GraphQL API directly and writes the cards into
assets/, so they are served from this repository and always render.

Usage:  GITHUB_TOKEN=<token> python3 scripts/generate_stats.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

LOGIN = os.environ.get("GITHUB_LOGIN", "Ishrat-Bhullar")
ASSETS = Path(__file__).resolve().parent.parent / "assets"
API = "https://api.github.com/graphql"

# Two palettes so <picture> can serve the right card for GitHub's theme.
THEMES = {
    "dark": {
        "accent": "#58A6FF",
        "label": "#8B949E",
        "value": "#C9D1D9",
        "muted": "#6E7681",
        "track": "#21262D",
    },
    "light": {
        "accent": "#0969DA",
        "label": "#57606A",
        "value": "#1F2328",
        "muted": "#6E7681",
        "track": "#D0D7DE",
    },
}

FONT = (
    "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,"
    "'Liberation Mono',monospace"
)

PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100,
                 orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 12, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""

YEAR_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
    }
  }
}
"""


def graphql(query: str, variables: dict, token: str) -> dict:
    payload = json.dumps({"query": query, "variables": variables}).encode()
    request = urllib.request.Request(
        API,
        data=payload,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{LOGIN}-profile-stats",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = json.loads(response.read())
    if "errors" in body:
        raise RuntimeError(json.dumps(body["errors"], indent=2))
    return body["data"]


def collect(token: str) -> tuple[dict, list[tuple[str, str, float]]]:
    """Return headline totals and the language breakdown as (name, colour, share)."""
    user = graphql(PROFILE_QUERY, {"login": LOGIN}, token)["user"]

    # contributionsCollection caps at one year per call, so walk year by year.
    created = datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    commits = pull_requests = issues = reviews = 0
    for year in range(created.year, now.year + 1):
        window_from = max(created, datetime(year, 1, 1, tzinfo=timezone.utc))
        window_to = min(now, datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
        if window_from >= window_to:
            continue
        contributions = graphql(
            YEAR_QUERY,
            {
                "login": LOGIN,
                "from": window_from.isoformat(),
                "to": window_to.isoformat(),
            },
            token,
        )["user"]["contributionsCollection"]
        commits += contributions["totalCommitContributions"]
        pull_requests += contributions["totalPullRequestContributions"]
        issues += contributions["totalIssueContributions"]
        reviews += contributions["totalPullRequestReviewContributions"]

    repositories = user["repositories"]
    candidates = {
        "Total Commits": commits,
        "Public Repos": repositories["totalCount"],
        "Pull Requests": pull_requests,
        "Issues": issues,
        "Code Reviews": reviews,
        "Stars Earned": sum(node["stargazerCount"] for node in repositories["nodes"]),
        "Followers": user["followers"]["totalCount"],
    }
    # A row reading "0" is worse than no row at all; each reappears on its own
    # once the underlying count is non-zero. ALWAYS_SHOWN anchors the card so it
    # can never render empty.
    always_shown = ("Total Commits", "Public Repos")
    totals = {
        label: value
        for label, value in candidates.items()
        if value or label in always_shown
    }

    sizes: dict[str, int] = {}
    colours: dict[str, str] = {}
    for node in repositories["nodes"]:
        for edge in node["languages"]["edges"]:
            name = edge["node"]["name"]
            sizes[name] = sizes.get(name, 0) + edge["size"]
            colours[name] = edge["node"]["color"] or "#8B949E"

    total_bytes = sum(sizes.values()) or 1
    ranked = sorted(sizes.items(), key=lambda item: item[1], reverse=True)
    shares = [
        (name, colours[name], size / total_bytes * 100) for name, size in ranked
    ]
    # Trailing sub-percent entries are visual noise on an otherwise clean card,
    # but never trim below four so the breakdown still reads as a breakdown.
    languages = [item for item in shares[:6] if item[2] >= 0.5] or shares[:4]
    if len(languages) < 4:
        languages = shares[:4]
    return totals, languages


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def fade_in(index: int) -> str:
    """Staggered fade — deliberately slow and small, so it reads as polish.

    Every animated element also carries its *final* value as a static
    attribute. A renderer that ignores SMIL then shows the finished card
    rather than a blank one.
    """
    return (
        f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" '
        f'begin="{0.08 * index:.2f}s" fill="freeze"/>'
    )


def render_stats(totals: dict, palette: dict) -> str:
    width, row_height, top = 450, 26, 62
    height = top + row_height * len(totals) + 12
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="GitHub statistics for {LOGIN}">',
        f'<style>text{{font-family:{FONT};}}</style>',
        f'<text x="0" y="22" fill="{palette["accent"]}" font-size="15" '
        f'font-weight="600" opacity="1">GitHub Statistics{fade_in(0)}</text>',
        f'<rect x="0" y="34" width="{width}" height="1" '
        f'fill="{palette["track"]}" opacity="1">{fade_in(1)}</rect>',
    ]
    for index, (label, value) in enumerate(totals.items()):
        y = top + row_height * index
        parts.append(
            f'<g opacity="1">{fade_in(index + 2)}'
            f'<text x="0" y="{y}" fill="{palette["label"]}" font-size="13">'
            f"{escape(label)}</text>"
            f'<text x="{width}" y="{y}" fill="{palette["value"]}" font-size="13" '
            f'font-weight="600" text-anchor="end">{value:,}</text>'
            f"</g>"
        )
    parts.append("</svg>")
    return "\n".join(parts)


def render_languages(languages: list[tuple[str, str, float]], palette: dict) -> str:
    width, bar_y, bar_height = 450, 48, 8
    columns, row_height = 2, 24
    rows = (len(languages) + columns - 1) // columns
    height = bar_y + bar_height + 22 + rows * row_height
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="Most used languages for {LOGIN}">',
        f'<style>text{{font-family:{FONT};}}</style>',
        f'<text x="0" y="22" fill="{palette["accent"]}" font-size="15" '
        f'font-weight="600" opacity="1">Most Used Languages{fade_in(0)}</text>',
        f'<rect x="0" y="34" width="{width}" height="1" '
        f'fill="{palette["track"]}" opacity="1">{fade_in(1)}</rect>',
        f'<clipPath id="bar"><rect x="0" y="{bar_y}" width="{width}" '
        f'height="{bar_height}" rx="{bar_height / 2}"/></clipPath>',
        f'<rect x="0" y="{bar_y}" width="{width}" height="{bar_height}" '
        f'rx="{bar_height / 2}" fill="{palette["track"]}"/>',
        f'<g clip-path="url(#bar)">',
    ]

    # Segments grow from zero on load — one pass, no looping motion.
    offset = 0.0
    for index, (_, colour, share) in enumerate(languages):
        segment = width * share / 100
        parts.append(
            f'<rect x="{offset:.2f}" y="{bar_y}" width="{segment:.2f}" '
            f'height="{bar_height}" fill="{colour}">'
            f'<animate attributeName="width" from="0" to="{segment:.2f}" '
            f'dur="0.9s" begin="{0.08 * index:.2f}s" fill="freeze"/></rect>'
        )
        offset += segment
    parts.append("</g>")

    legend_top = bar_y + bar_height + 30
    column_width = width / columns
    for index, (name, colour, share) in enumerate(languages):
        x = (index % columns) * column_width
        y = legend_top + (index // columns) * row_height
        parts.append(
            f'<g opacity="1">{fade_in(index + 2)}'
            f'<circle cx="{x + 5:.0f}" cy="{y - 4}" r="5" fill="{colour}"/>'
            f'<text x="{x + 18:.0f}" y="{y}" fill="{palette["label"]}" '
            f'font-size="13">{escape(name)}</text>'
            f'<text x="{x + column_width - 24:.0f}" y="{y}" '
            f'fill="{palette["value"]}" font-size="13" text-anchor="end">'
            f"{share:.1f}%</text></g>"
        )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 1

    try:
        totals, languages = collect(token)
    except (urllib.error.URLError, RuntimeError) as error:
        print(f"Failed to fetch statistics: {error}", file=sys.stderr)
        return 1

    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, palette in THEMES.items():
        (ASSETS / f"stats-{name}.svg").write_text(render_stats(totals, palette))
        (ASSETS / f"languages-{name}.svg").write_text(
            render_languages(languages, palette)
        )

    print(f"Rendered cards for {LOGIN}: {totals}")
    print("Languages: " + ", ".join(f"{n} {s:.1f}%" for n, _, s in languages))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
