"""
core/session.py
Manages in-session story history (no database needed).
"""

from datetime import datetime


class SessionManager:
    def add_story(self, history: list, title: str, body: str,
                  region: str, theme: str, mood: str) -> list:
        """Append a generated story to the session history list."""
        entry = {
            "title":      title,
            "body":       body,
            "region":     region,
            "theme":      theme,
            "mood":       mood,
            "created_at": datetime.now().strftime("%H:%M:%S"),
        }
        return history + [entry]

    def get_titles(self, history: list) -> list[str]:
        return [s["title"] for s in history]

    def get_story(self, history: list, title: str) -> dict | None:
        for s in history:
            if s["title"] == title:
                return s
        return None