from studio.ingestion import ingest_game_story, write_index


def test_ingest_indexes_markdown(settings):
    index = ingest_game_story(settings)
    assert not index.missing
    assert len(index.documents) >= 2
    paths = {d.path for d in index.documents}
    assert any("README.md" in p for p in paths)
    assert all(d.sha256 for d in index.documents)


def test_ingest_missing_story(empty_story_settings):
    index = ingest_game_story(empty_story_settings)
    assert index.missing
    assert index.documents == []


def test_write_index(settings):
    index = ingest_game_story(settings)
    path = write_index(index, settings)
    assert path.exists()
    assert "documents" in path.read_text(encoding="utf-8")
