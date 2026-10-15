---
name: youtube-search
description: YouTube Data API v3 — search and discover the most relevant videos/channels/playlists on any topic (reviews, tutorials). Fetch video details + transcripts.
---
# YouTube Search (youtube-search)

- **Status**: installed (placeholder key — needs YouTube Data API v3 key)
- **JSON key**: `youtube-search` (in `settings/mcp.json`, global — all agents)
- **Package**: `zubeid-youtube-mcp-server` (npm) — v1.0.2
- **Source**: [ZubeidHendricks/youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server) ⭐582, MIT, 140 forks
- **Wrapper**: `wrappers/youtube_mcp_wrapper.py` (loads `YOUTUBE_API_KEY` from `.env`)
- **Env**: `YOUTUBE_API_KEY` (required), `YOUTUBE_API_KEY2`/`3` (optional fallbacks, auto-rotate on quota), `YOUTUBE_TRANSCRIPT_LANG` (default `en`)
- **Placement**: cross-cutting (global `settings/mcp.json`) — accessible by all domain agents
- **Verdict**: ADOPTED — most-starred and best-maintained YouTube search MCP. Rich search filters (subscriber band, creator-only, indie_priority sort) ideal for finding quality product reviews/tutorials.

## 10 Tools

| Tool | Purpose |
|------|---------|
| `videos_searchVideos` | **Search videos** (query + order, date range, channel sub band, creatorOnly, sortBy) |
| `videos_getVideo` | Video details by ID |
| `transcripts_getTranscript` | Video transcript (language fallback) |
| `channels_getChannel` / `channels_getChannels` | Channel info |
| `channels_searchChannels` | Search channels |
| `channels_findCreators` | Find creator channels from video mentions |
| `channels_listVideos` | Videos from a channel |
| `playlists_getPlaylist` / `playlists_getPlaylistItems` | Playlist info/items |

## Notes

- Server validates the API key only when a tool is called (startup works with placeholder).
- `videos_searchVideos.sortBy` supports: `relevance`, `subscribers_asc`, `subscribers_desc`, `indie_priority`, `recent_activity`.
- Quota: YouTube Data API v3 = 10,000 units/day free; a search = 100 units (~100 searches/day). Add `YOUTUBE_API_KEY2`/`3` for more headroom.
- Complementary to `video-transcriber-mcp` (connect1) which transcribes known URLs — this one DISCOVERS videos.
