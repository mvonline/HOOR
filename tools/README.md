# tools

Scripts that keep the v7 story package and the GitHub Pages site in step. Run from the repo root.

| Script | What it does |
| --- | --- |
| `python3 -I tools/check_continuity.py` | Read-only text checks: budget sums, mission/ID presence, local links, character ages, retired-rule leaks, site dialogues vs screenplay, site build contract. Always exits 0; read the report. |
| `python3 -I tools/sync_dialogues.py` | Rebuilds `sites/*/content/dialogues.json` from the screenplay's `speaker: «text»` lines and the recordings' stamps. `reader-edition.json` is edited by hand. |
| `python3 tools/build_snapshot.py` | Builds `sites/*/.snapshot/portal-data.json` (docs, gallery as WebP, maps, map.html, chapters, people, side stories). Needs Pillow. Git-ignored: it is the whole story in plain text. |

## Rebuild the site

```
python3 -I tools/sync_dialogues.py      # after editing the screenplay / recordings
cd sites/hoor-github-pages-20261121
npm ci
npm run snapshot                        # tools/build_snapshot.py
npm run encrypt                         # asks for the passphrase on a TTY; writes dist/content.hoor
npm run build                           # vite build + map engine (does not touch dist/content.hoor)
npm run check                           # tsc
```

`npm run build` does not create `content.hoor`, and CI only runs `npm run build`, so a push alone deploys a site that cannot unlock. Deploy the encrypted package deliberately (for example copy `dist/content.hoor` into `public/` before committing) once you have decided that.
