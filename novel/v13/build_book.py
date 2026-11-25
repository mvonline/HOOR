#!/usr/bin/env python3
"""Compile written v13 chapters in novel/v13/chapters/ into RAD_E_HOOR_NOVEL_V13_FA.md and audit canon rules."""
from pathlib import Path
import re

NOVEL_DIR = Path(__file__).resolve().parent
CHAPTERS_DIR = NOVEL_DIR / 'chapters'
OUT_FILE = NOVEL_DIR / 'RAD_E_HOOR_NOVEL_V13_FA.md'
WORDS_PER_PAGE = 280  # Standard Persian trade paperback (قطع رقعی)

FORBIDDEN_TERMS = (
    'Mk-3',
    'اسکرمبلر',
    'موتور کراس',
    'موتورِ کراس',
    'گورستان پهپادها',
    'گورستانِ پهپادها',
    'قبرستان پهپادها',
    'قبرستانِ پهپادها',
    'پاترول',
    'درایو ۴۸ ساعت',
    'درایوِ ۴۸ ساعت',
    'MRAP',
    'گان‌شیپ',
    'وزارتخانه',
)

PART_FILES = {'ch01.md', 'ch08.md', 'ch15.md'}
CHAPTER_HEADER_RE = re.compile(r'^## فصل [۰-۹]+ — .+', re.MULTILINE)
EPILOGUE_HEADER_RE = re.compile(r'^## اپیلوگ — درِ چوبیِ شهداد\s*$', re.MULTILINE)


def audit_chapter(filename: str, text: str) -> list[str]:
    warnings: list[str] = []
    first_line = text.splitlines()[0].strip() if text else ''
    if filename in PART_FILES and not first_line.startswith('# بخش '):
        warnings.append(f'{filename}: missing `# بخش ...` header on line 1')
    if filename not in PART_FILES and first_line.startswith('# بخش '):
        warnings.append(f'{filename}: unexpected `# بخش ...` header (allowed only in ch01, ch08, ch15)')

    if filename == 'ch21_epilogue.md':
        if not EPILOGUE_HEADER_RE.search(text):
            warnings.append(f'{filename}: missing exact `## اپیلوگ — درِ چوبیِ شهداد` header')
    else:
        if not CHAPTER_HEADER_RE.search(text):
            warnings.append(f'{filename}: missing `## فصل N — ...` header')

    for term in FORBIDDEN_TERMS:
        if term in text:
            warnings.append(f'{filename}: contains deprecated/forbidden term `{term}`')
    return warnings


def main() -> None:
    files = sorted(CHAPTERS_DIR.glob('ch*.md'))
    if not files:
        print('No chapters found in novel/v13/chapters/')
        return

    parts = [
        '# ردِ هور\n',
        '> **رمانِ اکشن-تریلرِ ادبیِ «ردِ هور» (نسخهٔ ۱۳)**\n',
        '---\n',
    ]
    total_words = 0
    all_warnings: list[str] = []

    print(f'{"File":<24} {"Words":>8} {"Est. Pages":>11}')
    print('-' * 46)
    for f in files:
        text = f.read_text(encoding='utf-8-sig').strip()
        words = len(text.split())
        total_words += words
        pages = words / WORDS_PER_PAGE
        print(f'{f.name:<24} {words:>8,} {pages:>10.1f}')
        all_warnings.extend(audit_chapter(f.name, text))
        parts.append(text + '\n\n---\n')

    OUT_FILE.write_text('\n'.join(parts), encoding='utf-8')
    print('-' * 46)
    print(f'{"TOTAL":<24} {total_words:>8,} {total_words / WORDS_PER_PAGE:>10.1f}')
    print(f'\nCompiled manuscript -> {OUT_FILE}')

    if all_warnings:
        print('\n[CANON / HEADING AUDIT WARNINGS]')
        for w in all_warnings:
            print(f'  - {w}')
    else:
        print('Canon & parseNovel() heading audit: OK (0 warnings)')


if __name__ == '__main__':
    main()
