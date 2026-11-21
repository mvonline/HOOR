"""Studio configuration rooted at the repository."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STUDIO_", extra="ignore")

    repo_root: Path = Path(__file__).resolve().parent.parent
    project_id: str = "rade-hoor"
    max_task_retries: int = 3
    ai_base_url: str = "https://api.openai.com/v1"
    ai_api_key: str | None = None
    ai_model: str = "gpt-4.1"
    ai_timeout_seconds: int = 180

    @property
    def game_story_dir(self) -> Path:
        return self.repo_root / "gameStory"

    @property
    def project_dir(self) -> Path:
        return self.repo_root / "projects" / self.project_id

    @property
    def analysis_dir(self) -> Path:
        return self.project_dir / "analysis"

    @property
    def planning_dir(self) -> Path:
        return self.project_dir / "planning"

    @property
    def decisions_dir(self) -> Path:
        return self.project_dir / "decisions"

    @property
    def reports_dir(self) -> Path:
        return self.project_dir / "reports"

    @property
    def artifacts_dir(self) -> Path:
        return self.project_dir / "artifacts"

    @property
    def data_dir(self) -> Path:
        return self.project_dir / "data"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "studio.db"


def get_settings() -> Settings:
    return Settings()


def ensure_project_dirs(settings: Settings | None = None) -> Settings:
    settings = settings or get_settings()
    for path in (
        settings.analysis_dir,
        settings.planning_dir,
        settings.decisions_dir,
        settings.reports_dir,
        settings.artifacts_dir,
        settings.data_dir,
    ):
        path.mkdir(parents=True, exist_ok=True)
    return settings
