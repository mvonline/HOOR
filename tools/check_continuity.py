"""Independent continuity check for the v7 package and the GitHub Pages site content.

Read-only. Usage: python3 -I tools/check_continuity.py
Prints a section per check; exits 0 always (the report is the product).
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V7 = ROOT / 'gameStory/redesign/v7-20261121'
STORY = ROOT / 'gameStory'
SITE = ROOT / 'sites/hoor-github-pages-20261121'

FA_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')


def norm(text: str) -> str:
    text = text.translate(FA_DIGITS).replace('‌', ' ').replace('ي', 'ی').replace('ك', 'ک')
    text = re.sub(r'[\*\_\`«»"“”\'’\[\]\(\)\.,،؛:؟\?!…—–\-]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


docs = {p.name: read(p) for p in sorted(V7.glob('*.md'))}
problems = defaultdict(list)


def report(section, msg):
    problems[section].append(msg)


# ---------------------------------------------------------------- A. budget arithmetic
budget = json.loads(read(V7 / 'content-budget.json'))
ch_min = budget['chapter_minutes']
by_ch = defaultdict(int)
ids = [m['id'] for m in budget['main_missions']]
if len(ids) != len(set(ids)) or ids != [f'M{i:02d}' for i in range(1, 41)]:
    report('A budget', f'main mission ids not M01..M40 contiguous/unique: {ids}')
for m in budget['main_missions']:
    by_ch[m['chapter']] += m['minutes']
for i, expected in enumerate(ch_min, 1):
    if by_ch[i] != expected:
        report('A budget', f'chapter {i}: missions sum {by_ch[i]} != chapter_minutes {expected}')
if sum(ch_min) != budget['target_totals']['main_minutes']:
    report('A budget', f'chapter sum {sum(ch_min)} != main_minutes {budget["target_totals"]["main_minutes"]}')
side_total = 0
for chain in budget['side_chains']:
    ph = sum(p['minutes'] for p in chain['phases'])
    side_total += chain['minutes']
    if ph != chain['minutes']:
        report('A budget', f'{chain["id"]}: phases {ph} != {chain["minutes"]}')
expl = sum(x['minutes'] for x in budget['exploration_packs'])
t = budget['target_totals']
for label, got, want in [('side', side_total, t['side_minutes']), ('exploration', expl, t['exploration_minutes']),
                         ('total', sum(ch_min) + side_total + expl, t['balanced_total_minutes'])]:
    if got != want:
        report('A budget', f'{label}: {got} != {want}')
canyon = sum(1 for m in budget['main_missions'] if m['primary_region'].startswith('R08') or 'canyon' in str(m.get('primary_region')).lower())
claimed = budget['canyon_focus']['main_missions_with_primary_region_canyon']
print(f'[info] missions whose primary region is R08*: {canyon} (budget claims {claimed} canyon-primary; region naming decides)')

# ---------------------------------------------------------------- B. ID presence across documents
need = {
    'WORLD_AND_MISSIONS_FA.md': [f'M{i:02d}' for i in range(1, 41)] + [f'Q{i:02d}' for i in range(1, 9)] + [f'X{i:02d}' for i in range(1, 7)] + ['W01', 'W02'],
    'SCREENPLAY_AND_FINAL_SEQUENCE_FA.md': [f'M{i:02d}' for i in range(1, 41)],
    'ONBOARDING_AND_LEARNING_FA.md': [f'M{i:02d}' for i in range(1, 41)],
    'RECORDINGS_DOCUMENTS_AND_DIRECTION_FA.md': [f'T{i:02d}' for i in range(1, 7)] + [f'D{i:02d}' for i in range(1, 11)],
}
for fname, wanted in need.items():
    body = docs[fname]
    missing = [w for w in wanted if not re.search(rf'\b{w}\b', body)]
    if missing:
        report('B ids', f'{fname} missing {missing}')
# every M id mentioned anywhere must exist in M01..M40
valid = set(ids)
for fname, body in docs.items():
    stray = sorted({m for m in re.findall(r'\bM(\d{2,3})\b', body) if f'M{m}' not in valid})
    if stray:
        report('B ids', f'{fname} references unknown mission ids M{stray}')
# duplicate mission headings in the world doc
heads = re.findall(r'^#{2,4}\s*(M\d\d)\b', docs['WORLD_AND_MISSIONS_FA.md'], flags=re.M)
dup = {h for h in heads if heads.count(h) > 1}
if dup:
    report('B ids', f'WORLD has duplicate mission headings {sorted(dup)}')

# ---------------------------------------------------------------- C. local links
link_re = re.compile(r'\]\(([^)#\s]+)(?:#[^)]*)?\)')
for p in list(V7.glob('*.md')) + [V7 / 'maps/README_FA.md', STORY / 'README.md']:
    for target in link_re.findall(read(p)):
        if re.match(r'^[a-z]+:', target):
            continue
        if not (p.parent / target).resolve().exists():
            report('C links', f'{p.relative_to(ROOT)} -> {target} missing')

# ---------------------------------------------------------------- D. retired 6.2 rules leaking into v7
retired = ['دور هفتم', 'بازتولید', 'محوشدن', 'محو شد', 'بیست سال', 'استاز', 'بانگ', 'پژواک‌های هور',
           'Hambar Integration', 'جیب زمان‌کند']
retire_ctx = re.compile(r'(حذف|بازنشسته|منتقل نمی|ممنوع|نداریم|نمی‌شود|سابقه|قدیمی|۶\.۲|6\.2|نه |بدون|جداست)')
for fname, body in docs.items():
    if fname in ('VISION_AND_CAMPAIGN_FA.md', 'CONTINUITY_AND_STORY_REVIEW_FA.md', 'DESIGN_REVIEW_FA.md'):
        continue
    for n, line in enumerate(body.splitlines(), 1):
        for term in retired:
            if term in line and not retire_ctx.search(line):
                report('D retired-term (unframed)', f'{fname}:{n} [{term}] {line.strip()[:140]}')

# ---------------------------------------------------------------- E. per-mission minute mentions vs budget
bud = {m['id']: m['minutes'] for m in budget['main_missions']}
mm = re.compile(r'(\d+)\s*دقیقه')
for fname in ('SCREENPLAY_AND_FINAL_SEQUENCE_FA.md', 'WORLD_AND_MISSIONS_FA.md', 'ONBOARDING_AND_LEARNING_FA.md', 'ACTION_ENCOUNTER_ATLAS_FA.md'):
    for n, line in enumerate(docs[fname].splitlines(), 1):
        mids = set(re.findall(r'\bM\d\d\b', line))
        if len(mids) == 1:
            mid = next(iter(mids))
            for val in mm.findall(line.translate(FA_DIGITS)):
                v = int(val)
                if mid in bud and v >= 15 and v != bud[mid] and re.search(r'بودجه|ظرفیت|مدت', line):
                    report('E minutes', f'{fname}:{n} {mid} mentions {v} but budget={bud[mid]} :: {line.strip()[:110]}')

# ---------------------------------------------------------------- F. character facts
ages = {'دانیال': '38', 'سارا': '35', 'کامران': '45', 'کیان': '24', 'بهرام': '62', 'رستم': '48', 'مینا': '32'}
age_re = re.compile(r'(دانیال|سارا|کامران|کیان|بهرام|رستم|مینا)[^\n.]{0,12}?[،,]\s*([0-9۰-۹]{2})\b')
for fname, body in docs.items():
    for who, age in age_re.findall(body):
        age = age.translate(FA_DIGITS)
        if ages[who] != age:
            report('F ages', f'{fname}: {who} age {age} (character doc says {ages[who]})')

# ---------------------------------------------------------------- G. site content vs sources
sc = norm(docs['SCREENPLAY_AND_FINAL_SEQUENCE_FA.md'])
rec = norm(docs['RECORDINGS_DOCUMENTS_AND_DIRECTION_FA.md'])
dlg = json.loads(read(SITE / 'content/dialogues.json'))
lines_total = scenes_total = 0
for ch in dlg['chapters']:
    for scene in ch['scenes']:
        scenes_total += 1
        for ln in scene['lines']:
            lines_total += 1
            if norm(ln['text']) not in sc:
                report('G site dialogues', f'ch{ch["number"]} {scene["id"]} line not in screenplay: {ln["text"][:70]}')
        if scene['id'] not in ids and not re.fullmatch(r'C\d+', scene['id']):
            report('G site dialogues', f'unknown scene id {scene["id"]}')
fa_digits = str(lines_total).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
if fa_digits not in dlg['note']:
    report('G site dialogues', f'dialogues.json note does not state the real line count {lines_total}')
print(f'[info] dialogues.json: chapters={len(dlg["chapters"])} scenes={scenes_total} lines={lines_total}')
rec_lines = 0
for r in dlg['recordings']:
    for ln in re.findall(r'^\s*(?!\*\*)[^:\n]{1,40}:\s*(.+)$', r['markdown'], flags=re.M):
        rec_lines += 1
        if ln.startswith('**') or norm(ln) in rec or norm(ln) in sc:
            continue
        if True:
            report('G site recordings', f'{r["id"]} speech not in recordings doc: {ln[:70]}')
print(f'[info] recordings speech-like lines (heuristic): {rec_lines}; note claims 37')
heads_sc = re.findall(r'^## فصل (\d+) — (.+)$', docs['SCREENPLAY_AND_FINAL_SEQUENCE_FA.md'], flags=re.M)
for (num, title), ch in zip(heads_sc, dlg['chapters']):
    if norm(title) != norm(ch['title']) or int(num) != ch['number']:
        report('G site dialogues', f'chapter {num} title mismatch: doc="{title}" site="{ch["title"]}"')
if len(heads_sc) != len(dlg['chapters']):
    report('G site dialogues', f'chapter count doc={len(heads_sc)} site={len(dlg["chapters"])}')

reader = json.loads(read(SITE / 'content/reader-edition.json'))
for key in reader:
    stem = key.replace('maps-README_FA', 'maps/README_FA')
    exists = (V7 / f'{stem}.md').exists() or key == 'READER_GUIDE_FA'
    if not exists:
        report('G site reader', f'reader key {key} has no source doc')
for p in V7.glob('*.md'):
    if p.stem not in reader and p.stem != 'README':
        report('G site reader', f'source doc {p.name} has no reader summary')
for key, val in reader.items():
    for target in link_re.findall(val['markdown']):
        if not re.match(r'^[a-z]+:', target) and not target.startswith('#'):
            report('G site reader', f'{key} has relative link {target} (site cannot resolve)')
    for claim in re.findall(r'(\d[\d٬,\.]*)\s*(?:ساعت|دقیقه|مأموریت)', val['markdown'].translate(FA_DIGITS)):
        pass

# ---------------------------------------------------------------- H. site build contract
pkg = json.loads(read(SITE / 'package.json'))
src = read(SITE / 'scripts/encrypt-content.mjs')
m = re.search(r"SOURCE=new URL\('([^']+)'", src)
if m and not (SITE / 'scripts' / m.group(1)).resolve().exists():
    report('H site build', f'encrypt-content.mjs SOURCE {m.group(1)} does not exist (snapshot of docs/gallery/media/mapHtml is gone)')
wf = read(ROOT / '.github/workflows/jekyll-gh-pages.yml')
if not (SITE / 'public/content.hoor').exists() and 'encrypt' not in wf:
    report('H site build', 'public/content.hoor is missing and CI does not encrypt: the deployed site cannot unlock (run npm run snapshot && npm run encrypt, commit public/content.hoor)')
if 'encrypt' not in json.dumps(pkg['scripts']):
    report('H site build', 'no npm script for the encrypt step')

# ---------------------------------------------------------------- output
total = 0
for section in sorted(problems):
    print(f'\n== {section}: {len(problems[section])}')
    for msg in problems[section][:40]:
        print('  -', msg)
    if len(problems[section]) > 40:
        print(f'  ... +{len(problems[section]) - 40} more')
    total += len(problems[section])
print(f'\nTOTAL findings: {total}')
sys.exit(0)
