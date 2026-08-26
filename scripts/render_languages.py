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

top = totals.most_common(6)
if not top:
    raise RuntimeError('No repository language data found.')

total = sum(totals.values())
palette = ['#f1e05a', '#3572A5', '#3178c6', '#663399', '#e34c26', '#00ADD8']
bar_x, bar_y, bar_width = 34, 70, 572
segments, legend = [], []
cursor = bar_x
for index, (language, size) in enumerate(top):
    percent = size / total * 100
    width = bar_width * percent / 100
    segments.append(f'<rect x="{cursor:.1f}" y="{bar_y}" width="{width:.1f}" height="10" fill="{palette[index]}"/>')
    col, row = index % 2, index // 2
    x, y = 34 + col * 285, 114 + row * 29
    legend.append(f'<circle cx="{x + 6}" cy="{y - 4}" r="5" fill="{palette[index]}"/><text x="{x + 18}" y="{y}" fill="var(--body)" font-family="ui-sans-serif,system-ui,sans-serif" font-size="13">{escape(language)} <tspan fill="var(--muted)">{percent:.2f}%</tspan></text>')
    cursor += width

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="210" viewBox="0 0 640 210">
<style>
  :root {{ --card: #f6f8fa; --border: #d0d7de; --title: #8250df; --body: #24292f; --muted: #656d76; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --card: #21262d; --border: #30363d; --title: #f778ba; --body: #e6edf3; --muted: #b1bac4; }} }}
</style>
<rect x="10" y="10" width="620" height="190" rx="12" fill="var(--card)" stroke="var(--border)"/>
<text x="34" y="48" fill="var(--title)" font-family="ui-sans-serif,system-ui,sans-serif" font-size="22" font-weight="700">Most Used Languages</text>
<clipPath id="bar"><rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="10" rx="5"/></clipPath><g clip-path="url(#bar)">{''.join(segments)}</g>
{''.join(legend)}
</svg>'''
OUT.write_text(svg, encoding='utf-8')
print(f'Wrote {OUT}')
