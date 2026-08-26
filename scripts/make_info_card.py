from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'info-card.svg'
STATIC = False

W, H = 490, 520
lines = [
    ('role', 'Computer Science (AI-ML) — Final Year'),
    ('focus', 'DSA + Full Stack + AI'),
    ('languages', 'C++  ·  Python  ·  JavaScript  ·  SQL'),
    ('web', 'React  ·  Next.js  ·  Node.js  ·  REST APIs'),
    ('data', 'MySQL  ·  PostgreSQL  ·  SQL Server'),
    ('ai', 'NLP  ·  ML  ·  Deep Learning  ·  GenAI'),
    ('orchestration', 'CrewAI  ·  Tool Calling  ·  LLM Validation'),
    ('projects', 'PolishCV  ·  ActivityHub  ·  Voice Shopping'),
]

out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  :root {{
    --card-stroke: #d0d7de;
    --chrome-fill: #ffffff;
    --chrome-dot: #afb8c1;
    --title: #1f2328;
    --label: #656d76;
    --body: #24292f;
    --line: #d8dee4;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --card-stroke: #30363d;
      --chrome-fill: #161b22;
      --chrome-dot: #6e7681;
      --title: #f0f6fc;
      --label: #8b949e;
      --body: #c9d1d9;
      --line: #30363d;
    }}
  }}
</style>
<rect x="10" y="10" width="470" height="500" rx="18" fill="none" stroke="var(--card-stroke)"/>
<rect x="11" y="11" width="468" height="48" rx="17" fill="var(--chrome-fill)"/>
<circle cx="32" cy="35" r="5" fill="var(--chrome-dot)"/><circle cx="50" cy="35" r="5" fill="var(--chrome-dot)"/><circle cx="68" cy="35" r="5" fill="var(--chrome-dot)"/>
<text x="92" y="40" fill="var(--label)" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13">Adarshcode-012@github</text>
<text x="24" y="98" fill="var(--title)" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="23" font-weight="700">$ whoami</text>
<line x1="24" y1="114" x2="466" y2="114" stroke="var(--line)"/>''']

for i, (key, value) in enumerate(lines):
    y = 140 + i * 43
    delay = i * 0.16
    out.append(f'''<g opacity="1" transform="translate(0 0)">
  <animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{delay:.2f}s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="-10 0" to="0 0" dur="0.35s" begin="{delay:.2f}s" fill="freeze"/>
  <text x="24" y="{y}" fill="var(--label)" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11">{key.upper()}</text>
  <text x="24" y="{y+19}" fill="var(--body)" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13">{value}</text>
</g>''')

out.append('</svg>')
OUT.write_text('\n'.join(out), encoding='utf-8')
print(f'Wrote {OUT}')
