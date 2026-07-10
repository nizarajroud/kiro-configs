---
name: xpoz-mcp
description: Search Twitter, Instagram, Reddit & TikTok from AI agents. 1.5B+ posts indexed. Natural language queries, CSV exports, tracking/monitoring. Remote server (Streamable HTTP).
---
# xpoz-mcp — Social Intelligence Search

- **Status**: installed (trial token, 5 days)
- **JSON key**: `xpoz-mcp`
- **Agent**: **connect3**
- **Type**: Remote (Streamable HTTP — no local process)
- **URL**: `https://mcp.xpoz.ai/mcp`
- **Auth**: OAuth 2.1 (Google sign-in) ou trial token (Bearer header)
- **Source**: https://github.com/XPOZpublic/xpoz-mcp (⭐8, org XPOZpublic)
- **Version**: v3.0.0 (server-side)
- **Verdict**: adopted — unique MCP for cross-platform social search (1.5B+ posts)

## Tools (42)

### Twitter / X (14 tools)
| Tool | Description |
|------|-------------|
| `searchTwitterUsers` | Find users by name, bio, keywords |
| `getTwitterUser` | Profile details (followers, bio, metrics) |
| `getTwitterUsersByKeywords` | Discover users posting about topics |
| `getTwitterUserConnections` | Followers/following list |
| `getTwitterPostsByKeywords` | Search tweets by keywords/hashtags |
| `getTwitterPostsByAuthor` | Tweets from a specific user |
| `getTwitterPostsByIds` | Fetch specific tweets |
| `getTwitterPostComments` | Replies to a tweet |
| `getTwitterPostRetweets` | Retweets of a tweet |
| `getTwitterPostQuotes` | Quote tweets |
| `getTwitterPostInteractingUsers` | Users who liked/retweeted |
| `countTweets` | Count tweets (hourly/daily buckets) |
| `checkOperationStatus` | Poll async exports |
| `cancelOperation` | Cancel running operations |

### Instagram (9 tools)
| Tool | Description |
|------|-------------|
| `searchInstagramUsers` | Find users |
| `getInstagramUser` | Profile details |
| `getInstagramUsersByKeywords` | Discover users by topics |
| `getInstagramUserConnections` | Followers/following |
| `getInstagramPostsByKeywords` | Search posts |
| `getInstagramPostsByUser` | Posts from user |
| `getInstagramPostsByIds` | Specific posts |
| `getInstagramPostInteractingUsers` | Likers/commenters |
| `getInstagramCommentsByPostId` | Comments on a post |

### Reddit (9 tools)
| Tool | Description |
|------|-------------|
| `searchRedditUsers` | Find users |
| `getRedditUser` | Profile + karma |
| `getRedditUsersByKeywords` | Active users in topics |
| `getRedditPostsByKeywords` | Search across subreddits |
| `getRedditPostWithCommentsById` | Post + comment tree |
| `getRedditCommentsByKeywords` | Search comments |
| `searchRedditSubreddits` | Find subreddits |
| `getRedditSubredditWithPostsByName` | Subreddit metadata + posts |
| `getRedditSubredditsByKeywords` | Discover subreddits |

### TikTok (7 tools)
| Tool | Description |
|------|-------------|
| `searchTiktokUsers` | Find creators |
| `getTiktokUser` | Creator profile |
| `getTiktokUsersByKeywords` | Discover creators by topic |
| `getTiktokPostsByKeywords` | Search videos by keywords |
| `getTiktokPostsByUser` | Videos by creator |
| `getTiktokPostsByIds` | Specific videos |
| `getTiktokCommentsByPostId` | Comments on a video |

### Tracking & Monitoring (3 tools)
| Tool | Description |
|------|-------------|
| `addTrackedItems` | Subscribe to monitoring |
| `getTrackedItems` | List active tracked items |
| `removeTrackedItems` | Stop monitoring |

## Configuration MCP

```json
"xpoz-mcp": {
  "description": "Search Twitter, Instagram, Reddit & TikTok — 1.5B+ posts indexed. Social intelligence, lead gen, brand monitoring.",
  "type": "streamable-http",
  "url": "https://mcp.xpoz.ai/mcp",
  "headers": {
    "Authorization": "Bearer <TOKEN>"
  },
  "disabled": false
}
```

## Auth

- **Trial token** (5 days, limited results): `curl -X POST https://api.xpoz.ai/api/trial/token -H "Content-Type: application/json" -d '{"source":"cli"}'`
- **Full access**: OAuth 2.1 via Google sign-in at xpoz.ai/get-token
- Current trial: `TRIALSsXUC-MjMpiCgYtljeBNuwrEJNyp75xCfvxqDmHT4xg` (expires in 5 days from 2026-07-10)

## Pricing (xpoz.ai/pricing)

À vérifier — free tier limité, plans payants pour full results + exports.

## Placement

✅ **Placé sur connect3** (créé par IT-Supervisor le 2026-07-10). Agent dédié social intelligence.

## Notes

- Remote server — zéro RAM locale, zéro processus
- 1.5B+ posts indexés — recherche en langage naturel
- CSV exports jusqu'à 500K lignes
- Async operations pour les gros exports
