"""
test_story.py
Run with: python -m pytest test_story.py -v
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))


# ── Story Engine ─────────────────────────────────────────────────────────────
class TestStoryEngineParsing:
    """Test the output parser without making real API calls."""

    def setup_method(self):
        # We test _parse_output in isolation — no API key needed
        from core.story_engine import StoryEngine
        # Temporarily mock the client init to avoid needing a key
        import unittest.mock as mock
        with mock.patch.object(StoryEngine, '_init_client'):
            self.engine = StoryEngine()

    def test_parse_clean_output(self):
        raw = (
            "The banyan tree stood at the centre of the village.\n\n"
            "Old men gathered beneath it every evening.\n\n"
            "TITLE: The Banyan's Long Memory\n"
            "IMAGE_PROMPT: Ancient banyan tree, village square, golden light, elders seated"
        )
        title, body, image_prompt = self.engine._parse_output(raw)
        assert title == "The Banyan's Long Memory"
        assert "banyan tree" in body.lower()
        assert "IMAGE_PROMPT" not in body
        assert "TITLE" not in body
        assert "Ancient banyan" in image_prompt

    def test_parse_missing_title(self):
        raw = "Just a story with no title line."
        title, body, _ = self.engine._parse_output(raw)
        assert title == "A Story from Rural India"
        assert body == "Just a story with no title line."

    def test_parse_missing_image_prompt(self):
        raw = "A short story.\nTITLE: Short Tale"
        title, body, image_prompt = self.engine._parse_output(raw)
        assert title == "Short Tale"
        assert "rural India village" in image_prompt

    def test_body_strips_metadata_lines(self):
        raw = "Story content.\n\nTITLE: Test\nIMAGE_PROMPT: test prompt"
        _, body, _ = self.engine._parse_output(raw)
        assert "TITLE" not in body
        assert "IMAGE_PROMPT" not in body


# ── Session Manager ───────────────────────────────────────────────────────────
class TestSessionManager:
    def setup_method(self):
        from core.session import SessionManager
        self.mgr = SessionManager()

    def test_add_story_returns_new_list(self):
        history = []
        result = self.mgr.add_story(history, "Test", "body", "Rajasthan", "Love", "Joyful")
        assert len(result) == 1
        assert result[0]["title"] == "Test"

    def test_original_history_not_mutated(self):
        history = []
        self.mgr.add_story(history, "Test", "body", "Rajasthan", "Love", "Joyful")
        assert len(history) == 0  # original unchanged

    def test_get_story_by_title(self):
        history = []
        history = self.mgr.add_story(history, "My Tale", "once upon a time", "Bihar", "Wisdom", "Serene")
        found = self.mgr.get_story(history, "My Tale")
        assert found is not None
        assert found["body"] == "once upon a time"

    def test_get_story_not_found(self):
        history = []
        result = self.mgr.get_story(history, "Nonexistent")
        assert result is None


# ── Data Loader ───────────────────────────────────────────────────────────────
class TestDataLoader:
    def test_load_stories_returns_list(self):
        from data.loader import load_stories
        stories = load_stories()
        assert isinstance(stories, list)

    def test_stories_have_required_fields(self):
        from data.loader import load_stories
        stories = load_stories()
        for story in stories:
            assert "title" in story
            assert "region" in story
            assert "mood" in story

    def test_get_story_by_title(self):
        from data.loader import get_story_by_title
        # This depends on data/stories.json being populated
        stories_list = __import__('data.loader', fromlist=['load_stories']).load_stories()
        if stories_list:
            first_title = stories_list[0]["title"]
            result = get_story_by_title(first_title)
            assert result is not None
            assert result["title"] == first_title


if __name__ == "__main__":
    pytest.main([__file__, "-v"])