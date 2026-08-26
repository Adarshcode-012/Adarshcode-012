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
<rect width="100%" height="100%" rx="18" fill="#f7f8f9" stroke="#d8dde2"/>
<rect x="1" y="1" width="488" height="48" rx="17" fill="#ffffff"/>
<circle cx="22" cy="25" r="5" fill="#c8cdd2"/><circle cx="40" cy="25" r="5" fill="#c8cdd2"/><circle cx="58" cy="25" r="5" fill="#c8cdd2"/>
<text x="82" y="30" fill="#7b8289" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13">Adarshcode-012@github</text>
<text x="24" y="88" fill="#1f252b" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="23" font-weight="700">$ whoami</text>
<line x1="24" y1="104" x2="466" y2="104" stroke="#e0e4e8"/>''']

for i, (key, value) in enumerate(lines):
    y = 140 + i * 43
    delay = i * 0.16
    out.append(f'''<g opacity="1" transform="translate(0 0)">
  <animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{delay:.2f}s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="-10 0" to="0 0" dur="0.35s" begin="{delay:.2f}s" fill="freeze"/>
  <text x="24" y="{y}" fill="#8a9198" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11">{key.upper()}</text>
  <text x="24" y="{y+19}" fill="#343b42" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13">{value}</text>
</g>''')

out.append('</svg>')
OUT.write_text('\n'.join(out), encoding='utf-8')
print(f'Wrote {OUT}')
