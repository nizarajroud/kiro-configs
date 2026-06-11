---
name: youtube-transcript
description: YouTube transcript extraction — get transcripts, metadata, and languages from any YouTube video.
---
# YouTube Transcript

- **Status**: disabled
- **JSON key**: `youtube-transcript`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `uvx --from git+https://github.com/jkawamoto/mcp-youtube-transcript mcp-youtube-transcript`
- **Source**: https://github.com/jkawamoto/mcp-youtube-transcript (community)
- **Verdict**: disabled (not actively used)

## Tools

| Tool | Description |
|------|-------------|
| Get transcript | Extract subtitles/captions (with/without timestamps) |
| Get video metadata | Title, description, duration |
| List languages | Available transcript languages |

## Auth

- None required (no API key)

## Limitations

- Pagination for long videos
- Multi-language with fallback
- Currently disabled
