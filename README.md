# releases

A small Python script that fetches the latest non-prerelease GitHub releases for AI coding tools and prints their changelogs.

**Tracked repositories:**
- [anthropics/claude-code](https://github.com/anthropics/claude-code)
- [github/copilot-cli](https://github.com/github/copilot-cli)
- [openai/codex](https://github.com/openai/codex)

## Usage

Requires [uv](https://docs.astral.sh/uv/). No manual dependency installation needed.

```sh
# Releases from the last day (default)
uv run releases.py

# Releases from the last 7 days
uv run releases.py --days 7
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-d`, `--days` | Number of days to look back | `1` |
