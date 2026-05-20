#!/usr/bin/env python3
"""Browser Bookmarks MCP Server — search Chrome and Edge bookmarks."""

import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

CHROME_BOOKMARKS = Path("/mnt/c/Users/nizar/AppData/Local/Google/Chrome/User Data/Default/Bookmarks")
EDGE_BOOKMARKS = Path("/mnt/c/Users/nizar/AppData/Local/Microsoft/Edge/User Data/Default/Bookmarks")

mcp = FastMCP("bookmarks")


def _extract_bookmarks(node, folder=""):
    results = []
    name = node.get("name", "")
    current_folder = f"{folder}/{name}" if folder else name
    if node.get("type") == "url":
        results.append({"title": name, "url": node["url"], "folder": folder})
    for child in node.get("children", []):
        results.extend(_extract_bookmarks(child, current_folder))
    return results


def _load_all():
    all_bookmarks = []
    for path, browser in [(CHROME_BOOKMARKS, "Chrome"), (EDGE_BOOKMARKS, "Edge")]:
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for root in data.get("roots", {}).values():
            if isinstance(root, dict):
                for bm in _extract_bookmarks(root):
                    bm["browser"] = browser
                    all_bookmarks.append(bm)
    return all_bookmarks


@mcp.tool()
def search_bookmarks(query: str, max_results: int = 20) -> str:
    """Search bookmarks by keyword in title, URL, or folder name. Searches both Chrome and Edge."""
    q = query.lower()
    terms = q.split()
    bookmarks = _load_all()
    scored = []
    for bm in bookmarks:
        text = f"{bm['title']} {bm['url']} {bm['folder']}".lower()
        if all(t in text for t in terms):
            score = sum(text.count(t) for t in terms)
            scored.append((score, bm))
    scored.sort(key=lambda x: -x[0])
    results = [s[1] for s in scored[:max_results]]
    return json.dumps({"query": query, "count": len(results), "total_matches": len(scored), "bookmarks": results}, indent=2)


@mcp.tool()
def list_bookmark_folders(browser: str = "all") -> str:
    """List all bookmark folders. Browser: 'chrome', 'edge', or 'all'."""
    bookmarks = _load_all()
    folders = set()
    for bm in bookmarks:
        if browser != "all" and bm["browser"].lower() != browser.lower():
            continue
        if bm["folder"]:
            folders.add(f"[{bm['browser']}] {bm['folder']}")
    return json.dumps({"folders": sorted(folders), "count": len(folders)}, indent=2)


@mcp.tool()
def get_bookmarks_in_folder(folder_name: str, max_results: int = 50) -> str:
    """Get all bookmarks in a specific folder (partial match on folder path)."""
    q = folder_name.lower()
    bookmarks = _load_all()
    results = [bm for bm in bookmarks if q in bm["folder"].lower()][:max_results]
    return json.dumps({"folder": folder_name, "count": len(results), "bookmarks": results}, indent=2)


@mcp.tool()
def bookmark_stats() -> str:
    """Get statistics about bookmarks (count per browser, top folders)."""
    bookmarks = _load_all()
    chrome = sum(1 for b in bookmarks if b["browser"] == "Chrome")
    edge = sum(1 for b in bookmarks if b["browser"] == "Edge")
    folders = {}
    for bm in bookmarks:
        f = bm["folder"] or "(root)"
        folders[f] = folders.get(f, 0) + 1
    top_folders = sorted(folders.items(), key=lambda x: -x[1])[:20]
    return json.dumps({"total": len(bookmarks), "chrome": chrome, "edge": edge, "top_folders": top_folders}, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
