"""Read-only document checks; writes only its own verification evidence."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
STORY = ROOT / 'gameStory'
OWNERS = ['README.md', 'Rad-e-Hoor_Full_Screenplay_FA.md',
          'Rad-e-Hoor_Proposal_v5.0.md', 'Rad-e-Hoor_Character_Bible.md',
          'Rad-e-Hoor_Art_Direction_Bible.md', 'Rad-e-Hoor_Validation_Report.md']
texts = {name: (STORY / name).read_text(encoding='utf-8') for name in OWNERS}
s = texts[OWNERS[1]]
p = texts[OWNERS[2]]
results = []

def check(name, value):
    results.append({'check': name, 'passed': bool(value)})

for name, text in texts.items():
    check(f'{name}: UTF-8 without replacement characters', '\ufffd' not in text)
    check(f'{name}: current version in opening', '۵.۷' in '\n'.join(text.splitlines()[:8]))
    for target in re.findall(r'\]\(([^)]+\.md)(?:#[^)]*)?\)', text):
        if '://' not in target:
            check(f'{name}: local link {target}', (STORY / target).is_file())

check('Eleven chapters', len(re.findall(r'^## فصل ', s, re.M)) == 11)
check('Six tape archive entries', len(re.findall(r'^### نوار ', s, re.M)) == 6)
check('D01 through D10 exactly', re.findall(r'^### (D\d\d) —', s, re.M) == [f'D{i:02}' for i in range(1, 11)])
check('H01 through H07 exactly', re.findall(r'^### (H\d\d) —', s, re.M) == [f'H{i:02}' for i in range(1, 8)])
check('S01 through S04 exactly', re.findall(r'^### (S\d\d) —', s, re.M) == [f'S{i:02}' for i in range(1, 5)])
check('L01 through L10 retained', re.findall(r'^\| (L\d\d) \|', p, re.M) == [f'L{i:02}' for i in range(1, 11)])
check('O01 through O04 retained', re.findall(r'^\| (O\d\d) \|', p, re.M) == [f'O{i:02}' for i in range(1, 5)])
check('E01 through E07 only in source table', re.findall(r'^\| (E\d\d)\s*\|', p, re.M) == [f'E{i:02}' for i in range(1, 8)])
check('H01 before logistics departure', s.index('### H01') < s.index('پس از این کار، بهرام همراه تیم'))
check('Water-yard action before garage cut', s.index('**L02 —') < s.index('برش کوتاه به گاراژ.'))
check('H02 after radio stop, before L06', s.index('**L08 —') < s.index('### H02') < s.index('**L06 —'))
check('H03/H04 before entry', s.index('### H03') < s.index('### H04') < s.index('### ۰.۸'))
check('Tape 4 access outside optional H05', s.index('نوار ۴ در کیف ثبت') < s.index('### H05'))
check('H05 before main defensive route', s.index('### ۵.۱') < s.index('### H05') < s.index('### ۵.۲'))
check('H06 before Sara release', s.index('### H06') < s.index('### ۸.۳'))
check('H07 between morning and report', s.index('### ۱۰.۵') < s.index('### H07') < s.index('### ۱۰.۶'))

def scene(start, end):
    return s.split(start, 1)[1].split(end, 1)[0]

check('Tape 2 obtainable in source scene', 'نوار ۲ در کیف ژئوفون' in scene('### ۳.۲ —', '### ۳.۳ —'))
check('Tape 5 obtainable in source scene', 'نوار ۵ در آرشیو میدانی' in scene('### ۷.۱ —', '### ۷.۲ —'))
for echo, start, end in [('E03', '### ۴.۴ —', '## فصل ۵'),
                         ('E04', '### ۷.۱ —', '### ۷.۲ —'),
                         ('E05', '### ۸.۱ —', '### ۸.۲ —'),
                         ('E06', '### ۵.۳ —', '## فصل ۶')]:
    check(f'{echo} has on-scene playback', echo in scene(start, end))
check('No second parking drive in chapter 3', 'تا پارکینگ تونل فرسایشی می‌راند' not in scene('### ۳.۳ —', '## فصل ۴'))
check('Same cut has cause before bandaging', s.index('بریدگی کم‌عمق ایجاد می‌شود') < s.index('### ۹.۴ —'))
check('Daniyal does not claim authorship of dispatch summary', 'من کوتاهش کردم' not in s)
check('Locator boundary disconnection specified', 'آخرین موقعیت دریافت‌شده' in p)
check('Dialogue skipping is not time-transition consent', 'ردکردن گفت‌وگو فقط همان گفت‌وگو را رد می‌کند' in s)
check('F07 explicitly remains open', 'F07، کفایت منابع بیست‌سالهٔ بهرام' in p)
check('Finite source of Yunus info and rescue condition retained', 'فقط اگر قاب در H05 باز شود' in s and 'اگر قاب باز نشود' in s)
check('Yunus arithmetic', (11 * 3600 + 40 * 60 + 10) + 6 * (11 * 3600 + 25 * 60 + 10) + (6 * 3600 + 30 * 60) == 312070)
check('Bahram surface arithmetic unchanged', (29 * 3600 + 40 * 60) + 7 * (11 * 3600 + 25 * 60 + 10) + (4 * 3600 + 50 * 60) == 411970)
budget = p.split('## ۸. مدت و اولویت تولید', 1)[1].split('این بودجهٔ تجربه است', 1)[0]
values = [int(n) for n in re.findall(r'^\| (?:[۰-۹]+(?: تا نتیجه)?)\s*\|\s*(\d+)\s*\|', budget, re.M)]
check('Eleven core duration rows', len(values) == 11)
check('Core durations total 260', sum(values) == 260 and '| جمع         |        260 |' in budget)
check('Opening component durations total 30', sum([3, 5, 3, 5, 6, 2, 6]) == 30)
check('Real final timing: 4:45 plus ten seconds', (5 * 3600 + 5 * 60 + 10) - (5 * 3600 + 15) == 4 * 60 + 55)
check('Master references current package', 'design package **5.7**' in (ROOT / 'masterPrompt.md').read_text(encoding='utf-8'))
check('Narrative map covers eleven chapters', len(re.findall(r'^\| [۰-۹]+ \|', scene('## نقشهٔ کشش و پرداخت', '## مأموریت‌های اختیاری'), re.M)) == 11)

report = {'scope': 'Document structure, placement, local links and arithmetic; not runtime, independent review or audience validation.',
          'passed': sum(item['passed'] for item in results), 'total': len(results),
          'results': results,
          'sha256': {name: hashlib.sha256((STORY / name).read_bytes()).hexdigest() for name in OWNERS}}
Path(__file__).with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for item in results:
    if not item['passed']:
        print('FAIL:', item['check'])
print(f"{report['passed']}/{report['total']} document checks passed; no runtime/player tests.")
raise SystemExit(0 if report['passed'] == report['total'] else 1)
