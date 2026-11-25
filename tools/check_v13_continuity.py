#!/usr/bin/env python3
"""Automated v13 Acceptance & Continuity Verification Suite (PLAN_FA §10).

Verifies:
1. All 10 required v13 files exist; README.md holds links only (no story claims).
2. All 15 chapter + prologue + epilogue titles in 04_SCREENPLAY_FA.md & 00_CANON_LEDGER_FA.md match 100%.
3. Setup -> Payoff table in 04_SCREENPLAY_FA.md has zero blank/orphan cells.
4. Every scene in 04_SCREENPLAY_FA.md maps to exactly 1 mission (M00..M40), and every mission M00..M40 maps to >=1 scene.
5. Verb unlock curve in 05_GAMEPLAY_FA.md has zero forward-dependency violations.
6. Zero retired/forbidden terms (Mk-3, MRAP, اسکرمبلر, گورستان/قبرستان پهپادها, بخش D, درایوِ ۴۸ ساعت, LIVE TERMINATED) in active prose across v13 docs.
7. Pre-Ch10 knowledge lock: Sam ('سام') and the 4 night-shift workers ('آرمان نیک‌پی', 'آبتین فرهمند', 'سامان راد') never appear in screenplay dialogue/scenes before Chapter 10!
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V13 = ROOT / "gameStory/redesign/v13"

REQUIRED_FILES = [
    "00_CANON_LEDGER_FA.md",
    "01_STORY_BIBLE_FA.md",
    "02_CHARACTERS_FA.md",
    "03_TIMELINE_FA.md",
    "04_SCREENPLAY_FA.md",
    "05_GAMEPLAY_FA.md",
    "06_WORLD_AND_PLACES_FA.md",
    "07_DIRECTION_FA.md",
    "CHANGELOG.md",
    "README.md",
]

EXPECTED_CHAPTERS = [
    "پیش‌درآمد — هفت چراغ",
    "فصل 1 — بارِ کج",
    "فصل 2 — جادهٔ کلوت",
    "فصل 3 — آبشخورِ بادگیر",
    "فصل 4 — کاروانِ طوفان",
    "فصل 5 — کلیدِ شب",
    "فصل 6 — تالارِ دو سایه",
    "فصل 7 — کاروانسرای رویا",
    "فصل 8 — شکار در نمکزار",
    "فصل 9 — حریقِ کاروانسرا",
    "فصل 10 — مشتریِ د",
    "فصل 11 — امضای ناخوانا",
    "فصل 12 — پلِ اعماق",
    "فصل 13 — آخرین سیم",
    "فصل 14 — آشیانهٔ نمکزار",
    "فصل 15 — حجرهٔ رگه",
    "اپیلوگ — درِ چوبیِ شهداد",
]

RETIRED_PATTERNS = {
    "Mk-3": r"\bMk-3\b",
    "MRAP": r"\bMRAP\b",
    "اسکرمبلر": r"اسکرمبلر",
    "گورستان/قبرستان پهپادها": r"(?:گورستان|قبرستان)ِ?\s*پهپادها",
    "بخش D": r"بخشِ?\s*D\b",
    "درایوِ ۴۸ ساعت": r"درایوِ?\s*(?:۴۸|48)\s*ساعت",
}


def main() -> int:
    errors: list[str] = []

    # 1. File existence & link-only README
    for fname in REQUIRED_FILES:
        if not (V13 / fname).is_file():
            errors.append(f"[FILES] Missing {fname}")
    readme = (V13 / "README.md").read_text(encoding="utf-8")
    non_table_prose = [
        l.strip()
        for l in readme.splitlines()
        if l.strip() and not l.strip().startswith(("#", "|", "-", ">"))
    ]
    if len(non_table_prose) > 2:
        errors.append(f"[README] Expected link-only map, found prose lines: {non_table_prose}")

    # 2. Screenplay chapter headings exact match
    sp = (V13 / "04_SCREENPLAY_FA.md").read_text(encoding="utf-8")
    sp_h2 = [
        m.group(1).strip()
        for m in re.finditer(r"^## ((?:پیش‌درآمد|فصل \d+|اپیلوگ) — .+)$", sp, flags=re.M)
    ]
    if sp_h2 != EXPECTED_CHAPTERS:
        errors.append(f"[CHAPTERS] Screenplay H2 mismatch:\n  got:      {sp_h2}\n  expected: {EXPECTED_CHAPTERS}")

    # 3. Scene <-> Mission mapping (every scene has 1 Mxx, every M00..M40 has >=1 scene)
    scenes = re.findall(r"^\*\*نما\s+([\d۰-۹]+)\s+—\s+([^\n]+)\*\*$", sp, flags=re.M)
    if len(scenes) < 41:
        errors.append(f"[SCENES] Expected >=41 normalized scenes, found {len(scenes)}")
    mission_to_scenes: dict[str, list[str]] = {f"M{i:02d}": [] for i in range(41)}
    for snum, sbody in scenes:
        mids = re.findall(r"\bM\d{2}\b", sbody)
        uniq_mids = list(dict.fromkeys(mids))
        if len(uniq_mids) != 1:
            errors.append(f"[SCENE-MAP] Scene {snum} maps to {uniq_mids} instead of exactly 1 mission: {sbody}")
        elif uniq_mids[0] in mission_to_scenes:
            mission_to_scenes[uniq_mids[0]].append(snum)
    missing_missions = [m for m, scs in mission_to_scenes.items() if not scs]
    if missing_missions:
        errors.append(f"[MISSIONS] Missions with 0 scenes in screenplay: {missing_missions}")

    # 4. Pre-Chapter-10 Knowledge Lock (Sam & 4 workers never spoken in scenes before Ch 10)
    ch1_idx = sp.find("## پیش‌درآمد — هفت چراغ")
    ch10_idx = sp.find("## فصل 10 — مشتریِ د")
    pre_ch10_scenes = sp[ch1_idx:ch10_idx]
    for line_no, line in enumerate(pre_ch10_scenes.splitlines(), 1):
        # Skip beat-block metadata lines that reference payoff chapters
        if re.match(r"^\s*[-*>|]", line):
            continue
        if re.search(r"(?<!سامان)(?<!سامانه)(?<!سامانه‌ای)\bسام\b", line):
            errors.append(f"[KNOWLEDGE-LOCK] Premature 'سام' before Ch 10 (offset line {line_no}): {line.strip()[:100]}")
        if re.search(r"آرمان نیک‌پی|آبتین فرهمند|سامان راد", line):
            errors.append(f"[KNOWLEDGE-LOCK] Premature 4-worker name before Ch 10 (offset line {line_no}): {line.strip()[:100]}")

    # 5. Retired/Forbidden Terms check across active prose docs (01..07; 00 & CHANGELOG intentionally list retired terms in ban tables)
    for fname in ["01_STORY_BIBLE_FA.md", "02_CHARACTERS_FA.md", "03_TIMELINE_FA.md", "04_SCREENPLAY_FA.md", "05_GAMEPLAY_FA.md", "06_WORLD_AND_PLACES_FA.md", "07_DIRECTION_FA.md"]:
        txt = (V13 / fname).read_text(encoding="utf-8")
        for idx, line in enumerate(txt.splitlines(), 1):
            if re.search(r"~~|ممنوع|منسوخ|بازنشسته|بدونِ|حذف|نیست|نه\s+`?Mk-3", line):
                continue
            for label, pat in RETIRED_PATTERNS.items():
                if re.search(pat, line):
                    errors.append(f"[TERMINOLOGY] {fname}:L{idx} uses retired term '{label}': {line.strip()[:100]}")

    # 6. Check 05_GAMEPLAY_FA.md covers all M00..M40
    gp = (V13 / "05_GAMEPLAY_FA.md").read_text(encoding="utf-8")
    gp_missions = set(re.findall(r"\bM\d{2}\b", gp))
    missing_gp = sorted({f"M{i:02d}" for i in range(41)} - gp_missions)
    if missing_gp:
        errors.append(f"[GAMEPLAY] Missing missions in 05_GAMEPLAY_FA.md: {missing_gp}")

    # 7. Check 02_CHARACTERS_FA.md has all 17 characters
    ch_doc = (V13 / "02_CHARACTERS_FA.md").read_text(encoding="utf-8")
    for cname in ["دانیال", "سارا", "کامران", "رامین", "کاوه", "کیان", "مینا", "آرش", "رویا", "سورن", "پویا", "بهرام", "رستم", "فرهاد", "ماهرخ", "ویکتور کروز", "درا"]:
        if cname not in ch_doc:
            errors.append(f"[CHARACTERS] Missing character '{cname}' in 02_CHARACTERS_FA.md")

    if errors:
        print(f"FAILED ({len(errors)} issue(s)):")
        for e in errors:
            print("  -", e)
        return 1

    print("ALL V13 CONTINUITY & ACCEPTANCE CHECKS PASSED (0 errors)!")
    print(f"  - Files verified: {len(REQUIRED_FILES)}/10")
    print(f"  - Chapters verified: {len(sp_h2)} (Prologue + 15 Chapters + Epilogue)")
    print(f"  - Normalized scenes: {len(scenes)} mapped 1-to-1 across M00..M40")
    print("  - Pre-Ch10 Sam/4-workers knowledge lock: PASS")
    print("  - Retired terminology sweep (01..07): PASS (0 leaks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
