"""Discover and index files under gameStory/."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from studio.config import Settings, get_settings
from studio.models import StoryDocument, StoryIndex

HISTORICAL_HINTS = (
    "test-report",
    "proposal_and_scenario",
    "backup",
    "v4.",
    "legacy",
)

CURRENT_DOCS = {
    "readme.md",
    "rad-e-hoor_proposal_v5.0.md",
    "rad-e-hoor_full_screenplay_fa.md",
    "rad-e-hoor_character_bible.md",
    "rad-e-hoor_art_direction_bible.md",
    "rad-e-hoor_validation_report.md",
    "playtest_roadmap.md",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def _extract_headings(text: str, limit: int = 40) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,3})\s+(.+)$", line.strip())
        if match:
            headings.append(match.group(2).strip())
            if len(headings) >= limit:
                break
    return headings


def _summarize(text: str, max_chars: int = 400) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    # Prefer first non-heading paragraph
    for paragraph in paragraphs:
        if not paragraph.startswith("#"):
            cleaned = re.sub(r"\s+", " ", paragraph)
            return cleaned[:max_chars]
    if paragraphs:
        cleaned = re.sub(r"\s+", " ", paragraphs[0])
        return cleaned[:max_chars]
    return ""


def _is_historical(path: Path) -> bool:
    name = path.name.lower()
    if name in CURRENT_DOCS:
        return False
    return any(hint in name for hint in HISTORICAL_HINTS)


def ingest_game_story(settings: Settings | None = None) -> StoryIndex:
    settings = settings or get_settings()
    root = settings.game_story_dir
    index = StoryIndex(
        project_id=settings.project_id,
        root=str(root),
        missing=not root.exists(),
    )

    if index.missing:
        index.notes.append(
            "gameStory/ is missing. Add design documents before production."
        )
        return index

    if not any(root.iterdir()):
        index.missing = True
        index.notes.append("gameStory/ exists but is empty.")
        return index

    patterns = ("*.md", "*.txt", "*.json")
    files: list[Path] = []
    for pattern in patterns:
        files.extend(sorted(root.rglob(pattern)))

    for path in files:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
            index.notes.append(f"Non-UTF8 characters replaced in {path.name}")

        from datetime import datetime

        rel = path.relative_to(settings.repo_root).as_posix()
        mtime_iso = datetime.fromtimestamp(path.stat().st_mtime).isoformat()
        index.documents.append(
            StoryDocument(
                path=rel,
                title=_extract_title(text, path.stem),
                sha256=_sha256(path),
                size_bytes=path.stat().st_size,
                mtime_iso=mtime_iso,
                headings=_extract_headings(text),
                summary=_summarize(text),
                is_historical=_is_historical(path),
            )
        )

    current = [d for d in index.documents if not d.is_historical]
    historical = [d for d in index.documents if d.is_historical]
    index.notes.append(
        f"Indexed {len(index.documents)} files "
        f"({len(current)} current, {len(historical)} historical)."
    )
    return index


def write_index(index: StoryIndex, settings: Settings | None = None) -> Path:
    from studio.config import ensure_project_dirs

    settings = ensure_project_dirs(settings)
    out = settings.analysis_dir / "story-index.json"
    out.write_text(index.model_dump_json(indent=2), encoding="utf-8")
    return out
