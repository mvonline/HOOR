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

screenplay = (V7 / 'SCREENPLAY_AND_FINAL_SEQUENCE_FA.md').read_text(encoding='utf-8')
recordings_doc = (V7 / 'RECORDINGS_DOCUMENTS_AND_DIRECTION_FA.md').read_text(encoding='utf-8')

old = json.loads((CONTENT / 'dialogues.json').read_text(encoding='utf-8'))
old_scene = {s['id']: s for c in old['chapters'] for s in c['scenes']}

CONTEXT_PATCH = {
    'M01': 'باد بار را روی بلوک حیاط کج کرده و دستِ یک کارگر زیرش مانده است. کامران خودش شانه زیر بار می‌دهد و دانیال باید دست را آزاد کند. رستم جملهٔ آخر را بعد از نجات می‌گوید.',
    'M09': 'در دهانهٔ تنگه، سارا زمان مرجع را بیرون نگه می‌دارد و دانیال آزمایشِ دو ساعت را اجرا می‌کند. پیش از غروب، روی لبهٔ زونِ B یک لرزشِ بی‌ریتم دیده می‌شود: اولین رتیلِ هور.',
    'M39': 'پیش از شروع آتش، دانیال خروجِ بی‌سلاح و توقفِ دست‌کاری را پیشنهاد می‌کند. کامران آرام و سرد جواب می‌دهد و می‌داند کیان و خدمه روی خطِ تیر هستند. کمکِ واقعیِ گذشته با اجبارِ امروز یکی نیست.',
}

# ---- parse screenplay -------------------------------------------------------
chapter_re = re.compile(r'^## فصل (\d+) — (.+)$')
scene_re = re.compile(r'^(?:\*\*(M\d\d)، ([^:*]+):\*\*|### (M\d\d) — (.+))')
line_re = re.compile(r'^([^«»\n:]{1,60}):\s*«(.+)»\s*$')

chapters = []
current_chapter = None
current_scene = None
for raw in screenplay.splitlines():
    m = chapter_re.match(raw)
    if m:
        current_chapter = {'number': int(m.group(1)), 'title': m.group(2).strip(), 'scenes': []}
        chapters.append(current_chapter)
        current_scene = None
        continue
    m = scene_re.match(raw)
    if m and current_chapter is not None:
        sid = m.group(1) or m.group(3)
        title = (m.group(2) or m.group(4)).strip()
        current_scene = {'id': sid, 'title': title, 'context': '', 'lines': []}
        current_chapter['scenes'].append(current_scene)
        continue
    if raw.startswith('## '):
        current_scene = None
        continue
    if current_scene is not None:
        m = line_re.match(raw.strip())
        if m:
            current_scene['lines'].append({'speaker': m.group(1).strip(), 'text': m.group(2).strip()})

scenes_out = []
for ch in chapters:
    kept = []
    for sc in ch['scenes']:
        if not sc['lines']:
            continue
        prev = old_scene.get(sc['id'])
        sc['context'] = CONTEXT_PATCH.get(sc['id']) or (prev['context'] if prev else '')
        if not sc['context']:
            raise SystemExit(f'scene {sc["id"]} has dialogue but no context; add one')
        sc['source'] = {'docId': 'SCREENPLAY_AND_FINAL_SEQUENCE_FA',
                        'section': f'فصل {ch["number"]} — {ch["title"]} / {sc["id"]} — {sc["title"]}'}
        kept.append(sc)
    ch['scenes'] = kept
    scenes_out.extend(kept)

assert len(chapters) == 10, len(chapters)
fa = lambda n: str(n).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
n_lines = sum(len(s['lines']) for s in scenes_out)

# ---- recordings: prepend 'مشخصات ثبت' ---------------------------------------
meta = {}
for m in re.finditer(r'^### (T0\d) — .*?\n\n\*\*مشخصات ثبت:\*\* (.+)$', recordings_doc, flags=re.M):
    meta[m.group(1)] = m.group(2).strip()
recs = old['recordings']
for r in recs:
    stamp = meta.get(r['id'])
    if not stamp:
        raise SystemExit(f'no metadata for {r["id"]}')
    body = r['markdown']
    body = re.sub(r'^\*\*مشخصات ثبت:\*\*.*?\n\n', '', body)
    r['markdown'] = f'**مشخصات ثبت:** {stamp}\n\n{body}'

old['chapters'] = chapters
old['note'] = (
    f'این بخش گفت‌وگوهای مستقیمِ نوشته‌شده در سناریوی نسخهٔ ۷٫۱ را به تفکیک ده فصل گردآوری می‌کند: {fa(n_lines)} خط در {fa(len(scenes_out))} صحنه. '
    'همهٔ چهل مأموریت هنوز متن گفت‌وگوی مستقل ندارند. شش ضبط اختیاری نیز با متن پایهٔ کامل و مشخصاتِ ثبت (زمان، فرستنده و دستگاه)، شامل ۳۷ خط گفتار و توضیح موقعیت، آمده‌اند. '
    'این‌ها متنِ نوشته‌شده‌اند؛ هیچ فایل صوتی یا اجرای بازیگری ضبط نشده است. دیالوگ‌های واکنشیِ سیستمی، شاخه‌های شرطی و ترجمهٔ کامل انگلیسی همچنان کار نگارش و تولید آینده‌اند. '
    'خلاصهٔ غیرمستقیمِ حرفِ شخصیت به دیالوگ تازه تبدیل نشده است. خواندن این بخش، پیشروی و پایان داستان را افشا می‌کند.'
)
(CONTENT / 'dialogues.json').write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'dialogues.json: chapters={len(chapters)} scenes={len(scenes_out)} lines={n_lines}')
