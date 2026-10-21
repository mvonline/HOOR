# Project workspace — rade-hoor

Generated studio outputs live here. Do **not** store original design truth here; that remains in `gameStory/`.

| Path | Purpose |
| --- | --- |
| `analysis/` | Story index + English story analysis |
| `planning/` | Production plan markdown/json |
| `decisions/` | Human approvals and open decisions |
| `reports/` | Progress / playtest / review reports |
| `artifacts/` | Build receipts and deliverable pointers |
| `data/` | Embedded SQLite file `studio.db` (created automatically; no DB server) |

Bootstrap:

```bash
source .venv/bin/activate
python -m studio.cli align
python -m studio.cli status
python -m studio.cli submit
python -m studio.cli approve --note "Approved"
python -m studio.cli tasks
python -m studio.cli run --limit 3
python -m studio.cli serve
```
