#!/usr/bin/env python3
"""Verify every link and image across the profile and project READMEs.

A status code alone is not enough. Several widget services answer HTTP 200 and
draw the failure *inside* the SVG — shields.io renders "invalid" when its
upstream call is rate-limited, and the activity-graph widget rendered
"Can't fetch any contribution" while still returning 200. Both looked healthy
to a status-only check and broken to a human. So this inspects payloads too.

Error detection is phrase-based on purpose: matching a bare "404" also matches
the coordinate "404.2" inside a polyline, which is a false alarm, not a bug.

Usage:  python3 scripts/check_links.py [--profile-only]
"""

from __future__ import annotations

import concurrent.futures
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OWNER = "Ishrat-Bhullar"
PROJECT_REPOS = ("vectorless-chatbot", "rag-chatbot-mongodb", "sdlc-platform")

URL = re.compile(r'https://[^\s"\')>]+')
LOCAL_ASSET = re.compile(rf'/{OWNER}/{OWNER}/main/(assets/[^"\')\s]+)')

# Phrases a broken widget actually renders. No bare numbers — see the docstring.
BROKEN = re.compile(
    rb"can't fetch|cannot fetch|check your username|<title>[^<]*invalid"
    rb"|404:\s*not found|internal server error|deployment_paused",
    re.I,
)

# Hosts that answer automated requests with a challenge; a non-200 here is not
# evidence the link is dead.
UNVERIFIABLE = ("linkedin.com",)


def readme_sources(profile_only: bool) -> dict[str, str]:
    sources = {"profile": (ROOT / "README.md").read_text()}
    if profile_only:
        return sources
    for repo in PROJECT_REPOS:
        result = subprocess.run(
            ["gh", "api", f"repos/{OWNER}/{repo}/readme", "--jq", ".content"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            import base64
            sources[repo] = base64.b64decode(result.stdout).decode("utf-8", "replace")
        else:
            print(f"  warning: could not fetch {repo} README", file=sys.stderr)
    return sources


def check(url: str) -> tuple[str, object]:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "readme-link-check"})
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
            ctype = response.headers.get("Content-Type", "")
        if ("svg" in ctype or "json" in ctype) and BROKEN.search(body[:8000]):
            return url, "200, but the payload renders an error"
        if "svg" in ctype and len(body) < 200:
            return url, f"200, but the SVG is only {len(body)} bytes"
        if "image" in ctype and len(body) < 500:
            return url, f"200, but the image is only {len(body)} bytes"
        return url, 200
    except urllib.error.HTTPError as error:
        return url, error.code
    except Exception as error:                      # network/DNS/TLS
        return url, f"{type(error).__name__}"


def main() -> int:
    profile_only = "--profile-only" in sys.argv
    sources = readme_sources(profile_only)

    # Local asset references must exist on disk before anything is pushed.
    missing = sorted({
        ref for text in sources.values() for ref in LOCAL_ASSET.findall(text)
        if not (ROOT / ref).exists()
    })
    for ref in missing:
        print(f"  MISSING LOCALLY  {ref}")

    urls = sorted({
        u.rstrip(".,")
        for text in sources.values() for u in URL.findall(text)
    })
    checkable = [u for u in urls if not any(h in u for h in UNVERIFIABLE)]
    skipped = len(urls) - len(checkable)

    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for url, status in pool.map(check, checkable):
            if status != 200:
                failures.append((url, status))

    print(f"\nREADMEs checked : {', '.join(sources)}")
    print(f"URLs verified   : {len(checkable)}  (skipped {skipped}: bot-challenged hosts)")
    print(f"Local assets    : {len(missing)} missing")
    for url, status in failures:
        print(f"  FAIL [{status}]  {url}")
    total = len(failures) + len(missing)
    print(f"Failures        : {total}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
