#!/usr/bin/env python3
"""Rewrite the recent-activity block in README.md from public GitHub events.

The common off-the-shelf action for this only serialises PullRequest, Issue,
IssueComment and Release events, so an account whose activity is mostly commits
renders an empty section. This handles push and repository-creation events too.

Usage:  GITHUB_TOKEN=<token> python3 scripts/generate_activity.py
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
MAX_LINES = int(os.environ.get("MAX_LINES", "5"))
README = Path(__file__).resolve().parent.parent / "README.md"
START = "<!--START_SECTION:activity-->"
END = "<!--END_SECTION:activity-->"

FALLBACK = "_Recent public activity will appear here._"


def fetch_events(token: str) -> list[dict]:
    request = urllib.request.Request(
        f"https://api.github.com/users/{LOGIN}/events/public?per_page=100",
        headers={
            "Authorization": f"bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{LOGIN}-profile-activity",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def relative(timestamp: str) -> str:
    moment = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    days = (datetime.now(timezone.utc) - moment).days
    if days <= 0:
        return "today"
    if days == 1:
        return "yesterday"
    if days < 30:
        return f"{days} days ago"
    months = days // 30
    return "1 month ago" if months == 1 else f"{months} months ago"


def describe(event: dict) -> str | None:
    kind = event["type"]
    repo = event["repo"]["name"]
    link = f"[{repo.split('/')[-1]}](https://github.com/{repo})"
    payload = event.get("payload", {})

    if kind == "PushEvent":
        # The events API does not always include size/commits on PushEvent, so
        # only claim a count when one is actually present.
        count = payload.get("size") or len(payload.get("commits") or [])
        if not count:
            return f"Pushed to {link}"
        commits = "commit" if count == 1 else "commits"
        return f"Pushed {count} {commits} to {link}"
    if kind == "CreateEvent":
        ref_type = payload.get("ref_type")
        if ref_type == "repository":
            return f"Created repository {link}"
        # A new repository surfaces publicly as the creation of its default
        # branch, so these carry real signal. Word them for what they are.
        if ref_type in ("branch", "tag") and payload.get("ref"):
            return f"Created {ref_type} `{payload['ref']}` in {link}"
        return None
    if kind == "PullRequestEvent":
        number = payload["pull_request"]["number"]
        action = payload.get("action", "opened")
        if action == "closed" and payload["pull_request"].get("merged"):
            action = "merged"
        return f"{action.capitalize()} pull request #{number} in {link}"
    if kind == "IssuesEvent":
        number = payload["issue"]["number"]
        return f"{payload.get('action', 'opened').capitalize()} issue #{number} in {link}"
    if kind == "IssueCommentEvent":
        number = payload["issue"]["number"]
        return f"Commented on #{number} in {link}"
    if kind == "ReleaseEvent":
        return f"Released {payload['release']['tag_name']} in {link}"
    if kind == "ForkEvent":
        return f"Forked {link}"
    if kind == "WatchEvent":
        return f"Starred {link}"
    return None


def build_block(events: list[dict]) -> str:
    lines: list[str] = []
    seen: set[str] = set()
    for event in events:
        description = describe(event)
        if not description or description in seen:
            continue
        seen.add(description)
        lines.append(f"- {description} &nbsp;·&nbsp; <sub>{relative(event['created_at'])}</sub>")
        if len(lines) == MAX_LINES:
            break
    return "\n".join(lines) if lines else FALLBACK


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 1

    try:
        events = fetch_events(token)
    except (urllib.error.URLError, json.JSONDecodeError) as error:
        print(f"Failed to fetch events: {error}", file=sys.stderr)
        return 1

    content = README.read_text()
    if START not in content or END not in content:
        print("Activity markers are missing from README.md", file=sys.stderr)
        return 1

    head, _, remainder = content.partition(START)
    _, _, tail = remainder.partition(END)
    README.write_text(f"{head}{START}\n{build_block(events)}\n{END}{tail}")
    print(f"Rendered activity block for {LOGIN}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
