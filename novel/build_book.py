#!/usr/bin/env python3
"""Compile written chapters in novel/chapters/ into a single manuscript and report page counts."""
from pathlib import Path

NOVEL_DIR = Path(__file__).resolve().parent
CHAPTERS_DIR = NOVEL_DIR / 'chapters'
OUT_FILE = NOVEL_DIR / 'RAD_E_HOOR_NOVEL_FA.md'
WORDS_PER_PAGE = 280  # Standard Persian trade paperback (قطع رقعی)


def main() -> None:
    files = sorted(CHAPTERS_DIR.glob('ch*.md'))
    if not files:
        print('No chapters found in novel/chapters/')
        return

    parts = [
        '# ردِ هور\n',
        '> **رمانِ مرجعِ جهانِ «ردِ هور»**\n',
        '---\n',
    ]
    total_words = 0
    print(f'{"File":<24} {"Words":>8} {"Est. Pages":>11}')
    print('-' * 46)
    for f in files:
        text = f.read_text(encoding='utf-8-sig').strip()
        words = len(text.split())
        total_words += words
        pages = words / WORDS_PER_PAGE
        print(f'{f.name:<24} {words:>8,} {pages:>10.1f}')
        parts.append(text + '\n\n---\n')

    OUT_FILE.write_text('\n'.join(parts), encoding='utf-8')
    print('-' * 46)
    print(f'{"TOTAL":<24} {total_words:>8,} {total_words / WORDS_PER_PAGE:>10.1f}')
    print(f'\nCompiled manuscript -> {OUT_FILE}')


if __name__ == '__main__':
    main()
