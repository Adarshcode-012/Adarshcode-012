from pathlib import Path
from collections import Counter
from html import escape
import os
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'languages.svg'
USERNAME = 'Adarshcode-012'
API = f'https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner&sort=updated'

headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'profile-language-card'}
if token := os.getenv('GITHUB_TOKEN'):
    headers['Authorization'] = f'Bearer {token}'
repos = requests.get(API, headers=headers, timeout=30).json()
if not isinstance(repos, list):
    raise RuntimeError(f'Could not load repositories: {repos}')

totals = Counter()
for repo in repos:
    if repo.get('fork') or repo.get('archived'):
        continue
    languages = requests.get(repo['languages_url'], headers=headers, timeout=30).json()
    if isinstance(languages, dict):
        totals.update({name: int(size) for name, size in languages.items()})

top = totals.most_common(5)
if not top:
    raise RuntimeError('No repository language data found.')

total_bytes = sum(totals.values())
colors = ['#0969da', '#8250df', '#1f883d', '#bf8700', '#cf222e']
rows = []
for i, (language, size) in enumerate(top):
    y = 62 + i * 20
    percent = size / total_bytes * 100
    rows.append(f'''<circle cx="31" cy="{y-4}" r="4" fill="{colors[i]}"/>
<text x="43" y="{y}" fill="var(--body)" font-family="ui-sans-serif,system-ui,sans-serif" font-size="12">{escape(language)}</text>
<text x="878" y="{y}" text-anchor="end" fill="var(--muted)" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11">{percent:.1f}%</text>
<rect x="170" y="{y-10}" width="680" height="7" rx="3.5" fill="var(--track)"/>
<rect x="170" y="{y-10}" width="{680 * percent / 100:.1f}" height="7" rx="3.5" fill="{colors[i]}"/>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="920" height="178" viewBox="0 0 920 178">
<style>
  :root {{ --border: #d0d7de; --title: #1f2328; --body: #24292f; --muted: #656d76; --track: #d8dee4; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --border: #30363d; --title: #f0f6fc; --body: #c9d1d9; --muted: #8b949e; --track: #21262d; }} }}
</style>
<rect x="10" y="10" width="900" height="158" rx="18" fill="none" stroke="var(--border)"/>
<text x="28" y="39" fill="var(--title)" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="16" font-weight="700">MOST USED LANGUAGES</text>
<text x="28" y="54" fill="var(--muted)" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10">public, non-fork repositories · by code volume</text>
{''.join(rows)}
</svg>'''
OUT.write_text(svg, encoding='utf-8')
print(f'Wrote {OUT}')
