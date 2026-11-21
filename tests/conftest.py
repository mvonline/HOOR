from __future__ import annotations

from pathlib import Path
import json
from unittest.mock import Mock

import pytest

from studio.config import Settings


@pytest.fixture()
def production_responses(monkeypatch):
    """Simulate only the provider; run the actual production and review workflow."""
    request = Mock(side_effect=[
        json.dumps({
            "summary": "Implemented test deliverable",
            "files": [{"path": "game/deliverable.txt", "content": "implemented\n"}],
            "acceptance_evidence": ["Deliverable exists"],
            "assumptions": [],
        }),
        json.dumps({"approved": True, "issues": [], "summary": "Reviewed"}),
    ])
    monkeypatch.setattr("studio.agents._request", request)
    return request


@pytest.fixture()
def tmp_repo(tmp_path: Path) -> Path:
    game_story = tmp_path / "gameStory"
    game_story.mkdir()
    (game_story / "README.md").write_text(
        "# Rad-e Hoor\n\n- Daniel and Sara have no romance.\n",
        encoding="utf-8",
    )
    (game_story / "Rad-e-Hoor_Proposal_v5.0.md").write_text(
        "# Rules\n\n## Hearing\n\n| Sound | Radius | Bang |\n| --- | --- | --- |\n| Whisper | 0 | no |\n| Yell | 50 | yes |\n\nبانگ در پنجره ثبت می‌شود.\n",
        encoding="utf-8",
    )
    (game_story / "Playtest_Roadmap.md").write_text(
        "# Playtest\n\nTests 1-3.\n",
        encoding="utf-8",
    )
    (tmp_path / "studio").mkdir()
    return tmp_path


@pytest.fixture()
def settings(tmp_repo: Path) -> Settings:
    return Settings(repo_root=tmp_repo, project_id="rade-hoor-test")


@pytest.fixture()
def empty_story_settings(tmp_path: Path) -> Settings:
    (tmp_path / "gameStory").mkdir()
    (tmp_path / "studio").mkdir()
    return Settings(repo_root=tmp_path, project_id="empty-story")
