from pathlib import Path
from datetime import date, timedelta
import json
import math

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'leetcode.json'
OUT = ROOT / 'leetcode-heatmap.svg'

W, H = 920, 275
CELL, GAP = 12, 5
LEFT, TOP = 54, 68
COLS, ROWS = 53, 7
PALETTE = ['#eef0f2', '#d7eadb', '#a8d5b0', '#62b66d', '#24963f', '#087f2f']

payload = json.loads(DATA.read_text(encoding='utf-8'))
days = {x['date']: x['count'] for x in payload.get('days', [])}
values = list(days.values())
max_count = max(values) if values else 1

# Build a rolling 53-week calendar ending today, Sunday-aligned.
today = date.today()
start = today - timedelta(days=364)
start -= timedelta(days=(start.weekday() + 1) % 7)  # Sunday

def level(count):
    if count <= 0: return 0
    # Log-ish buckets make sparse submission histories readable.
    ratio = math.log1p(count) / math.log1p(max_count)
    return min(5, max(1, math.ceil(ratio * 5)))

out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" rx="18" fill="#f7f8f9" stroke="#d8dde2"/>
<text x="28" y="35" fill="#1f252b" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="17" font-weight="700">LEETCODE ACTIVITY</text>
<text x="28" y="54" fill="#7b8289" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11">submission heatmap · last 365 days</text>''']

# Month labels from the first day represented by each column.
seen_months = set()
for c in range(COLS):
    d = start + timedelta(days=c*7)
    if d.month not in seen_months:
        seen_months.add(d.month)
        out.append(f'<text x="{LEFT+c*(CELL+GAP)}" y="84" fill="#8a9198" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10">{d.strftime("%b")}</text>')

# Heatmap cells. Each column is one week; each row is Sunday..Saturday.
for c in range(COLS):
    for r in range(ROWS):
        d = start + timedelta(days=c*7+r)
        count = days.get(d.isoformat(), 0)
        fill = PALETTE[level(count)]
        x = LEFT + c*(CELL+GAP)
        y = TOP + r*(CELL+GAP)
        delay = (c + r) * 0.018
        out.append(f'''<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{fill}" opacity="1" transform="translate(0,0)">
  <animate attributeName="opacity" from="0" to="1" dur="0.24s" begin="{delay:.3f}s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="-8,-8" to="0,0" dur="0.24s" begin="{delay:.3f}s" fill="freeze"/>
</rect>''')

stats = payload.get('stats', {})
out.append(f'''<text x="28" y="218" fill="#343b42" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12"><tspan font-weight="700">{stats.get('submissions', 0)}</tspan> submissions</text>
<text x="190" y="218" fill="#343b42" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12"><tspan font-weight="700">{stats.get('active_days', 0)}</tspan> active days</text>
<text x="330" y="218" fill="#343b42" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12"><tspan font-weight="700">{stats.get('streak', 0)}</tspan> day streak</text>
<text x="28" y="244" fill="#8a9198" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10">Less</text>''')

for i, color in enumerate(PALETTE):
    x = 66 + i*18
    out.append(f'<rect x="{x}" y="236" width="12" height="12" rx="3" fill="{color}"/>')
out.append('''<text x="186" y="244" fill="#8a9198" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10">More</text>
<text x="830" y="244" fill="#8a9198" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10">Adarsh_jai12</text>
</svg>''')

OUT.write_text('\n'.join(out), encoding='utf-8')
print(f'Wrote {OUT}')
