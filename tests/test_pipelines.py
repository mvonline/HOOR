from studio.analysis import build_analysis, write_analysis
from studio.ingestion import ingest_game_story
from studio.planning import build_production_plan, write_plan
from studio.service import bootstrap_alignment


def test_analysis_separates_approved_and_assumptions(settings):
    analysis = build_analysis(ingest_game_story(settings), settings)
    assert analysis.approved
    assert analysis.assumptions
    assert analysis.campaign_time_budget_minutes == 270
    ids = {a.id for a in analysis.assumptions}
    assert "AS-engine" in ids


def test_analysis_empty_story_does_not_invent(empty_story_settings):
    analysis = build_analysis(settings=empty_story_settings)
    assert "missing" in analysis.concept.lower() or "unknown" in analysis.concept.lower()
    assert analysis.assumptions
    assert analysis.source_paths == []


def test_plan_is_rade_hoor_layered(settings):
    analysis = build_analysis(settings=settings)
    plan = build_production_plan(analysis, settings)
    layers = {d.layer for d in plan.deliverables}
    assert {"P0", "P1", "P2", "P3", "P4", "P5"} <= layers
    assert any(d.id == "P1-00-SCAFFOLD" for d in plan.deliverables)
    assert any("Playtest 1" in d.title for d in plan.deliverables)
    assert len(plan.deliverables) >= 25


def test_bootstrap_writes_english_artifacts(settings):
    result = bootstrap_alignment(settings)
    analysis = settings.analysis_dir / "story-analysis.md"
    plan = settings.planning_dir / "production-plan.md"
    assert analysis.exists()
    assert plan.exists()
    text = analysis.read_text(encoding="utf-8")
    assert "APPROVED" in text
    assert "ASSUMPTION" in text
    assert result["plan_id"]
