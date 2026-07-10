---
name: video-transcriber-mcp
description: Transcribe videos from 1000+ platforms (TikTok, YouTube, Instagram, Twitter/X, etc.) using whisper.cpp locally. Input = URL, Output = full transcript.
---
# video-transcriber-mcp (Rust)

- **Status**: installed
- **JSON key**: `video-transcriber-mcp`
- **Agent**: connect1
- **Wrapper**: none (direct binary, no secrets)
- **Binary**: `/home/nizar/.cargo/bin/video-transcriber-mcp`
- **Source**: https://github.com/nhatvu148/video-transcriber-mcp-rs
- **Crate**: video-transcriber-mcp v0.8.0 (cargo install)
- **Verdict**: adopted — replaces youtube-transcript with multi-platform support + local Whisper

## Tools

| Tool | Description |
|------|-------------|
| `transcribe_video` | Transcribe any video URL (1000+ platforms) via yt-dlp + whisper.cpp |
| `backfill` | Bulk transcription utility (separate binary) |

## How it works

1. Takes a video URL (TikTok, YouTube, Instagram, Twitter/X, Twitch, Vimeo, etc.)
2. Downloads audio via `yt-dlp`
3. Transcribes locally via `whisper.cpp` (no cloud API)
4. Returns full text transcript

## Dependencies

- Rust (installed: rustc 1.93.1)
- yt-dlp (installed: 2026.06.09)
- ffmpeg (installed: 4.4.2)
- whisper.cpp model: small (compatible GPU MX450 2GB VRAM)
- Models stored in: `~/.cache/video-transcriber-mcp/models/`

## Configuration

```json
"video-transcriber-mcp": {
  "description": "Transcribe videos from 1000+ platforms (TikTok, YouTube, Instagram, etc.) using local Whisper. Input = URL.",
  "command": "video-transcriber-mcp",
  "args": [],
  "env": {
    "RUST_LOG": "info"
  },
  "disabled": false
}
```

## Replaces

- `youtube-transcript` (disabled on connect1) — this server does everything youtube-transcript did + 1000 more platforms + local Whisper fallback

## Notes

- No API key needed (100% local processing)
- First transcription downloads the Whisper model (~500 MB for small)
- Processing time: ~10-30 sec per video depending on length
- GPU acceleration available if CUDA/Metal configured
