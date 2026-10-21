# Story Analysis — rade-hoor

Generated (UTC): 2026-10-21T18:00:42.584280+00:00

> Technical artifact. Source design package remains authoritative in `gameStory/`.

## Concept
Rad-e Hoor (The Solar Trace): audio-first survival in a Lut Desert canyon with a time loop gated by a ten-second dawn window.

## Genre
First-person audio survival / narrative thriller with light off-road traversal

## Platform
PC/Steam primary; console later; gamepad + MK from day one

## Campaign time budget (design minutes): 270

_This is a design budget, not validated playtime._

## Gameplay loop
Move and shelter while managing emitted sound; distinguish live sources from Hoor echoes; protect companions; resolve the dawn window without (or with) Bang; preserve evidence. Winch/hand-puller extend Daniel's craft under sound cost.

## Hearing notes (cited / extracted)
- محور نقشهٔ بازی جنوب‌شرق به شمال‌غرب است؛ ورود در دهانهٔ جنوب‌شرقی و خروج نهایی در گلوگاه شمال‌غربی قرار دارند. مترهای مسیر نهایی فاصله در امتداد راه‌اند، نه فاصلهٔ مستقیم. پیچ‌ها خط دید و مسیر انتشار صدا را عوض می‌کنند؛
- - رستم خطر گزارش‌شده را کوچک کرده است. او از حلقه، شرط بانگ، ناپدید شدن انسان و نسبت زمان مناطق خبر ندارد.
- | دانیال به مرز جنوب‌شرقی می‌رسد | روز ۴، ۰۵:۰۵:۱۰ | بانگ کیان در پنجرهٔ دور ۰ ثبت شده؛ نخستین برگشت رخ می‌دهد |
- **قاعدهٔ اتصال:** اولین بانگ دور ۰، ورود واقعی امدادگرِ حاضر در مرز را به غروب بازگشته وصل می‌کند. تصویر، تجهیزات و حافظهٔ همین ورود برای بازتولید ذخیره می‌شود. این قاعدهٔ فراطبیعی فقط بر اتصال مرز عمل می‌کند؛ پیام به گذ
- بانگ در این ده ثانیه ثبت می‌شود. خاموش کردن پس از ثبت، آن ثبت را لغو نمی‌کند. محوشدن و بازگشت فقط در E رخ می‌دهند؛ هیچ دستی در اولین پرتو محو نمی‌شود.
- - اگر بانگی نباشد، همهٔ بازماندگان داخل به صبح روز چهارم می‌رسند. رگه‌ها خاکستری می‌شوند. آسیب‌های قبلی درمان نمی‌شوند.
- - اگر بانگ باشد، فرد مسئول آن در E محو می‌شود. لباس و وسایل می‌مانند. دیگر افراد داخل، با حافظه و بدن فعلی، بی‌فاصله به غروب می‌رسند. ورودی دانیال دوباره ساخته می‌شود.
- 3. **پژواک هور:** فقط صدایی که قبلاً داخل مرز تولید شده است. صدا جابه‌جا بازپخش می‌شود، اما کلمات ترکیب نمی‌شوند و اطلاعات آینده ساخته نمی‌شود. هور نجوا را نیز ذخیره می‌کند؛ ذخیره‌شدن با «بانگ» یکی نیست.

## Chapter structure
- Ch0 setup / qanat / delivery (~25m design budget)
- Ch1–2 entry & camp (~15–20m)
- Ch3 soft sand / recovery (~25m)
- Ch4 Bahram time-dilated room (~30m)
- Ch5 plate defense (~25m)
- Ch6 caravanserai / optional ski / Dara (~25m)
- Ch7 evidence / R-17 (~20m)
- Ch8 heart of Hoor / Sara rescue (~25m)
- Ch9 northwest escape with companions (~35m)
- Ch10 endings: Circle / Escape / Ledge (~25m)
- Design campaign budget total: 270 minutes (not validated playtime)

## Characters
- Daniel (player) — skill and avoidance
- Sara — measurement and decision; unveiled in all languages
- Bahram — learned to ask for help; ~82 biological years in-room
- Kian — recording and fear (loop 0)
- Rostam — real help, incomplete warning
- Farhad — logistics contact
- Qasem — qanat / pengān in chapter 0
- Dara (companion animal)
- Tarantulas — three scales; hearing-driven, not magic vision

## Prohibitions / recorded constraints
- No Daniel–Sara romance
- No religious symbols in current character/props design
- Sara without hijab; hair visible; costume stable across languages
- Do not invent echoes outside E01–E07 without sourced approval
- Do not claim geo/hardware/playtest proof without evidence
- Historical v4 docs are not current production orders
- رابطهٔ دانیال و سارا حرفه‌ای است و تنش عاشقانه ندارد.
- نمادهای مذهبی در طراحی جاری شخصیت‌ها و وسایل حذف شده‌اند.
- سارا لباس سادهٔ صحرایی و بدون حجاب دارد؛ موهایش آشکار است.
- پس از آزادی سارا، ریزش زمین دلیل حرکت به شمال‌غرب است. در زمین پایدار، انتظار ساکت راه معتبر نجات است.
- رستم کمک واقعی کرده و هشدار ناقص فرستاده؛ از قواعد هور خبر نداشته است.
- مرگ دانیال بدهی اخلاقی را پاک نمی‌کند. هر سه مسیر پایان راه بقا دارند.

## Audio & accessibility
- Completable without microphone
- Headphones recommended but not mandatory for essential information
- Captions must not spoil echo speaker identity early
- Reduced-motion / reduced print FX modes required
- Hot/cold hand feedback via rumble with non-rumble alternatives

## Technical risks
- Teachability of loop + Bang + radii density
- 3D audio latency and direction discrimination
- Chapter 9 dual-path companions vs vehicle
- Print-style visual readability vs performance
- Early engine lock before hearing proof

## Open gaps
- Bahram 20-year water/food/energy balance not proven (Validation open item)
- Real canyon elevation/coordinates not surveyed as game facts
- Anchor 1.5s margin is arithmetic only — not proven playability
- Playtests 1–3 not yet executed with players
- Main game engine not ADR-locked (must wait for audio signal unless human exception)
- English player-facing adaptation not complete in design package
- | بقای بهرام | فرض آب شیرین طبیعی و چرخ‌آب حذف؛ اتاق کشت تأسیسات داستانی است؛ کفایت منابع بیست‌ساله هنوز تأیید نشده | قواعد ۲.۳؛ سناریو ۴.۲ |
- ## ۴. آزمون‌های اجراییِ هنوز انجام‌نشده
- پیوندهای شش سند، قالب‌بندی، شمار فصل‌ها و تطبیق عبارتیِ اصلاحات بررسی شدند. پوشش نوشتاریِ موارد بالا به معنی تأیید پیمودن مسیر سارا، دسترسی به باربند خودروی گیرکرده، مدت واقعی فصل ۱۰ یا رفتار هوش مصنوعی نیست. این موارد هنوز به نمونه نیاز دا

## APPROVED
- `AP-genre` First-person audio-survival with driving, companionship, exploration; fictional Lut canyon. — source: `gameStory/Rad-e-Hoor_Proposal_v5.0.md`
- `AP-platform` Primary platform PC/Steam; console stage 2; mobile only simplified later. — source: `gameStory/Rad-e-Hoor_Proposal_v5.0.md`
- `AP-window` Silence window [05:05:00, 05:05:10); Bang registration in window; resolution at E. — source: `gameStory/Rad-e-Hoor_Proposal_v5.0.md`
- `AP-hearing` Audible radius and Bang are independent tests; shelter blocks contact not sound. — source: `gameStory/Rad-e-Hoor_Proposal_v5.0.md`
- `AP-endings` Three silence paths: Circle / vehicle escape / Ledge(Anchor); death does not clear moral debt. — source: `gameStory/Rad-e-Hoor_Proposal_v5.0.md`
- `AP-sara-costume` Sara unveiled with visible short hair in current design bible. — source: `gameStory/Rad-e-Hoor_Character_Bible.md`

## ASSUMPTION
- `AS-engine` Main engine remains undecided until C0 audio Go/No-Go unless human signs ADR early. — source: `studio`
- `AS-budget` 270-minute chapter budget is a design target, not measured playtime. — source: `gameStory/Rad-e-Hoor_Proposal_v5.0.md`
- `AS-web-audio` Playtest tests 1 and 3 should start on Web Audio for speed (from Playtest Roadmap). — source: `gameStory/Playtest_Roadmap.md`

## Source paths
- `gameStory/README.md`
- `gameStory/Rad-e-Hoor_Proposal_v5.0.md`
- `gameStory/Rad-e-Hoor_Full_Screenplay_FA.md`
- `gameStory/Rad-e-Hoor_Character_Bible.md`
- `gameStory/Rad-e-Hoor_Art_Direction_Bible.md`
- `gameStory/Rad-e-Hoor_Validation_Report.md`
- `gameStory/Playtest_Roadmap.md`
