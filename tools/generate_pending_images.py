#!/usr/bin/env python3
"""Generate pending images from gameStory/images/pending-wildlife-and-action-prompts.json
using GEMINI_API_KEY from .env (requires Paid/Tier-1 enabled on Google AI Studio for image models),
register them in image-index.json and completion-manifest.json, and rebuild the site snapshot.
"""
import base64
import hashlib
import io
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / 'gameStory/images'
PENDING = IMG_DIR / 'pending-wildlife-and-action-prompts.json'


def load_api_key() -> str:
    env_path = ROOT / '.env'
    if not env_path.exists():
        sys.exit('Error: .env file not found in project root.')
    txt = env_path.read_text(encoding='utf-8-sig', errors='ignore').strip()
    m = re.search(r'(?:GEMINI_API_KEY|GOOGLE_API_KEY)\s*=\s*["\']?([^\s"\']+)', txt)
    return m.group(1) if m else txt.split()[0]


def main() -> None:
    key = load_api_key()
    spec = json.loads(PENDING.read_text(encoding='utf-8'))
    idx_path = IMG_DIR / 'image-index.json'
    idx = json.loads(idx_path.read_text(encoding='utf-8-sig'))
    existing_idx = {a['filename']: a for a in idx['assets']}

    man_path = IMG_DIR / 'completion-manifest.json'
    man = json.loads(man_path.read_text(encoding='utf-8-sig'))

    generated_any = False
    for item in spec['images']:
        dst = IMG_DIR / item['filename']
        if dst.exists():
            print(f'Skipping (already exists): {dst.name}')
            continue

        inputs = [{'type': 'text', 'text': item['prompt']}]
        for ref in item.get('references', []):
            ref_p = ROOT / ref
            if ref_p.exists():
                with Image.open(ref_p) as im:
                    im = im.convert('RGB')
                    im.thumbnail((1024, 1024))
                    buf = io.BytesIO()
                    im.save(buf, format='JPEG', quality=85)
                inputs.append({
                    'type': 'image',
                    'mime_type': 'image/jpeg',
                    'data': base64.b64encode(buf.getvalue()).decode('ascii'),
                })

        aspect = '2:3' if item['group'] == 'characters' else '16:9'
        body = json.dumps({
            'model': 'gemini-nano-banana-2.1',
            'input': inputs,
            'response_format': {
                'type': 'image',
                'aspect_ratio': aspect,
                'image_size': '1K',
                'mime_type': 'image/jpeg',
            },
        }).encode('utf-8')

        req = urllib.request.Request(
            'https://generativelanguage.googleapis.com/v1beta/interactions',
            data=body,
            headers={
                'x-goog-api-key': key,
                'Content-Type': 'application/json',
                'Api-Revision': '2026-05-20',
            },
            method='POST',
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                res = json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8', errors='ignore')
            print(f'API error on {item["filename"]} ({e.code}): {err_body}')
            sys.exit(1)

        img_b64 = None
        if res.get('output_image') and res['output_image'].get('data'):
            img_b64 = res['output_image']['data']
        else:
            for st in res.get('steps', []):
                for c in st.get('content', []):
                    if c.get('type') == 'image' and c.get('data'):
                        img_b64 = c['data']
        if not img_b64:
            print(f'No image returned for {item["filename"]}')
            continue

        raw = base64.b64decode(img_b64)
        with Image.open(io.BytesIO(raw)) as im:
            im.save(dst, format='PNG')
            w, h = im.size
        data = dst.read_bytes()
        sha = hashlib.sha256(data).hexdigest()

        existing_idx[item['filename']] = {
            'filename': item['filename'],
            'bytes': len(data),
            'width': w,
            'height': h,
            'sha256': sha,
            'status': 'visual_reference_not_final_v7',
            'canon_authority': False,
        }
        entry = {
            'id': item['id'],
            'group': item['group'],
            'title': item['title'],
            'filename': item['filename'],
            'bytes': len(data),
            'sha256': sha.upper(),
            'status': 'generated',
        }
        if any(a['filename'] == item['filename'] for a in man['assets']):
            man['assets'] = [entry if a['filename'] == item['filename'] else a for a in man['assets']]
        else:
            man['assets'].append(entry)

        generated_any = True
        print(f'Generated and registered: {dst.name} ({w}x{h}, {len(data)} bytes)')

    if generated_any:
        idx['assets'] = [existing_idx[k] for k in sorted(existing_idx)]
        idx['image_count'] = len(idx['assets'])
        idx['total_bytes'] = sum(a['bytes'] for a in idx['assets'])
        idx_path.write_text(json.dumps(idx, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

        man['assetCount'] = len(man['assets'])
        man_path.write_text(json.dumps(man, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        subprocess.run([sys.executable, str(ROOT / 'tools/build_snapshot.py')], check=True)


if __name__ == '__main__':
    main()
