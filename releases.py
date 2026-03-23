#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
# ]
# ///

import argparse
import asyncio
import sys
from datetime import datetime, timedelta, timezone

import httpx

REPOS = [
    "anthropics/claude-code",
    "github/copilot-cli",
    "openai/codex",
]


async def fetch_releases(
    repo: str, since: datetime, client: httpx.AsyncClient
) -> tuple[str, list[dict]]:
    url = f"https://api.github.com/repos/{repo}/releases"
    try:
        resp = await client.get(url, params={"per_page": 30})
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"⚠ Failed to fetch {repo}: {e.response.status_code}", file=sys.stderr)
        return repo, []
    except httpx.RequestError as e:
        print(f"⚠ Failed to fetch {repo}: {e}", file=sys.stderr)
        return repo, []

    releases = []
    for r in resp.json():
        if r.get("prerelease") or r.get("draft"):
            continue
        published = datetime.fromisoformat(r["published_at"])
        if published < since:
            break
        releases.append(r)
    return repo, releases


def print_release(release: dict) -> None:
    tag = release["tag_name"]
    published = release["published_at"][:10]
    body = (release.get("body") or "").strip()
    url = release["html_url"]

    print(f"  {tag} ({published})")
    print(f"  {url}")
    if body:
        for line in body.splitlines():
            print(f"    {line}")
    print()


async def main() -> None:
    parser = argparse.ArgumentParser(description="Show recent GitHub releases")
    parser.add_argument(
        "-d", "--days", type=int, default=1,
        help="Show releases from the last N days (default: 1)",
    )
    args = parser.parse_args()

    since = datetime.now(timezone.utc) - timedelta(days=args.days)

    headers = {"Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient(headers=headers, timeout=15) as client:
        results = await asyncio.gather(
            *(fetch_releases(repo, since, client) for repo in REPOS)
        )

    for repo, releases in results:
        print(f"{'─' * 60}")
        print(f"📦 {repo}")
        print(f"{'─' * 60}")
        if not releases:
            print(f"  No releases in the last {args.days} day(s)\n")
        else:
            for r in releases:
                print_release(r)


if __name__ == "__main__":
    asyncio.run(main())
