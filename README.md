# Rad-e Hoor — AI-Native Game Studio

Multi-agent production studio for **Rad-e Hoor** (The Solar Trace).

- Design source of truth: `gameStory/` (do not overwrite)
- Studio constitution: `masterPrompt.md` (English)
- Studio code: `studio/`
- Generated workspace: `projects/rade-hoor/`
- State DB: embedded **SQLite** at `projects/rade-hoor/data/studio.db` (no DB server to install)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Quick start

```bash
source .venv/bin/activate
python -m studio.cli align      # ingest + analysis + draft plan
python -m studio.cli status
python -m studio.cli submit
python -m studio.cli approve -n "Approved by human"
python -m studio.cli run -l 3
pytest
```

HTTP API: `python -m studio.cli serve` then `GET http://127.0.0.1:8000/status`.

Streamlit UI (separate folder `ui/`):

```bash
streamlit run ui/app.py
```
