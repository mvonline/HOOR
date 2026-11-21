"""Rebuild sites/hoor-github-pages-*/content/dialogues.json from the v11 AAA screenplay.

Spoken lines come from SCREENPLAY_V11_FA.md (`speaker: «text»`).
Run: python3 -I tools/sync_dialogues.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V7 = ROOT / 'gameStory/redesign/v7-20261121'
V11 = ROOT / 'gameStory/redesign/v11-aaa'
CONTENT = ROOT / 'sites/hoor-github-pages-20261121/content'

screenplay = (V11 / 'SCREENPLAY_V11_FA.md').read_text(encoding='utf-8')
recordings_doc = (V7 / 'RECORDINGS_DOCUMENTS_AND_DIRECTION_FA.md').read_text(encoding='utf-8')

old = json.loads((CONTENT / 'dialogues.json').read_text(encoding='utf-8'))

CAST = {
    'دانیال', 'سارا', 'کامران', 'کیان', 'بهرام', 'رستم', 'مینا', 'ماهرخ',
    'آرش', 'پروانه', 'اسماعیل', 'مهدی', 'فرهاد', 'نادر', 'رویا', 'یونس',
    'حسین', 'قاسم', 'حیدر', 'سعید', 'مریم', 'ناهید', 'سهراب', 'لیلا',
    'صادقی', 'زن', 'مردِ ۹', 'مردِ ۷',
}


def clean_speaker(raw: str) -> str:
    sp = re.split(r'[،(]', raw)[0].strip()
    if sp in CAST:
        return sp
    first = sp.split()[0] if sp.split() else sp
    if first in CAST:
        return first
    if len(sp) > 22:
        return first.rstrip('ِ')
    return sp


chapter_re = re.compile(r'^## فصل (\d+) — (.+)$')
scene_re = re.compile(r'^\*\*نما ([\d۰-۹]+[ب]?) — ([^*]+?)\*\*\s*$')
line_re = re.compile(r'^([^«»\n:]{1,65}):\s*«(.+)»\s*$')

chapters = []
current_chapter = None
current_scene = None
epilogue_chapter = None

for raw in screenplay.splitlines():
    if raw.startswith('## پیش‌درآمد'):
        current_chapter = {'number': 1, 'title': 'پیش‌درآمد', 'scenes': [], 'prologue': True}
        chapters.append(current_chapter)
        current_scene = None
        continue
    if raw.startswith('## اپیلوگ'):
        epilogue_chapter = {'number': 15, 'title': 'اپیلوگ', 'scenes': [], 'epilogue': True}
        current_chapter = epilogue_chapter
        current_scene = None
        continue
    m = chapter_re.match(raw)
    if m:
        title = m.group(2).strip().replace(' ★', '')
        title = re.sub(r'\s*\([^)]*فصلِ وحشت[^)]*\)\s*$', '', title).strip()
        current_chapter = {'number': int(m.group(1)), 'title': title, 'scenes': []}
        chapters.append(current_chapter)
        current_scene = None
        continue
    m = scene_re.match(raw)
    if m:
        if current_chapter is None:
            current_chapter = {'number': 1, 'title': 'پیش‌درآمد', 'scenes': [], 'prologue': True}
            chapters.append(current_chapter)
        num = m.group(1).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
        head = m.group(2).strip()
        mm = re.search(r'\[([^\]]+)\]\s*$', head)
        tag = mm.group(1) if mm else ''
        place = re.sub(r'\s*\[[^\]]+\]\s*$', '', head)
        sid = 'N' + (num.zfill(2) if num.isdigit() else num[:-1].zfill(2) + 'b')
        title = place + (f' ({tag})' if tag else '')
        current_scene = {'id': sid, 'title': title, 'context': '', 'lines': [], 'intro': ''}
        current_chapter['scenes'].append(current_scene)
        continue
    if raw.startswith('## '):
        current_scene = None
        continue
    if current_scene is not None:
        s = raw.strip()
        if not s or s.startswith('---') or s.startswith('**باس') or s.startswith('**سکانس') or s.startswith('**عملیات') or s.startswith('**بخش') or s.startswith('**درگیری') or s.startswith('**بزرگ‌ترین') or s.startswith('- '):
            continue
        m = line_re.match(s)
        if m:
            current_scene['lines'].append({'speaker': clean_speaker(m.group(1)), 'text': m.group(2).strip()})
        elif not current_scene['intro']:
            current_scene['intro'] = s


def finalize_scenes(ch):
    kept = []
    for sc in ch['scenes']:
        if not sc['lines']:
            continue
        first = re.split(r'(?<=[.؟!])\s+', re.sub(r'[*_]', '', sc.pop('intro', '')))[0][:240]
        sc['context'] = first or sc['title']
        sc['source'] = {
            'docId': 'SCREENPLAY_V11_FA',
            'section': f'فصل {ch["number"]} — {ch["title"]} / {sc["id"]} — {sc["title"]}',
        }
        kept.append(sc)
    ch['scenes'] = kept
    return kept


scenes_out = []
prologs = [c for c in chapters if c.get('prologue')]
main_chapters = [c for c in chapters if not c.get('prologue')]

for pc in prologs:
    kept = finalize_scenes(pc)
    if main_chapters:
        main_chapters[0]['scenes'] = kept + main_chapters[0]['scenes']
    scenes_out.extend(kept)

for ch in main_chapters:
    kept = finalize_scenes(ch)
    scenes_out.extend(kept)

if epilogue_chapter:
    kept = finalize_scenes(epilogue_chapter)
    if main_chapters:
        main_chapters[-1]['scenes'].extend(kept)
    scenes_out.extend(kept)

assert len(main_chapters) == 15, f'Expected 15 chapters, got {len(main_chapters)}'
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
n_lines = sum(len(s['lines']) for s in scenes_out)

# Keep archive recordings from v7 reference cleanly
bodies = {}
for m in re.finditer(r'^### (T0\d) — .*?\n\n(\*\*مشخصات ثبت:\*\* .+?)(?=^### |^## |\Z)', recordings_doc, flags=re.M | re.S):
    bodies[m.group(1)] = m.group(2).strip()
recs = old.get('recordings', [])
for r in recs:
    if r['id'] in bodies:
        r['markdown'] = bodies[r['id']]

out = {
    'chapters': main_chapters,
    'recordings': recs,
    'note': (
        f'این بخش گفت‌وگوهای مستقیمِ فیلم‌نامهٔ نسخهٔ ۱۱ (بازطراحیِ AAA) را در ۱۵ فصل گردآوری می‌کند: '
        f'{fa(n_lines)} خط دیالوگِ زنده در {fa(len(scenes_out))} صحنه. '
        'پیش‌درآمد در ابتدای فصل ۱ و اپیلوگ در انتهای فصل ۱۵ آمده است. '
        'خواندن فصل‌های میانی و پایانی، رازها و پایان داستان را افشا می‌کند.'
    ),
}
(CONTENT / 'dialogues.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'dialogues.json (v11): chapters={len(main_chapters)} scenes={len(scenes_out)} lines={n_lines}')
