from pathlib import Path
from datetime import date, timedelta
import json
import math

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'leetcode.json'
OUT = ROOT / 'leetcode-heatmap.svg'

W, H = 920, 286
CELL, GAP = 11, 5
LEFT, TOP = 36, 102
COLS, ROWS = 53, 7
STEP = CELL + GAP
PALETTE = ['var(--cell0)', 'var(--cell1)', 'var(--cell2)', 'var(--cell3)', 'var(--cell4)', 'var(--cell5)']

payload = json.loads(DATA.read_text(encoding='utf-8'))
days = {item['date']: item['count'] for item in payload.get('days', [])}
max_count = max(days.values(), default=1)
stats = payload.get('stats', {})

today = date.today()
start = today - timedelta(days=364)
start -= timedelta(days=(start.weekday() + 1) % 7)  # Sunday-aligned columns

def level(count):
    if count <= 0:
        return 0
    return min(5, max(1, math.ceil(math.log1p(count) / math.log1p(max_count) * 5)))

out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  :root {{ --card: #f6f8fa; --border: #d0d7de; --title: #1f2328; --body: #24292f; --muted: #656d76; --cell0: #ebedf0; --cell1: #9be9a8; --cell2: #40c463; --cell3: #30a14e; --cell4: #216e39; --cell5: #0e4429; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --card: #21262d; --border: #30363d; --title: #f0f6fc; --body: #c9d1d9; --muted: #8b949e; --cell0: #30363d; --cell1: #0e4429; --cell2: #006d32; --cell3: #26a641; --cell4: #39d353; --cell5: #7ee787; }} }}
</style>
<rect x="10" y="10" width="900" height="266" rx="14" fill="var(--card)" stroke="var(--border)"/>
<text x="36" y="38" fill="var(--muted)" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11" font-weight="700">LEETCODE ACTIVITY</text>
<text x="36" y="72" fill="var(--body)" font-family="ui-sans-serif,system-ui,sans-serif" font-size="16"><tspan font-size="25" font-weight="700">{stats.get('submissions', 0)}</tspan> submissions in the past year</text>
<text x="625" y="65" fill="var(--muted)" font-family="ui-sans-serif,system-ui,sans-serif" font-size="12">Total active days: <tspan fill="var(--body)" font-weight="700">{stats.get('active_days', 0)}</tspan></text>
<text x="760" y="65" fill="var(--muted)" font-family="ui-sans-serif,system-ui,sans-serif" font-size="12">Current streak: <tspan fill="var(--body)" font-weight="700">{stats.get('streak', 0)}</tspan></text>''']

# Month labels sit below the grid, as on LeetCode. Skip a label only when a
# partial opening month would make neighbouring labels collide.
last_month = None
last_label_col = -3
month_labels = []
for c in range(COLS):
    column_date = start + timedelta(days=c * 7)
    if column_date.month != last_month:
        last_month = column_date.month
        if c - last_label_col >= 3:
            last_label_col = c
            month_labels.append((c, column_date.strftime('%b')))

for c in range(COLS):
    for r in range(ROWS):
        current = start + timedelta(days=c * 7 + r)
        x, y = LEFT + c * STEP, TOP + r * STEP
        out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[level(days.get(current.isoformat(), 0))]}"/>')

for c, label in month_labels:
    x = LEFT + c * STEP + CELL / 2
    out.append(f'<text x="{x}" y="{TOP + ROWS * STEP + 15}" text-anchor="middle" fill="var(--muted)" font-family="ui-sans-serif,system-ui,sans-serif" font-size="11">{label}</text>')

legend_y = 253
out.append(f'<text x="36" y="{legend_y + 9}" fill="var(--muted)" font-family="ui-sans-serif,system-ui,sans-serif" font-size="10">Less</text>')
for i, colour in enumerate(PALETTE):
    out.append(f'<rect x="{70 + i * 17}" y="{legend_y}" width="11" height="11" rx="2" fill="{colour}"/>')
out.append(f'''<text x="177" y="{legend_y + 9}" fill="var(--muted)" font-family="ui-sans-serif,system-ui,sans-serif" font-size="10">More</text>
<text x="884" y="{legend_y + 9}" text-anchor="end" fill="var(--muted)" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10">{payload.get('username', 'Adarsh_jai12')}</text>
</svg>''')

OUT.write_text('\n'.join(out), encoding='utf-8')
print(f'Wrote {OUT}')
