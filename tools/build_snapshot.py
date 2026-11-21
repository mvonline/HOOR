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
    'SCREENPLAY_FILM_FA': ('../v10-bible/SCREENPLAY_FILM_FA.md', 'داستان', True),
    'CHARACTER_BIBLE_FA': ('../v10-bible/CHARACTER_BIBLE_FA.md', 'داستان', True),
    'GAMEPLAY_DESIGN_FA': ('../v10-bible/GAMEPLAY_DESIGN_FA.md', 'بازی‌سازی', False),
    'STORY_BIBLE_FA': ('../v10-bible/STORY_BIBLE_FA.md', 'داستان', True),
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
     'کار فنی را خوب انجام می\u200cدهد و خبر بد را نگه می\u200cدارد. چیزی از دو سال پیش با اوست که هیچ\u200cکس دیگر به یاد ندارد؛ بقیهٔ حسابِ آن شب هنوز در جیبش است.'),
    ('سارا', 35, 'پژوهشگر اندازه‌گیری و مسئول ایمنی', ['sara-v1'],
     'هر چیز را می\u200cنویسد؛ دفترهایش ضدِ فراموشی\u200cاند. دقیق است و گاهی سرد. می\u200cداند چه چیزی ثابت\u200cشدنی است و چه چیزی فقط باید باور شود.'),
    ('کامران', 45, 'مدیر عملیات', [],
     'همه را به اسم صدا می\u200cزند و استکان چای می\u200cدهد. پیش\u200cتر به کارکنان کمک واقعی کرده، برای همین به او اعتماد می\u200cکنند. آرام حرف می\u200cزند و هیچ\u200cوقت صدایش را بالا نمی\u200cبرد.'),
    ('کیان', 24, 'صدا و ثبت', ['kian-v2', 'kian-v1'],
     'شیفتهٔ شنیدن و نگه\u200cداشتنِ صداست. ضبط\u200cهایش فراموش نمی\u200cشوند. گاهی ثبت\u200cکردن را جای فرستادن فوریِ پیام می\u200cگذارد.'),
    ('بهرام', 62, 'پژوهشگر مواد و لایه‌ها', ['bahram-62-v1'],
     'هر روز اسم\u200cها را در دفترش می\u200cنویسد. تجربهٔ میدانی دارد و حدِ دانش خودش را هم باید بپذیرد.'),
    ('رستم', 48, 'مسئول تدارکات', ['rostam-v2', 'rostam-v1'],
     'می\u200cترسد که همه\u200cچیز فرو بریزد؛ برای همین گاهی چیزی را حذف می\u200cکند. بزدل است، ولی وقتی افتاد، می\u200cگوید «من بودم».'),
    ('ماهرخ', 58, 'آشپزِ کمپ', [],
     'کامران را از جوانی می\u200cشناسد و تنها کسی است که او را «پسر» صدا می\u200cزند. غذا می\u200cپزد، کفگیر را وسطِ جمله می\u200cزند، و زیادی می\u200cداند.'),
    ('آرش', 19, 'شاگردِ دانیال', [],
     'همان سؤالی را می\u200cپرسد که دانیال نپرسید. دفترچهٔ کوچکی دارد و گاهی از سرِ شور خطر می\u200cکند.'),
    ('پروانه', 44, 'پرستارِ درمانگاه', [],
     'وقتی برق می\u200cرود با دست پمپ می\u200cکند. اسمِ بیماران را تکرار می\u200cکند: «اگه یادتون رفت، دوباره می\u200cگم.»'),
    ('اسماعیل', 39, 'نگهبانِ مرزِ شمالی', [],
     'نگهبانِ شمال. وفادار، تا روزی که امضاهایش دیگر خوانا نیستند.'),
    ('ایرج', 70, 'راننده‌ی پیرِ کامیون', [],
     'راننده\u200cی پیر و لافزن؛ حافظهٔ جاده\u200cها. شب\u200cهای کمپ حرف می\u200cزند تا سکوت نماند.'),
    ('حسین', 35, 'کارگرِ بلوکِ جرثقیل', [],
     'کارگرِ بلوک؛ پسرِ بیمار دارد. لیوانِ خالی کنارش مالِ کسی است که دیگر نیست.'),
    ('مهدی', 41, 'تکنسین و سیم‌کش', [],
     'تکنسین و سیم\u200cکش؛ گاهی دزدی هم می\u200cکند. سیمی که می\u200cکشد برای کارِ دیگری هم استفاده می\u200cشود.'),
    ('قاسم', 65, 'میرابِ نوبتی', [],
     'میرابِ نوبتی؛ آب را با پنگانِ مسی می\u200cسنجد. «نوبتِ آب، نوبتِ آبه.»'),
    ('فرهاد', 60, 'رادیو و رصدِ شب', [],
     'یکی از نگهبانانِ بی\u200cنام؛ رسیدی در جیب دارد که مالِ کسی است که نمی\u200cشناسد.'),
    ('مینا', 32, 'پایشگر و نگهدار آبشخورها', [],
     'بی\u200cرحم ولی منصف. حسابِ آبشخورها را با لاشهٔ بزها می\u200cکند. دوربینِ تله\u200cای\u200cاش شب\u200cها چیزهایی ثبت کرده که کسی به یاد ندارد.'),
]

QUOTES = {
    'دانیال': 'بستش رو عوض کردم. اگه باز لق شد، مال من نیست؛ مال دنیاست.',
    'سارا': 'تو چیزی رو که نمی‌دونی نمی‌گی. من چیزی رو که می‌دونم نمی‌گم تا مطمئن شم.',
    'کامران': 'من هیچ‌وقت نگفتم کسی بمیره. گفتم کار نخوابه.',
    'کیان': 'این باد صداش زرده. نه، زرد نه؛ کرمیه. ببخشید، عادتِ شغلیه.',
    'بهرام': 'یک سطر دیگه.',
    'رستم': 'این یکی از ساعتِ بارگیری مهم‌تر بود.',
    'مینا': 'اگه امروز عکس خوب گرفتی و فردا آب نرسید، کارِ ما خوب پیش نرفته.',
    'قاسم': 'نوبتِ آب، نوبتِ آبه.',
    'ماهرخ': 'کسی که غذا نخورده، کار نمی‌کنه.',
    'ایرج': 'ماشین رو اگه خوب نگه‌داری، تو رو هم نگه می‌داره.',
    'آرش': 'شما از کِی ساکت شدین؟',
    'پروانه': 'من هیچ‌وقت بیمار رو اندازه نگرفتم.',
    'اسماعیل': 'من فقط می‌خوام بدونم چرا درمانگاه رو قطع کردیم.',
    'مهدی': 'ترس رو بده من؛ من نگهش می‌دارم.',
    'حسین': 'استاد، شما نمی‌ترسین؟',
    'فرهاد': 'ببینین اگه چشم‌هاتون به تاریکی عادت کرد، یه خط غباری هم می‌بینین.',
}
ORDER = ['دانیال', 'سارا', 'کامران', 'کیان', 'بهرام', 'رستم', 'مینا', 'ماهرخ', 'آرش', 'پروانه', 'اسماعیل', 'ایرج', 'حسین', 'مهدی', 'قاسم', 'فرهاد']

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

    screenplay = read(V7 / '../v10-bible/SCREENPLAY_FILM_FA.md')
    headings = re.findall(r'^## فصل (\d+) — (.+)$', screenplay, flags=re.M)
    assert len(headings) == 10, headings
    chapters = [{'number': int(n), 'title': t.strip(), 'minutes': budget['chapter_minutes'][int(n) - 1]} for n, t in headings]

    summaries = []
    chapter_sections = [x for x in re.split(r'^## ', screenplay, flags=re.M) if x.startswith('فصل ')]
    assert len(chapter_sections) == 10, len(chapter_sections)
    for sec in chapter_sections:
        paras = [q.strip() for q in sec.split('\n', 1)[1].split('\n\n') if q.strip() and not q.strip().startswith(('**نما', '---', ':'))]
        text = next((q for q in paras if '«' not in q), paras[0])
        summaries.append(re.sub(r'\s+', ' ', text))

    world = read(V7 / 'WORLD_AND_MISSIONS_FA.md')
    side = []
    for m in re.finditer(r'^### (Q0[1-8]) — (.+?) /.*?\n(.*?)(?=^### Q0|^## |\Z)', world, flags=re.M | re.S):
        side.append({'id': m.group(1), 'title': m.group(2).strip(), 'markdown': m.group(3).strip()})
    assert len(side) == 8, [s['id'] for s in side]

    stems = sorted(p.stem for p in IMAGES.glob('*.png'))
    people = []
    for name, age, role, candidates, text in PEOPLE:
        image = next((c for c in candidates if c in stems and (status.get(c) != 'retired_story_reference' or c in NOT_RETIRED)), None)
        people.append({'name': name, 'age': age, 'role': role, 'image': image, 'text': text, 'quote': QUOTES.get(name, '')})
    people.sort(key=lambda p: ORDER.index(p['name']) if p['name'] in ORDER else 99)

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
