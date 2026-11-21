#!/usr/bin/env python3
"""Build the plaintext content snapshot that sites/hoor-github-pages-*/scripts/encrypt-content.mjs encrypts.

Reads the v7 package (gameStory/redesign/v7-20261121) and gameStory/images and writes
sites/hoor-github-pages-20261121/.snapshot/portal-data.json  (git-ignored: it holds the whole story in plain text).

Needs: Python 3.10+, Pillow.  Usage:  python3 tools/build_snapshot.py [--max-mb 28]
"""
import argparse
import base64
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
V7 = ROOT / 'gameStory/redesign/v7-20261121'
IMAGES = ROOT / 'gameStory/images'
SITE = ROOT / 'sites/hoor-github-pages-20261121'
OUT = SITE / '.snapshot/portal-data.json'

# id -> (file relative to V7, category, spoiler)
DOCS = {
    'READER_GUIDE_FA': ('README.md', 'شروع مطالعه', False),
    'VISION_AND_CAMPAIGN_FA': ('VISION_AND_CAMPAIGN_FA.md', 'طرح کلی', False),
    'SCREENPLAY_AND_FINAL_SEQUENCE_FA': ('SCREENPLAY_AND_FINAL_SEQUENCE_FA.md', 'داستان', True),
    'CHARACTERS_AND_DRAMA_FA': ('CHARACTERS_AND_DRAMA_FA.md', 'داستان', False),
    'WORLD_AND_MISSIONS_FA': ('WORLD_AND_MISSIONS_FA.md', 'جهان و مأموریت‌ها', False),
    'GAMEPLAY_SYSTEMS_FA': ('GAMEPLAY_SYSTEMS_FA.md', 'بازی‌سازی', False),
    'ACTION_ENCOUNTER_ATLAS_FA': ('ACTION_ENCOUNTER_ATLAS_FA.md', 'بازی‌سازی', False),
    'ONBOARDING_AND_LEARNING_FA': ('ONBOARDING_AND_LEARNING_FA.md', 'بازی‌سازی', False),
    'WEAPONS_VEHICLES_AND_EQUIPMENT_FA': ('WEAPONS_VEHICLES_AND_EQUIPMENT_FA.md', 'بازی‌سازی', False),
    'RESOURCES_TRADE_SURVIVAL_AND_WATER_SUPPLY_FA': ('RESOURCES_TRADE_SURVIVAL_AND_WATER_SUPPLY_FA.md', 'بازی‌سازی', False),
    'SCIENCE_SKY_AND_THERMAL_RULES_FA': ('SCIENCE_SKY_AND_THERMAL_RULES_FA.md', 'علم و طبیعت', False),
    'NIGHT_SKY_NAVIGATION_AND_EASTER_EGGS_FA': ('NIGHT_SKY_NAVIGATION_AND_EASTER_EGGS_FA.md', 'علم و طبیعت', False),
    'ECOLOGY_WATERHOLES_AND_PHOTOGRAPHY_FA': ('ECOLOGY_WATERHOLES_AND_PHOTOGRAPHY_FA.md', 'علم و طبیعت', False),
    'RECORDINGS_DOCUMENTS_AND_DIRECTION_FA': ('RECORDINGS_DOCUMENTS_AND_DIRECTION_FA.md', 'داستان', True),
    'GEOGRAPHY_EVIDENCE_FA': ('GEOGRAPHY_EVIDENCE_FA.md', 'نقشه و جغرافیا', False),
    'maps-README_FA': ('maps/README_FA.md', 'نقشه و جغرافیا', False),
    'CONTINUITY_AND_STORY_REVIEW_FA': ('CONTINUITY_AND_STORY_REVIEW_FA.md', 'بازبینی', True),
    'DESIGN_REVIEW_FA': ('DESIGN_REVIEW_FA.md', 'بازبینی', False),
}

# These creatures are back in v7.1 (retil family: juvenile + adult); only the giant stays retired.
NOT_RETIRED = {'hoor-adult-v1', 'hoor-adult-v2', 'hoor-juvenile-v1', 'hoor-juvenile-v2'}

PEOPLE = [  # (name, age, role, image candidates, text)
    ('دانیال', 38, 'مکانیک و راننده؛ شخصیت بازیکن', ['daniyal-v1'],
     'کار فنی را خوب انجام می‌دهد، اما خبر بد را گاهی تا مطمئن‌شدن نگه می‌دارد. هشدار یک گزارش را دیده و کامل نگفته است؛ نجات‌دادن دیگران مسئولیت این سکوت را پاک نمی‌کند.'),
    ('سارا', 35, 'پژوهشگر اندازه‌گیری و مسئول ایمنی', ['sara-v1'],
     'باید میان بررسی بیشتر و اقدام به‌موقع تصمیم بگیرد. همکار دانیال است، نه کسی که فقط باید نجاتش داد. در آزمایش، مسیر و پایان کارِ مستقل دارد.'),
    ('کامران', 45, 'مدیر عملیات', [],
     'پیش‌تر به کارکنان کمک واقعی کرده و دانیال دلیل قابل‌فهمی برای اعتماد به او دارد. مشکل از جایی شروع می‌شود که حفظ پروژه را مهم‌تر از اختیار و امنیت دیگران می‌داند. آرام حرف می‌زند و کم‌کم بی‌رحم‌تر می‌شود.'),
    ('کیان', 24, 'صدا و ثبت', ['kian-v2', 'kian-v1'],
     'شیفتهٔ شنیدن محیط است و گاهی ثبت‌کردن را جای فرستادن فوریِ پیام می‌گذارد. وقتی خطر روشن می‌شود، داده را روی دو حامل می‌گذارد و دیگران را پناه می‌دهد.'),
    ('بهرام', 62, 'پژوهشگر مواد و لایه‌ها', ['bahram-62-v1'],
     'تجربهٔ میدانی دارد و حدِ دانش خودش را هم باید بپذیرد. سه روز را در یک ایستگاه خدماتی با جیره و دفتر مصرف گذرانده است.'),
    ('رستم', 48, 'مسئول تدارکات', ['rostam-v2', 'rostam-v1'],
     'کمک واقعی کرده و در عین حال بخشی از هشدار را حذف کرده است. ترس از قطع حقوق انتخابش را قابل‌فهم می‌کند، ولی مسئولیتش را کم نمی‌کند.'),
    ('مینا', 32, 'پایشگر و نگهدار آبشخورها', [],
     'دفتر مصرف و گزارش مشاهده را نگه می‌دارد. دامپزشک یا راهنمای همه‌چیزدان نیست؛ برایش آبِ فردا مهم‌تر از عکسِ زیبای امشب است.'),
]

COPY = {
    'heroTitle': 'ردِ هور — خطِ سایه',
    'heroText': 'یک مکانیک و یک پژوهشگر برای نجاتِ همکارانشان وارد تنگه‌ای در حاشیهٔ لوت می‌شوند و کم‌کم می‌فهمند چه کسی ساعتِ دیگران را به ابزارِ کنترل تبدیل کرده است.',
    'storyLead': 'اول آدم‌ها را بشناسید: کی چه خواسته، کی چه نگفته و هر کس برای کدام کار پاسخ‌گوست. راز دستگاه بعد از این‌ها می‌آید.',
    'mapLead': 'منطقهٔ شهداد و تنگ رتیل واقعی‌اند؛ تأسیسات و آبشخورهای داستان ساختگی‌اند و جای واقعیِ ثابت ندارند. این سه نما سه پرسشِ جدا را جواب می‌دهند.',
    'mapTitles': ['نقشهٔ منطقه: شهداد تا تنگ', 'نمای ماهواره‌ای محدودهٔ تنگ', 'اتصالِ ناحیه‌های بازی'],
    'mapTexts': [
        'جای واقعیِ آبادی‌ها و راه‌های اصلی. فاصلهٔ مستقیمِ شهداد تا تنگ حدود ۹۸٫۸ کیلومتر است؛ ۱۳۰ کیلومتر برآوردِ مسیرِ گزارشِ پیمایش است و تأیید نشده.',
        'تصویر ماهواره‌ایِ مرجع. هیچ مسیرِ حدسیِ درون تنگه کشیده نشده و هندسهٔ دقیقِ تنگه هنوز برداشت نشده است.',
        'نمودارِ بدونِ مقیاس که نشان می‌دهد از کدام ناحیه به کدام ناحیه می‌شود رفت. جغرافیای واقعی نیست.',
    ],
}


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8-sig')


def first_h1(md: str, fallback: str) -> str:
    m = re.search(r'^#\s+(.+)$', md, flags=re.M)
    return m.group(1).strip() if m else fallback


def first_paragraph(md: str) -> str:
    for block in re.split(r'\n\s*\n', md):
        block = block.strip()
        if block and not block.startswith(('#', '|', '```', '>', '-', '!', '[')):
            return re.sub(r'\s+', ' ', re.sub(r'[*_`]', '', block))[:280]
    return ''


def b64_image(path: Path, max_edge: int, quality: int) -> dict:
    img = Image.open(path)
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
    img.thumbnail((max_edge, max_edge), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'WEBP', quality=quality, method=6)
    return {'type': 'image/webp', 'data': base64.b64encode(buf.getvalue()).decode('ascii')}


def humanize(stem: str) -> str:
    return re.sub(r'-v\d+$', '', stem).replace('-', ' ')


def category_of(stem: str) -> str:
    if stem.startswith('env-') or stem in ('canyon-day-v1', 'caravanserai-night-v1'):
        return 'محیط'
    if stem.startswith(('pirmard', 'vehicle', 'camel-pack')):
        return 'وسیله'
    if stem.startswith(('hoor-', 'dara-')):
        return 'جانور و هور'
    return 'شخصیت'


def build(max_mb: float) -> dict:
    budget = json.loads(read(V7 / 'content-budget.json'))
    index = json.loads(read(IMAGES / 'image-index.json'))
    status = {Path(a['filename']).stem: a['status'] for a in index['assets']}
    manifest = json.loads(read(IMAGES / 'completion-manifest.json'))
    titles = {Path(a['filename']).stem: a['title'] for a in manifest['assets']}

    docs = []
    for doc_id, (rel, category, spoiler) in DOCS.items():
        md = read(V7 / rel)
        docs.append({'id': doc_id, 'file': rel, 'title': first_h1(md, doc_id), 'category': category,
                     'description': first_paragraph(md), 'markdown': md, 'legacy': False, 'spoiler': spoiler,
                     'words': len(md.split())})

    screenplay = read(V7 / 'SCREENPLAY_AND_FINAL_SEQUENCE_FA.md')
    headings = re.findall(r'^## فصل (\d+) — (.+)$', screenplay, flags=re.M)
    assert len(headings) == 10, headings
    chapters = [{'number': int(n), 'title': t.strip(), 'minutes': budget['chapter_minutes'][int(n) - 1]} for n, t in headings]

    reader = json.loads(read(SITE / 'content/reader-edition.json'))
    story = reader['SCREENPLAY_AND_FINAL_SEQUENCE_FA']['markdown']
    summaries = []
    chapter_sections = [s for s in re.split(r'^## ', story, flags=re.M) if s.startswith('فصل ')]
    assert len(chapter_sections) == 10, len(chapter_sections)
    for sec in chapter_sections:
        body = sec.split('\n', 1)[1].strip()
        summaries.append(re.sub(r'\s+', ' ', body.split('\n\n')[0]))

    world = read(V7 / 'WORLD_AND_MISSIONS_FA.md')
    side = []
    for m in re.finditer(r'^### (Q0[1-8]) — (.+?) /.*?\n(.*?)(?=^### Q0|^## |\Z)', world, flags=re.M | re.S):
        side.append({'id': m.group(1), 'title': m.group(2).strip(), 'markdown': m.group(3).strip()})
    assert len(side) == 8, [s['id'] for s in side]

    stems = sorted(p.stem for p in IMAGES.glob('*.png'))
    people = []
    for name, age, role, candidates, text in PEOPLE:
        image = next((c for c in candidates if c in stems and (status.get(c) != 'retired_story_reference' or c in NOT_RETIRED)), None)
        people.append({'name': name, 'age': age, 'role': role, 'image': image, 'text': text})

    # images: shrink until the plaintext fits the budget
    max_edge, quality = 1280, 76
    while True:
        media, gallery = {}, []
        for stem in stems:
            retired = status.get(stem) == 'retired_story_reference' and stem not in NOT_RETIRED
            gallery.append({'id': stem, 'title': titles.get(stem) or humanize(stem), 'filename': f'{stem}.png',
                            'category': category_of(stem),
                            'caption': 'ایدهٔ کنارگذاشته‌شده؛ مرجعِ داستانِ فعلی نیست.' if retired else 'مرجعِ تصویری برای تصور فضا؛ طرحِ نهاییِ بازی نیست.',
                            'retired': retired})
            media[stem] = b64_image(IMAGES / f'{stem}.png', max_edge, quality)
        for name in ('region-map', 'canyon-map', 'design-map'):
            media[name] = b64_image(V7 / 'maps' / f'{name}.png', 1600 if name != 'design-map' else 1200, 80)
        snapshot = {
            'library': {'docs': docs, 'gallery': gallery, 'budget': budget, 'chapters': chapters, 'sideStories': side,
                        'people': people, 'chapterSummaries': summaries, 'copy': COPY},
            'media': media,
            'mapHtml': read(V7 / 'maps/map.html'),
        }
        size = len(json.dumps(snapshot, ensure_ascii=False).encode('utf-8'))
        print(f'images {max_edge}px q{quality}: {size / 1048576:.1f} MB')
        if size <= max_mb * 1048576:
            return snapshot
        if quality > 52:
            quality -= 8
        elif max_edge > 800:
            max_edge -= 160
        else:
            sys.exit('snapshot cannot fit the size budget; drop images or raise --max-mb')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-mb', type=float, default=28.0, help='plaintext size cap (encrypt step allows 32 MB)')
    args = ap.parse_args()
    snapshot = build(args.max_mb)
    # the same checks the browser (transport.ts validateContent) and the encrypt step will run
    lib, media = snapshot['library'], snapshot['media']
    assert lib['docs'] and lib['gallery'] and all(g['id'] in media for g in lib['gallery'])
    assert 'https://esm.sh/d3-geo@3.1.1' in snapshot['mapHtml'], 'map.html no longer imports d3-geo from esm.sh; transport.mapUrl() rewrite would not apply'
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snapshot, ensure_ascii=False), encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)}: docs={len(lib["docs"])} gallery={len(lib["gallery"])} '
          f'chapters={len(lib["chapters"])} side={len(lib["sideStories"])} people={len(lib["people"])}')


if __name__ == '__main__':
    main()
