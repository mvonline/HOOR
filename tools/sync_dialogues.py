"""Rebuild sites/hoor-github-pages-*/content/dialogues.json from the v7 screenplay and recordings.

Spoken lines come from SCREENPLAY (`speaker: «text»`), recording stamps from RECORDINGS.
Scene contexts are kept from the existing JSON (CONTEXT_PATCH overrides); a new scene with dialogue needs a context.
reader-edition.json is edited by hand. Run: python3 -I tools/sync_dialogues.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V7 = ROOT / 'gameStory/redesign/v7-20261121'
CONTENT = ROOT / 'sites/hoor-github-pages-20261121/content'

V10 = ROOT / 'gameStory/redesign/v10-bible'
screenplay = (V10 / 'SCREENPLAY_FILM_FA.md').read_text(encoding='utf-8')
recordings_doc = (V7 / 'RECORDINGS_DOCUMENTS_AND_DIRECTION_FA.md').read_text(encoding='utf-8')

old = json.loads((CONTENT / 'dialogues.json').read_text(encoding='utf-8'))
old_scene = {s['id']: s for c in old['chapters'] for s in c['scenes']}

CONTEXT_PATCH = {
    'M01': 'باد بار را روی بلوک حیاط کج کرده و دستِ یک کارگر زیرش مانده است. کامران خودش شانه زیر بار می‌دهد و دانیال باید دست را آزاد کند. رستم جملهٔ آخر را بعد از نجات می‌گوید.',
    'M09': 'در دهانهٔ تنگه، سارا زمان مرجع را بیرون نگه می‌دارد و دانیال آزمایشِ دو ساعت را اجرا می‌کند. پیش از غروب، روی لبهٔ زونِ B یک لرزشِ بی‌ریتم دیده می‌شود: اولین رتیلِ هور.',
    'M39': 'پیش از شروع آتش، دانیال خروجِ بی‌سلاح و توقفِ دست‌کاری را پیشنهاد می‌کند. کامران آرام و سرد جواب می‌دهد و می‌داند کیان و خدمه روی خطِ تیر هستند. کمکِ واقعیِ گذشته با اجبارِ امروز یکی نیست.',
}

CAST = {'دانیال','سارا','کامران','کیان','بهرام','رستم','مینا','ماهرخ','آرش','پروانه','اسماعیل','مهدی','فرهاد','نادر','رویا','یونس','حسین','قاسم','حیدر','سعید','مریم','ناهید','سهراب','لیلا'}

def clean_speaker(raw):
    sp = re.split(r'[،(]', raw)[0].strip()
    if sp.startswith('دستگاهِ ضبط'):
        return 'برچسب روی دستگاه'
    if sp.split()[0] in CAST:
        return sp.split()[0]
    if len(sp) > 20 or '.' in sp:
        sp = sp.split()[0].rstrip('ِ')
    return sp

# ---- parse screenplay -------------------------------------------------------
chapter_re = re.compile(r'^## فصل (\d+) — (.+)$')
scene_re = re.compile(r'^\*\*نما ([\d۰-۹]+) — ([^*]+?)\*\*\s*$')
line_re = re.compile(r'^([^«»\n:]{1,60}):\s*«(.+)»\s*$')

chapters = []
current_chapter = None
current_scene = None
for raw in screenplay.splitlines():
    if raw.startswith('## پیش‌درآمد'):
        current_chapter = {'number': 1, 'title': 'پیش‌درآمد', 'scenes': [], 'prologue': True}
        chapters.append(current_chapter)
        current_scene = None
        continue
    m = chapter_re.match(raw)
    if m:
        current_chapter = {'number': int(m.group(1)), 'title': m.group(2).strip(), 'scenes': []}
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
        sid = 'N' + num.zfill(2)
        title = place + (f' ({tag})' if tag else '')
        current_scene = {'id': sid, 'title': title, 'context': '', 'lines': [], 'intro': ''}
        current_chapter['scenes'].append(current_scene)
        continue
    if raw.startswith('## '):
        current_scene = None
        continue
    if current_scene is not None:
        if not current_scene['intro'] and raw.strip() and not line_re.match(raw.strip()):
            current_scene['intro'] = raw.strip()
        m = line_re.match(raw.strip())
        if m:
            current_scene['lines'].append({'speaker': clean_speaker(m.group(1)), 'text': m.group(2).strip()})

scenes_out = []
for ch in chapters:
    kept = []
    for sc in ch['scenes']:
        if not sc['lines']:
            continue
        prev = old_scene.get(sc['id'])
        first = re.split(r'(?<=[.؟!])\s+', re.sub(r'[*_]', '', sc.pop('intro', '')))[0][:220]
        sc['context'] = CONTEXT_PATCH.get(sc['id']) or first or (prev['context'] if prev else '')
        if not sc['context']:
            raise SystemExit(f'scene {sc["id"]} has dialogue but no context; add one')
        sc['source'] = {'docId': 'SCREENPLAY_FILM_FA',
                        'section': f'فصل {ch["number"]} — {ch["title"]} / {sc["id"]} — {sc["title"]}'}
        kept.append(sc)
    ch['scenes'] = kept
    scenes_out.extend(kept)

prolog = [c for c in chapters if c.get('prologue')]
chapters = [c for c in chapters if not c.get('prologue')]
for pc in prolog:
    chapters[0]['scenes'] = pc['scenes'] + chapters[0]['scenes'] if chapters else pc['scenes']
assert len(chapters) == 10, len(chapters)
fa = lambda n: str(n).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
n_lines = sum(len(s['lines']) for s in scenes_out)

# ---- recordings: prepend 'مشخصات ثبت' ---------------------------------------
bodies = {}
for m in re.finditer(r'^### (T0\d) — .*?\n\n(\*\*مشخصات ثبت:\*\* .+?)(?=^### |^## |\Z)', recordings_doc, flags=re.M | re.S):
    bodies[m.group(1)] = m.group(2).strip()
recs = old['recordings']
for r in recs:
    if r['id'] not in bodies:
        raise SystemExit(f'no recording body for {r["id"]}')
    r['markdown'] = bodies[r['id']]

old['chapters'] = chapters
old['note'] = (
    f'این بخش گفت‌وگوهای مستقیمِ فیلم‌نامهٔ نسخهٔ ۱۰ را به تفکیک ده فصل گردآوری می‌کند: {fa(n_lines)} خط در {fa(len(scenes_out))} صحنه. '
    'پیش‌درآمد در فصل یک آمده است. شش ضبط اختیاری نیز با متن پایه و مشخصاتِ ثبت آمده‌اند؛ این‌ها متنِ نوشته‌شده‌اند و هیچ فایل صوتی یا اجرای بازیگری ضبط نشده است. '
    'دیالوگ‌های واکنشیِ بازی و شاخه‌های شرطی هنوز نوشته نشده‌اند. خواندن این بخش، پیشروی و پایان داستان را افشا می‌کند.'
)
(CONTENT / 'dialogues.json').write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'dialogues.json: chapters={len(chapters)} scenes={len(scenes_out)} lines={n_lines}')
