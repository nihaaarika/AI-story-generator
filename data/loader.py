"""
data/loader.py
Loads curated stories from stories.json
"""

import json
from pathlib import Path

STORIES_FILE = Path(__file__).parent / "stories.json"


def load_stories() -> list[dict]:
    """Load all stories from the JSON database."""
    if not STORIES_FILE.exists():
        return []
    with open(STORIES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_story_by_title(title: str) -> dict | None:
    for story in load_stories():
        if story.get("title") == title:
            return story
    return None