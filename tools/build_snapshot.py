#!/usr/bin/env python3
"""Build the plaintext content snapshot that sites/hoor-github-pages-*/scripts/encrypt-content.mjs encrypts.

Canon source: gameStory/redesign/v11-aaa (with maps/geography reference from v7-20261121 and images from gameStory/images).
Writes sites/hoor-github-pages-20261121/.snapshot/portal-data.json (git-ignored).

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
V11 = ROOT / 'gameStory/redesign/v11-aaa'
IMAGES = ROOT / 'gameStory/images'
SITE = ROOT / 'sites/hoor-github-pages-20261121'
OUT = SITE / '.snapshot/portal-data.json'

# id -> (path relative to ROOT, category, spoiler, legacy)
DOCS = {
    'READER_GUIDE_FA': ('gameStory/redesign/v11-aaa/README.md', 'شروع مطالعه', False, False),
    'SCREENPLAY_V11_FA': ('gameStory/redesign/v11-aaa/SCREENPLAY_V11_FA.md', 'داستان', True, False),
    '01_STORY_WORLD_AND_CAMPAIGN_FA': ('gameStory/redesign/v11-aaa/01_STORY_WORLD_AND_CAMPAIGN_FA.md', 'داستان', True, False),
    '02_CHARACTERS_AND_DIALOGUE_CRAFT_FA': ('gameStory/redesign/v11-aaa/02_CHARACTERS_AND_DIALOGUE_CRAFT_FA.md', 'داستان', False, False),
    '03_COMBAT_ENEMIES_BOSSES_AND_VEHICLES_FA': ('gameStory/redesign/v11-aaa/03_COMBAT_ENEMIES_BOSSES_AND_VEHICLES_FA.md', 'بازی‌سازی', False, False),
    '04_OPEN_WORLD_SYSTEMS_AND_VISUAL_BIBLE_FA': ('gameStory/redesign/v11-aaa/04_OPEN_WORLD_SYSTEMS_AND_VISUAL_BIBLE_FA.md', 'جهان و مأموریت‌ها', False, False),
    'GEOGRAPHY_EVIDENCE_FA': ('gameStory/redesign/v7-20261121/GEOGRAPHY_EVIDENCE_FA.md', 'نقشه و جغرافیا', False, False),
    'maps-README_FA': ('gameStory/redesign/v7-20261121/maps/README_FA.md', 'نقشه و جغرافیا', False, False),
    'ECOLOGY_WATERHOLES_AND_PHOTOGRAPHY_FA': ('gameStory/redesign/v7-20261121/ECOLOGY_WATERHOLES_AND_PHOTOGRAPHY_FA.md', 'علم و طبیعت', False, False),
    'NIGHT_SKY_NAVIGATION_AND_EASTER_EGGS_FA': ('gameStory/redesign/v7-20261121/NIGHT_SKY_NAVIGATION_AND_EASTER_EGGS_FA.md', 'علم و طبیعت', False, False),
    'RECORDINGS_DOCUMENTS_AND_DIRECTION_FA': ('gameStory/redesign/v7-20261121/RECORDINGS_DOCUMENTS_AND_DIRECTION_FA.md', 'آرشیو نسخه‌های قبل', True, True),
    'SCREENPLAY_FILM_FA': ('gameStory/redesign/v10-bible/SCREENPLAY_FILM_FA.md', 'آرشیو نسخه‌های قبل', True, True),
}

NOT_RETIRED = {'hoor-adult-v1', 'hoor-adult-v2', 'hoor-juvenile-v1', 'hoor-juvenile-v2', 'v11-action-kalut-convoy-v1'}

PEOPLE = [  # (name, age, role, image candidates, text)
    ('دانیال', 38, 'راننده-مکانیکِ کاروان‌های سنگین؛ شخصیتِ بازیکن', ['daniyal-v1'],
     'مردی کارکشته و سخت‌جان که هم پشتِ فرمانِ «پیرمرد»، SUV، موتور، چهارچرخ و شتر استاده و هم در نبردِ گرم و سرد کم نمی‌آورد. دو سال است با بارِ گناه تصادفی در شهداد و پاکتِ بازنشدهٔ «بقیهٔ حساب» زندگی می‌کند.'),
    ('سارا', 35, 'بازرسِ ارشدِ زمین‌شناسی و تحلیلگرِ میدانی', ['sara-v1'],
     'تیز، بی‌تعارف و عمل‌گرا؛ خاکِ معادنِ کرمان و یزد را خورده. با کارابین، دوربینِ حرارتی و دفترِ ضدِ فراموشی شانه به شانهٔ دانیال می‌جنگد تا حقیقتِ رگهٔ هور را بیرون بکشد.'),
    ('کامران', 46, 'مدیرِ عملیاتِ «سپهرِ لوت»؛ بارونِ تجارتِ فراموشی', [],
     'خوش‌پوش، مودب و چای‌ریز با حافظه‌ای ترسناک. زیرِ پوششِ نیروگاهِ خورشیدی و معدنِ لیتیوم، کارتلِ «ناپدیدسازیِ بدونِ جنازه» را می‌چرخاند و تا آخرین نفس خونسرد و خطرناک می‌ماند.'),
    ('مهدی', 42, 'برق‌کارِ ارشد، دزدِ سابق و مهندسِ ابزارِ کمپ', [],
     'شوخ‌ترین و رک‌ترین رفیقِ دانیال. پهپادِ شناسایی، دید در شب، دوربینِ حرارتی و تله‌های انفجاریِ گروه را می‌سازد و برای دزدیدنِ دفترِ مشتریانِ کامران جانش را وسط می‌گذارد.'),
    ('نادر', 52, 'بازماندهٔ فاجعهٔ هفت سال پیش و تک‌تیراندازِ ردیاب', [],
     'تنها بازماندهٔ شیفتِ شبِ شش کارگرِ گمشده در گسل. پایش لنگ است اما هنوز بهترین تک‌تیرانداز و ردیابِ لوت است و تا پایِ جان دنبالِ حقیقتِ حیدر و پنج رفیقش می‌رود.'),
    ('کیان', 25, 'صدابردار، خلبانِ پهپاد و آرشیودارِ زیرزمینی', ['kian-v2', 'kian-v1'],
     'جوانِ پرانرژی و تیزهوشی که پهپادِ شناسایی را به منطقه آورده. پس از گیر افتادن در اتاقکِ آهنیِ اعماق، از طریقِ رادیو امید و طنزِ زندهٔ گروه می‌ماند تا نجاتِ بزرگش در فصل ۱۲.'),
    ('مینا', 33, 'محیط‌بانِ مستقل، موتورسوار و متخصصِ حیات‌وحش', [],
     'زنِ سرسخت و بومیِ لوت؛ سوار بر موتورِ تریلِ برقی با دوربینِ تله‌ای و تفنگِ شکاری. مربیِ شکار، ردیابی و نگهبانِ آبشخورهایی است که کامران آبشان را دزدیده.'),
    ('آرش', 20, 'شاگردِ مکانیک و رانندهٔ بی‌پروای موتور و چهارچرخ', [],
     'انرژیِ بی‌پروای کمپ؛ عاشقِ سرعت، پرش از کلوت با موتورِ تریل و تیونینگِ چهارچرخ. دانیال الگوی اوست و افشای رازِ دانیال، بزرگ‌ترین آزمونِ بلوغِ او می‌شود.'),
    ('رویا', 40, 'گردانندهٔ کاروانسرا و ملکهٔ بازارِ سیاهِ لوت', ['roya-v2', 'roya-v1'],
     'دلالِ تیز و بی‌تعارفِ سلاح‌های گرم و سرد، قطعاتِ خودرو و قراردادهای حمله به کاروان‌ها. فقط پول و اعتبار می‌شناسد — تا شبی که کامران کاروانسرایش را به آتش می‌کشد.'),
    ('اسماعیل', 39, 'فرماندهٔ گشتِ شمالیِ کامران (چهرهٔ تراژیکِ دشمن)', [],
     'در نیمهٔ اول فرماندهٔ اسکادرانِ دید-در-شب و تعقیب‌کنندهٔ بی‌رحمِ گروه است؛ اما وقتی می‌بیند امضاهایش عوض شده و عکسِ زنش را نمی‌شناسد، روی پلِ فلزی علیه کامران می‌ایستد.'),
    ('بهرام', 62, 'زمین‌شناسِ کهنه‌کار و نگارندهٔ دفترِ شش اسم', ['bahram-62-v1'],
     'در بخشِ قرنطینهٔ تنگه گیر افتاده؛ نجاتش در فصل ۶ دفترِ شش اسم و رازِ زیست-شیمیاییِ «رگهٔ H-0» را آشکار می‌کند.'),
    ('رستم', 48, 'مسئولِ تدارکات', ['rostam-v2', 'rostam-v1'],
     'بزدل اما صادق‌تر از کامران؛ مجوزِ بازرسی را جعل کرده تا کار نخوابد، ولی وقتی نوبتِ پاک‌شدنِ خودش می‌رسد، کدهای اتاقکِ کیان و نقشه‌ها را به کمپ می‌آورد.'),
    ('فرهاد', 34, 'نگهبانِ بی‌نام (بازوبندِ ۹)', [],
     'یکی از پاک‌شده‌های مسلحِ کامران که در جیبش فقط یک رسیدِ چروکِ «نان و شیر» دارد و در سپیدهٔ پایان بالاخره نامش را پس می‌گیرد.'),
    ('ماهرخ', 58, 'آشپز و حافظهٔ قدیمِ کمپ', [],
     'بزرگ‌ترِ کمپ که کامران را از جوانی می‌شناخته؛ با غذای داغ و حرف‌های بی‌پرده، ستونِ روحیهٔ گروه در شب‌های سختِ لوت است.'),
]

QUOTES = {
    'دانیال': 'اسمش علی بود. هشت سالش بود. من دو سال ازش فرار کردم... دیگه فرار نمی‌کنم.',
    'سارا': 'تو دو سال با اون پاکتِ مهرشده رانندگی کردی؛ چون سکوتت راحت‌تر بود!',
    'کامران': 'حافظه بزرگ‌ترین نفرینِ آدمه؛ من دارم به آدما آرامش می‌فروشم.',
    'مهدی': 'این اسباب‌بازیِ کیان جونش به یه بندِ پلاستیکی بنده... افتاد از حقوقِ خودت کم می‌کنم!',
    'نادر': 'هفت سال پیش شیش تا مردِ گردن‌کلفت رفتن تو، فقط من با پای شکسته برگشتم.',
    'کیان': 'اگه صدای منو دارین یه فحش بدین بفهمم زنده‌این!',
    'مینا': 'یه قدم دیگه بیای جلو، به جایِ چرخِ کامیونت، زانوت رو می‌زنم راننده.',
    'آرش': 'بذار من با چهارچرخ از شیارِ غربی برم، تا بفهمن از کجا خوردن کارشون تمومه!',
    'رویا': 'مادرخراب‌ها کاروانسرام رو آتیش زدن! امشب هیچی از پروژه‌ش سرِ پا نمی‌ذاریم.',
    'اسماعیل': 'اسمِ زنم رو یادم نمی‌آد دانیال، ولی اسمِ خودم رو هنوز یادمه!',
    'بهرام': 'اینجا معدنِ لیتیوم نیست؛ کامران داره از این گسل داروی پاک‌کردنِ حافظه می‌سازه.',
    'رستم': 'امضا رو مجبور نیستی بخونی.',
    'فرهاد': 'یادم... نمی‌آد. فقط گفتن کامیون رو نذارین رد شه.',
    'ماهرخ': 'اون سال که اومد فقط یه لیوان آب می‌خورد و می‌گفت سیره؛ بعد دیدم هیچ‌وقت سیر نشد.',
}
ORDER = [p[0] for p in PEOPLE]

COPY = {
    'heroTitle': 'ردِ هور — نسخهٔ ۱۱ (بازطراحیِ AAA)',
    'heroText': 'اکشنِ جهان‌بازِ مدرن در کویرِ لوت با الهام از RDR2، GTA 6 و Resident Evil: یک راننده-مکانیکِ زخمی و یک بازرسِ سرسخت در برابرِ کارتلِ تجارتِ فراموشیِ کامران — با پهپاد، دید در شب و حرارتی، ۶ حالتِ حرکت و سواری، نبردِ سنگینِ گرم و سرد، و ۲ فصلِ نادر و هولناکِ وحشت در اعماقِ تنگه.',
    'storyLead': 'هستهٔ ۱۰ نفرهٔ گوشت‌ودار و زنده به‌جای شخصیت‌های پراکنده: هر کس صدای خودش، زخمش، شوخی‌اش و نقشِ ملموسش در کمپ و عملیات را دارد.',
    'mapLead': 'جغرافیای واقعیِ شهداد تا تنگِ رتیل در لوتِ شمالی، مبنای ۶ ناحیهٔ دنیای باز و تنگهٔ هور است؛ تأسیسات و پایگاه‌های داستان ساختگی‌اند.',
    'mapTitles': ['نقشهٔ منطقه: شهداد تا تنگ', 'نمای ماهواره‌ای محدودهٔ تنگ', 'اتصالِ ناحیه‌های بازی'],
    'mapTexts': [
        'جای واقعیِ آبادی‌ها و راه‌های اصلی. فاصلهٔ مستقیمِ شهداد تا تنگ حدود ۹۸٫۸ کیلومتر است و الهام‌بخشِ مسیرهای رانندگی و شترسواری در بازی است.',
        'تصویر ماهواره‌ایِ مرجع محدودهٔ تنگِ رتیل؛ هیچ مسیرِ حدسیِ درون تنگه به‌عنوان برداشت واقعی ادعا نشده است.',
        'نمودارِ ارتباطِ نواحی بازی (شهداد، نبکا، کلوت، کاروانسرا، نیروگاه، کمپ و تنگهٔ هور).',
    ],
}

V11_MISSIONS = [
    (1, 'M01', 'بارِ کج و حیاطِ کارگاه', 45, 'R01', ['پیاده', 'نبردِ مشت', 'کارگاه']),
    (1, 'M02', 'مجوزِ جعلیِ سپهرِ لوت', 35, 'R01', ['داستان', 'سارا', 'کامران']),
    (1, 'M03', 'میدانِ تیر و آماده‌سازیِ پیرمرد', 40, 'R01', ['سلاحِ گرم', 'آموزش', 'مهدی']),
    (2, 'M04', 'کمینِ کلوت و تیراندازیِ جاده‌ای', 55, 'R03', ['کامیون‌سواری', 'تیراندازیِ حینِ سواری', 'چهارچرخ']),
    (2, 'M05', 'چهرهٔ بی‌نام (بازوبندِ ۹)', 40, 'R03', ['سلاحِ سرد', 'Parry', 'داستان']),
    (2, 'M06', 'اردوگاهِ پژوهشی و شبی که چراغ رفت', 45, 'R07', ['کمپ', 'شترسواری', 'پهپاد']),
    (3, 'M07', 'نبکاها، شکار و آبشخورِ خشکیده', 55, 'R02', ['شترسواریِ درا', 'شکار', 'مینا']),
    (3, 'M08', 'پمپ‌خانهٔ نبکا — اولین پروازِ پهپاد', 60, 'R02', ['پهپاد', 'موتور تریل', 'اکشنِ آزاد']),
    (4, 'M09', 'باس ۱: کاروانِ طوفانِ کلوت', 75, 'R03', ['باس‌فایت', 'SUV و کامیون', 'دوربینِ حرارتی']),
    (4, 'M10', 'بازگشتِ مهدی به کمپِ سنگ‌چین', 40, 'R06', ['کمپِ زنده', 'ارتقای NVG', 'نادر']),
    (5, 'M11', 'عملیاتِ شبانهٔ نیروگاهِ خورشیدی', 70, 'R04', ['پهپاد', 'دید در شب NVG', 'تک‌تیراندازی']),
    (5, 'M12', 'کلیدِ دروازه و صدای کامران', 45, 'R04', ['اتاقِ کنترل', 'اکشنِ شبانه', 'داستان']),
    (6, 'M13', 'ورود به قرنطینهٔ تنگه (فصلِ وحشت ۱)', 55, 'R08', ['Resident Evil', 'دوربینِ حرارتی', 'تاریکی']),
    (6, 'M14', 'باس ۲: حیدر در تالارِ دو سایه', 65, 'R08', ['باس‌فایتِ رتیل', 'شاتگان و منور', 'Parry']),
    (6, 'M15', 'نجاتِ بهرام و دفترِ شش اسم', 45, 'R08', ['نجات', 'رازِ رگه', 'فرار']),
    (7, 'M16', 'بازارِ سیاهِ کاروانسرا و دعوای حیاط', 55, 'R06', ['سلاحِ سرد و مشت', 'رویا', 'تیونینگ']),
    (7, 'M17', 'پاکتِ «بقیهٔ حساب» و رولورِ نادر', 35, 'R06', ['درام', 'تعارضِ گروه', 'نادر']),
    (8, 'M18', 'شکار در نمکزار با چهارچرخ و درا', 75, 'R05', ['چهارچرخ Quad', 'شترسواری', 'نجات']),
    (9, 'M19', 'باس ۳: حریقِ کاروانسرا و هلی‌کوپتر', 85, 'R06', ['باس‌فایت', 'محاصره', 'تک‌تیراندازِ سنگین']),
    (10, 'M20', 'ظهرِ مصنوعی و معاملهٔ صادقی', 60, 'R07', ['پهپادِ EMP', 'دید در شب', 'عکاسیِ مدرک']),
    (10, 'M21', 'افشای «مشتری د» و فرارِ شبانه', 60, 'R07', ['رازِ علی', 'موتور تریل', 'تعقیبِ شبانه']),
    (11, 'M22', 'شکاف در کمپ و اعترافِ رستم', 45, 'R07', ['کمپِ دوم', 'درامِ آرش', 'کدهای اعماق']),
    (11, 'M23', 'امضای پاک‌شدهٔ اسماعیل', 35, 'R04', ['خطِ موازی', 'اسماعیل', 'تراژدی']),
    (11, 'M24', 'تماسِ زندهٔ کیان از اعماق', 35, 'R07', ['رادیو', 'برنامه‌ریزیِ نجات']),
    (12, 'M25', 'اتاقکِ آهنی (فصلِ وحشت ۲)', 60, 'R08', ['Resident Evil', 'نجاتِ کیان', 'شاتگان']),
    (12, 'M26', 'باس ۴: محاصرهٔ پلِ فلزی و ایستادگیِ اسماعیل', 80, 'R08', ['باس‌فایتِ پل', 'رتیل + مزدور', 'تبر و شاتگان']),
    (13, 'M27', 'اعترافِ «علی» زیرِ طاقِ تنگه', 35, 'R08', ['درامِ دانیال و سارا']),
    (13, 'M28', 'تعقیبِ برجِ رادیو و فداکاریِ مهدی', 75, 'R03', ['موتور و SUV', 'اکشنِ پرشتاب', 'دفترِ کامران']),
    (14, 'M29', 'یورشِ گروهی به نیروگاه و دکلِ پارازیت', 95, 'R04', ['کامیونِ زره‌کوب', 'پهپاد', '۶ حالتِ حرکت']),
    (15, 'M30', 'باس ۵: حجرهٔ رگه — دوئلِ دوفاز با کامران', 85, 'R08', ['باسِ نهایی', 'سلاحِ گرم و سرد', 'ردِ فراموشی']),
    (15, 'M31', 'سپیدهٔ دشت، شش اسم و فرهاد', 35, 'R08', ['پایان‌بندی', 'اسم‌ها']),
    (15, 'M32', 'پاکتِ «بقیهٔ حساب» و اپیلوگِ شهداد', 30, 'R01', ['اپیلوگ', 'علی']),
]

V11_SIDE_STORIES = [
    ('Q01', 'خطِ کلوت — چالشِ موتور تریل و چهارچرخ (آرش)',
     'مسابقه و تعقیبِ شبانه میانِ شیارهای کلوت همراه با آرش که به کشفِ یک انبارِ مخفیِ سلاح و قطعاتِ تیونینگِ کامران و آزمونِ بلوغِ آرش ختم می‌شود.\n\n- **فاز ۱:** پرش و زمان‌گیری با موتورِ تریل در هزارتوی کلوت.\n- **فاز ۲:** ردیابیِ چهارچرخ‌های قاچاقی با دوربینِ حرارتی در غروب.\n- **فاز ۳:** یورشِ دو نفره به انبارِ کلوت و بازکردنِ اگزوز و کمک‌فنرِ مسابقه‌ای.'),
    ('Q02', 'چشمِ شب — ارتقای پهپاد و دید در شب (مهدی)',
     'مأموریت‌های تخصصی با مهدی برای دزدیدنِ ماژول‌های نظامی از دکلِ مخابراتیِ کامران و آزادکردنِ پالسِ EMP و دیدِ حرارتی روی پهپاد.\n\n- **فاز ۱:** صعودِ شبانه به دکلِ فرعی با NVG و چاقو.\n- **فاز ۲:** هکِ جعبهٔ مخابراتی زیرِ فشارِ گشت‌های چهارچرخ.\n- **فاز ۳:** آزمایشِ میدانیِ پالسِ EMP پهپاد روی برجِ نورافکن.'),
    ('Q03', 'تفنگِ نادر — شش یادگاریِ گمشده',
     'یافتنِ ۶ یادگاریِ شخصیِ کارگرانِ هفت سال پیش در خانه‌ها و انبارهای متروکهٔ شهداد همراه با نادر، و شکارِ تک‌تیراندازِ قدیمیِ کامران.\n\n- **فاز ۱:** سرزدن به اتاقِ کارگرانِ قدیم در شهداد.\n- **فاز ۲:** دوئلِ تک‌تیراندازیِ دوربرد از روی کلوت‌ها با باد و مسافت‌سنج.\n- **فاز ۳:** ثبتِ کاملِ داستانِ شش کارگر در دفترِ سارا.'),
    ('Q04', 'سرقتِ لیتیوم — عملیاتِ بزرگِ کاروانسرا (رویا)',
     'یک عملیاتِ سرقتِ دو مرحله‌ای (`GTA Heist`) به سفارشِ رویا علیه کاروانِ زرهیِ لیتیومِ کامران با همکاریِ کلِ وسایل نقلیهٔ گروه.\n\n- **فاز ۱:** شناساییِ مسیرِ کاروان با پهپاد و کاشتنِ بمبِ C4 روی جاده.\n- **فاز ۲:** حملهٔ هماهنگ با «پیرمرد»، SUV و چهارچرخ و نبردِ سنگین.\n- **فاز ۳:** تحویلِ محموله و بازشدنِ شاتگانِ نیمه‌خودکار و تک‌تیراندازِ سنگین.'),
    ('Q05', 'آبِ دزدیده‌شده و شکار در نبکاها (مینا)',
     'پاک‌سازیِ پمپ‌های غیرمجاز، شکارِ کویریِ مجاز برای کمپ با «درا»، و عکاسیِ تحقیقی از حیات‌وحشِ نادرِ لوت و مسیرهای شبانهٔ کامران.\n\n- **فاز ۱:** شترسواریِ بی‌صدا در نبکاها و کاشتنِ دوربین‌های تله‌ای.\n- **فاز ۲:** خرابکاری در ایستگاهِ پمپاژ با موتورِ برقیِ مینا.\n- **فاز ۳:** بازگرداندنِ جریانِ آبشخور و کشفِ مسیرِ مخفیِ ورود به تنگه.'),
    ('Q06', 'رسیدِ نان و شیر — ردِ نگهبانِ ۹ (فرهاد)',
     'تعقیبِ سرنخِ رسیدِ چروک‌شدهٔ نگهبانِ شماره ۹ در شهداد و یافتنِ حقیقتِ خانواده‌ای که هفت سال است منتظرِ بازگشتِ اویند.\n\n- **فاز ۱:** بررسیِ تاریخ و مغازهٔ روی رسید در شهداد.\n- **فاز ۲:** یافتنِ پروندهٔ مفقودی در بایگانیِ محلی.\n- **فاز ۳:** پیوندِ عاطفی با صحنهٔ سپیدهٔ فصل ۱۵.'),
]


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
    if stem.startswith('v11-'):
        return 'کانسپت نسخهٔ ۱۱'
    if stem.startswith('env-') or stem in ('canyon-day-v1', 'caravanserai-night-v1'):
        return 'محیط'
    if stem.startswith(('pirmard', 'vehicle', 'camel-pack')):
        return 'وسیله'
    if stem.startswith(('hoor-', 'dara-')):
        return 'جانور و هور'
    return 'شخصیت'


def build(max_mb: float) -> dict:
    index = json.loads(read(IMAGES / 'image-index.json'))
    status = {Path(a['filename']).stem: a['status'] for a in index['assets']}
    manifest = json.loads(read(IMAGES / 'completion-manifest.json'))
    titles = {Path(a['filename']).stem: a['title'] for a in manifest['assets']}
    titles['v11-action-kalut-convoy-v1'] = 'کمینِ کاروانِ طوفان در کلوت‌ها (کانسپت نسخهٔ ۱۱)'

    docs = []
    for doc_id, (rel, category, spoiler, legacy) in DOCS.items():
        p = ROOT / rel
        if not p.exists():
            continue
        md = read(p)
        docs.append({
            'id': doc_id,
            'file': rel,
            'title': first_h1(md, doc_id),
            'category': category,
            'description': first_paragraph(md),
            'markdown': md,
            'legacy': legacy,
            'spoiler': spoiler,
            'words': len(md.split()),
        })

    screenplay = read(V11 / 'SCREENPLAY_V11_FA.md')
    headings = re.findall(r'^## فصل (\d+) — (.+)$', screenplay, flags=re.M)
    assert len(headings) == 15, headings

    # Build v11 budget object
    chapter_minutes = [0] * 15
    main_missions = []
    for ch_num, mid, title_fa, mins, region, tags in V11_MISSIONS:
        chapter_minutes[ch_num - 1] += mins
        main_missions.append({
            'id': mid,
            'chapter': ch_num,
            'title_fa': title_fa,
            'minutes': mins,
            'primary_region': region,
            'focus_tags_fa': tags,
        })
    budget = {
        'version': 'v11-aaa',
        'chapter_minutes': chapter_minutes,
        'main_minutes_total': sum(chapter_minutes),
        'side_minutes_total': 480,
        'exploration_minutes_total': 300,
        'total_target_minutes': sum(chapter_minutes) + 480 + 300,
        'main_missions': main_missions,
    }

    chapters = []
    for n, t in headings:
        clean_t = t.strip().replace(' ★', '')
        clean_t = re.sub(r'\s*\([^)]*فصلِ وحشت[^)]*\)\s*$', '', clean_t).strip()
        chapters.append({'number': int(n), 'title': clean_t, 'minutes': chapter_minutes[int(n) - 1]})

    summaries = []
    chapter_sections = [x for x in re.split(r'^## ', screenplay, flags=re.M) if re.match(r'^فصل \d+ — ', x)]
    assert len(chapter_sections) == 15, len(chapter_sections)
    for sec in chapter_sections:
        paras = [
            q.strip() for q in sec.split('\n', 1)[1].split('\n\n')
            if q.strip() and not q.strip().startswith(('**نما', '---', ':', '**باس', '**سکانس', '**عملیات', '- '))
        ]
        text = next((q for q in paras if '«' not in q), paras[0] if paras else '')
        summaries.append(re.sub(r'\s+', ' ', re.sub(r'[*_`]', '', text)))

    side = [{'id': sid, 'title': title, 'markdown': md} for sid, title, md in V11_SIDE_STORIES]

    stems = sorted(p.stem for p in IMAGES.glob('*.png'))
    # Put v11 concept art first in gallery
    stems = [s for s in stems if s.startswith('v11-')] + [s for s in stems if not s.startswith('v11-')]

    people = []
    for name, age, role, candidates, text in PEOPLE:
        image = next((c for c in candidates if c in stems and (status.get(c) != 'retired_story_reference' or c in NOT_RETIRED)), None)
        people.append({'name': name, 'age': age, 'role': role, 'image': image, 'text': text, 'quote': QUOTES.get(name, '')})
    people.sort(key=lambda p: ORDER.index(p['name']) if p['name'] in ORDER else 99)

    max_edge, quality = 1280, 76
    while True:
        media, gallery = {}, []
        for stem in stems:
            retired = status.get(stem) == 'retired_story_reference' and stem not in NOT_RETIRED
            caption = (
                'کانسپت‌آرتِ جدیدِ نسخهٔ ۱۱ (بازطراحیِ AAA).' if stem.startswith('v11-')
                else ('ایدهٔ کنارگذاشته‌شده؛ مرجعِ داستانِ فعلی نیست.' if retired else 'مرجعِ تصویری پیشین؛ برای نسخهٔ ۱۱ بازطراحیِ بصری جدید تعریف شده است.')
            )
            gallery.append({
                'id': stem,
                'title': titles.get(stem) or humanize(stem),
                'filename': f'{stem}.png',
                'category': category_of(stem),
                'caption': caption,
                'retired': retired,
            })
            media[stem] = b64_image(IMAGES / f'{stem}.png', max_edge, quality)
        for name in ('region-map', 'canyon-map', 'design-map'):
            media[name] = b64_image(V7 / 'maps' / f'{name}.png', 1600 if name != 'design-map' else 1200, 80)
        snapshot = {
            'library': {
                'docs': docs,
                'gallery': gallery,
                'budget': budget,
                'chapters': chapters,
                'sideStories': side,
                'people': people,
                'chapterSummaries': summaries,
                'copy': COPY,
            },
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
    lib, media = snapshot['library'], snapshot['media']
    assert lib['docs'] and lib['gallery'] and all(g['id'] in media for g in lib['gallery'])
    assert 'https://esm.sh/d3-geo@3.1.1' in snapshot['mapHtml']
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snapshot, ensure_ascii=False), encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)}: docs={len(lib["docs"])} gallery={len(lib["gallery"])} '
          f'chapters={len(lib["chapters"])} side={len(lib["sideStories"])} people={len(lib["people"])}')


if __name__ == '__main__':
    main()
