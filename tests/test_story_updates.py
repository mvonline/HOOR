from studio.analysis import build_analysis
from studio.ingestion import ingest_game_story
from studio.service import bootstrap_alignment


def test_story_update_changes_index_hash(settings):
    first = ingest_game_story(settings)
    readme = settings.game_story_dir / "README.md"
    before = next(d for d in first.documents if d.path.endswith("README.md"))
    readme.write_text(readme.read_text(encoding="utf-8") + "\n\nExtra note.\n", encoding="utf-8")
    second = ingest_game_story(settings)
    after = next(d for d in second.documents if d.path.endswith("README.md"))
    assert before.sha256 != after.sha256


def test_realign_after_story_change(settings):
    bootstrap_alignment(settings)
    proposal = settings.game_story_dir / "Rad-e-Hoor_Proposal_v5.0.md"
    proposal.write_text(
        proposal.read_text(encoding="utf-8") + "\n\n## New section\n\nUpdated constraint.\n",
        encoding="utf-8",
    )
    result = bootstrap_alignment(settings)
    analysis = build_analysis(settings=settings)
    assert result["document_count"] >= 2
    assert analysis.source_paths
