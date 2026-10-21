"""Story analysis pipeline — English technical artifact from gameStory index."""

from __future__ import annotations

import re
from pathlib import Path

from studio.config import Settings, ensure_project_dirs, get_settings
from studio.ingestion import ingest_game_story
from studio.models import (
    ApprovedFact,
    Assumption,
    StoryAnalysis,
    StoryIndex,
)


def _find_doc(index: StoryIndex, needle: str) -> str | None:
    needle = needle.lower()
    for doc in index.documents:
        if needle in doc.path.lower() or needle in doc.title.lower():
            return doc.path
    return None


def _read_repo_file(settings: Settings, rel_or_abs: str) -> str:
    path = Path(rel_or_abs)
    if not path.is_absolute():
        path = settings.repo_root / path
    return path.read_text(encoding="utf-8", errors="replace")


def _pull_bullets(text: str, markers: tuple[str, ...], limit: int = 12) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith(("-", "*")):
            continue
        body = line.lstrip("-* ").strip()
        if any(marker.lower() in body.lower() for marker in markers):
            lines.append(body)
        if len(lines) >= limit:
            break
    return lines


def build_analysis(
    index: StoryIndex | None = None,
    settings: Settings | None = None,
) -> StoryAnalysis:
    settings = settings or get_settings()
    index = index or ingest_game_story(settings)

    if index.missing:
        return StoryAnalysis(
            project_id=settings.project_id,
            concept="Unknown — gameStory/ missing or empty",
            genre="Unknown",
            platform="Unknown",
            campaign_time_budget_minutes=0,
            gameplay_loop="Cannot analyze without design inputs.",
            open_gaps=["gameStory/ is missing or empty"],
            assumptions=[
                Assumption(
                    id="A-missing-story",
                    text="No design package present; do not invent a game story.",
                )
            ],
            source_paths=[],
        )

    readme = _find_doc(index, "README")
    rules = _find_doc(index, "Proposal_v5")
    screenplay = _find_doc(index, "Screenplay")
    characters = _find_doc(index, "Character")
    art = _find_doc(index, "Art_Direction")
    validation = _find_doc(index, "Validation")
    playtest = _find_doc(index, "Playtest")

    source_paths = [
        p
        for p in (readme, rules, screenplay, characters, art, validation, playtest)
        if p
    ]

    rules_text = _read_repo_file(settings, rules) if rules else ""
    readme_text = _read_repo_file(settings, readme) if readme else ""
    validation_text = _read_repo_file(settings, validation) if validation else ""
    character_text = _read_repo_file(settings, characters) if characters else ""

    hearing_notes: list[str] = []
    for line in rules_text.splitlines():
        if "بانگ" in line or "Bang" in line or "شعاع" in line:
            cleaned = re.sub(r"\s+", " ", line.strip())
            if cleaned and cleaned not in hearing_notes:
                hearing_notes.append(cleaned[:220])
            if len(hearing_notes) >= 8:
                break

    chapter_structure = [
        "Ch0 setup / qanat / delivery (~25m design budget)",
        "Ch1–2 entry & camp (~15–20m)",
        "Ch3 soft sand / recovery (~25m)",
        "Ch4 Bahram time-dilated room (~30m)",
        "Ch5 plate defense (~25m)",
        "Ch6 caravanserai / optional ski / Dara (~25m)",
        "Ch7 evidence / R-17 (~20m)",
        "Ch8 heart of Hoor / Sara rescue (~25m)",
        "Ch9 northwest escape with companions (~35m)",
        "Ch10 endings: Circle / Escape / Ledge (~25m)",
        "Design campaign budget total: 270 minutes (not validated playtime)",
    ]

    character_names = [
        "Daniel (player) — skill and avoidance",
        "Sara — measurement and decision; unveiled in all languages",
        "Bahram — learned to ask for help; ~82 biological years in-room",
        "Kian — recording and fear (loop 0)",
        "Rostam — real help, incomplete warning",
        "Farhad — logistics contact",
        "Qasem — qanat / pengān in chapter 0",
        "Dara (companion animal)",
        "Tarantulas — three scales; hearing-driven, not magic vision",
    ]

    prohibitions = [
        "No Daniel–Sara romance",
        "No religious symbols in current character/props design",
        "Sara without hijab; hair visible; costume stable across languages",
        "Do not invent echoes outside E01–E07 without sourced approval",
        "Do not claim geo/hardware/playtest proof without evidence",
        "Historical v4 docs are not current production orders",
    ]

    # Pull recorded decisions from README when present
    for bullet in _pull_bullets(
        readme_text,
        ("دانیال", "سارا", "مذهبی", "رستم", "مرگ"),
        limit=8,
    ):
        if bullet not in prohibitions:
            prohibitions.append(bullet)

    approved = [
        ApprovedFact(
            id="AP-genre",
            text="First-person audio-survival with driving, companionship, exploration; fictional Lut canyon.",
            source=rules or "gameStory/",
        ),
        ApprovedFact(
            id="AP-platform",
            text="Primary platform PC/Steam; console stage 2; mobile only simplified later.",
            source=rules or "gameStory/",
        ),
        ApprovedFact(
            id="AP-window",
            text="Silence window [05:05:00, 05:05:10); Bang registration in window; resolution at E.",
            source=rules or "gameStory/",
        ),
        ApprovedFact(
            id="AP-hearing",
            text="Audible radius and Bang are independent tests; shelter blocks contact not sound.",
            source=rules or "gameStory/",
        ),
        ApprovedFact(
            id="AP-endings",
            text="Three silence paths: Circle / vehicle escape / Ledge(Anchor); death does not clear moral debt.",
            source=rules or "gameStory/",
        ),
    ]

    open_gaps = [
        "Bahram 20-year water/food/energy balance not proven (Validation open item)",
        "Real canyon elevation/coordinates not surveyed as game facts",
        "Anchor 1.5s margin is arithmetic only — not proven playability",
        "Playtests 1–3 not yet executed with players",
        "Main game engine not ADR-locked (must wait for audio signal unless human exception)",
        "English player-facing adaptation not complete in design package",
    ]
    for line in validation_text.splitlines():
        if "هنوز" in line and ("تأیید" in line or "آزمون" in line):
            cleaned = re.sub(r"\s+", " ", line.strip())
            if cleaned and cleaned not in open_gaps:
                open_gaps.append(cleaned[:240])
            if len(open_gaps) >= 10:
                break

    assumptions = [
        Assumption(
            id="AS-engine",
            text="Main engine remains undecided until C0 audio Go/No-Go unless human signs ADR early.",
            source=None,
        ),
        Assumption(
            id="AS-budget",
            text="270-minute chapter budget is a design target, not measured playtime.",
            source=rules,
        ),
        Assumption(
            id="AS-web-audio",
            text="Playtest tests 1 and 3 should start on Web Audio for speed (from Playtest Roadmap).",
            source=playtest,
        ),
    ]

    analysis = StoryAnalysis(
        project_id=settings.project_id,
        concept=(
            "Rad-e Hoor (The Solar Trace): audio-first survival in a Lut Desert canyon "
            "with a time loop gated by a ten-second dawn window."
        ),
        genre="First-person audio survival / narrative thriller with light off-road traversal",
        platform="PC/Steam primary; console later; gamepad + MK from day one",
        campaign_time_budget_minutes=270,
        gameplay_loop=(
            "Move and shelter while managing emitted sound; distinguish live sources from "
            "Hoor echoes; protect companions; resolve the dawn window without (or with) Bang; "
            "preserve evidence. Winch/hand-puller extend Daniel's craft under sound cost."
        ),
        hearing_notes=hearing_notes
        or [
            "Hearing unit table and Bang flags live in Rules §3.3 (Persian source).",
            "Device loud output attributes Bang to last conscious activator.",
        ],
        chapter_structure=chapter_structure,
        characters=character_names,
        prohibitions=prohibitions,
        audio_accessibility=[
            "Completable without microphone",
            "Headphones recommended but not mandatory for essential information",
            "Captions must not spoil echo speaker identity early",
            "Reduced-motion / reduced print FX modes required",
            "Hot/cold hand feedback via rumble with non-rumble alternatives",
        ],
        technical_risks=[
            "Teachability of loop + Bang + radii density",
            "3D audio latency and direction discrimination",
            "Chapter 9 dual-path companions vs vehicle",
            "Print-style visual readability vs performance",
            "Early engine lock before hearing proof",
        ],
        open_gaps=open_gaps,
        approved=approved,
        assumptions=assumptions,
        source_paths=source_paths,
    )

    # Character bible presence check
    if characters and "سارا" in character_text:
        analysis.approved.append(
            ApprovedFact(
                id="AP-sara-costume",
                text="Sara unveiled with visible short hair in current design bible.",
                source=characters,
            )
        )

    return analysis


def render_analysis_markdown(analysis: StoryAnalysis) -> str:
    lines = [
        f"# Story Analysis — {analysis.project_id}",
        "",
        f"Generated (UTC): {analysis.generated_at.isoformat()}",
        "",
        "> Technical artifact. Source design package remains authoritative in `gameStory/`.",
        "",
        "## Concept",
        analysis.concept,
        "",
        "## Genre",
        analysis.genre,
        "",
        "## Platform",
        analysis.platform,
        "",
        f"## Campaign time budget (design minutes): {analysis.campaign_time_budget_minutes}",
        "",
        "_This is a design budget, not validated playtime._",
        "",
        "## Gameplay loop",
        analysis.gameplay_loop,
        "",
        "## Hearing notes (cited / extracted)",
    ]
    for note in analysis.hearing_notes:
        lines.append(f"- {note}")
    lines.extend(["", "## Chapter structure"])
    for item in analysis.chapter_structure:
        lines.append(f"- {item}")
    lines.extend(["", "## Characters"])
    for item in analysis.characters:
        lines.append(f"- {item}")
    lines.extend(["", "## Prohibitions / recorded constraints"])
    for item in analysis.prohibitions:
        lines.append(f"- {item}")
    lines.extend(["", "## Audio & accessibility"])
    for item in analysis.audio_accessibility:
        lines.append(f"- {item}")
    lines.extend(["", "## Technical risks"])
    for item in analysis.technical_risks:
        lines.append(f"- {item}")
    lines.extend(["", "## Open gaps"])
    for item in analysis.open_gaps:
        lines.append(f"- {item}")
    lines.extend(["", "## APPROVED"])
    for fact in analysis.approved:
        lines.append(f"- `{fact.id}` {fact.text} — source: `{fact.source}`")
    lines.extend(["", "## ASSUMPTION"])
    for assumption in analysis.assumptions:
        src = assumption.source or "studio"
        lines.append(f"- `{assumption.id}` {assumption.text} — source: `{src}`")
    lines.extend(["", "## Source paths"])
    for path in analysis.source_paths:
        lines.append(f"- `{path}`")
    lines.append("")
    return "\n".join(lines)


def write_analysis(
    analysis: StoryAnalysis | None = None,
    settings: Settings | None = None,
) -> tuple[StoryAnalysis, Path]:
    settings = ensure_project_dirs(settings)
    analysis = analysis or build_analysis(settings=settings)
    path = settings.analysis_dir / "story-analysis.md"
    path.write_text(render_analysis_markdown(analysis), encoding="utf-8")
    analysis.markdown_path = str(path.relative_to(settings.repo_root))
    json_path = settings.analysis_dir / "story-analysis.json"
    json_path.write_text(analysis.model_dump_json(indent=2), encoding="utf-8")
    return analysis, path
