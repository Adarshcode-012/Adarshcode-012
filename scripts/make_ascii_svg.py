from pathlib import Path
import cv2
import html
import math

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'assets' / 'source-prepped.png'
OUT = ROOT / 'avi-ascii.svg'

RAMP = " .`:-=+*cs#%@"
COLS = 58
ROWS = 42
CELL_W = 6.3
CELL_H = 9.0
WIDTH = int(COLS * CELL_W)
HEIGHT = int(ROWS * CELL_H)

img = cv2.imread(str(SRC), cv2.IMREAD_GRAYSCALE)
if img is None:
    raise SystemExit(f'Missing {SRC}. Run prep_photo.py first.')

# Correct for character aspect ratio: terminal glyphs are taller than wide.
target_h = int(img.shape[0] * COLS / img.shape[1] * 0.55)
target_h = min(max(target_h, 30), ROWS)
small = cv2.resize(img, (COLS, target_h), interpolation=cv2.INTER_AREA)
canvas = 255 * __import__('numpy').ones((ROWS, COLS), dtype='uint8')
off = (ROWS - target_h) // 2
canvas[off:off + target_h] = small

rows = []
for r in range(ROWS):
    chars = []
    for c in range(COLS):
        v = int(canvas[r, c])
        idx = round((255 - v) / 255 * (len(RAMP) - 1))
        chars.append(RAMP[idx])
    rows.append(''.join(chars).rstrip())

parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<rect width="100%" height="100%" fill="#ffffff"/>
<g fill="#555b61" font-family="ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace" font-size="8" xml:space="preserve">''']

for r, text in enumerate(rows):
    y = (r + 1) * CELL_H - 2
    delay = r * 0.055
    dur = 0.42
    escaped = html.escape(text)
    # Clip wipe + cursor-like edge. SMIL is self-contained in the SVG.
    parts.append(f'''<clipPath id="clip{r}"><rect x="0" y="{r*CELL_H}" width="{WIDTH}" height="{CELL_H + 2}">
  <animate attributeName="width" from="0" to="{WIDTH}" dur="{dur}s" begin="{delay:.3f}s" fill="freeze"/>
</rect></clipPath>
<text x="0" y="{y:.1f}" clip-path="url(#clip{r})">{escaped}</text>
<rect x="0" y="{r*CELL_H}" width="2" height="{CELL_H + 2}" fill="#9aa0a6" opacity="0">
  <animate attributeName="x" from="0" to="{WIDTH-2}" dur="{dur}s" begin="{delay:.3f}s" fill="freeze"/>
  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.92;1" dur="{dur}s" begin="{delay:.3f}s" fill="freeze"/>
</rect>''')

parts.append('</g></svg>')
OUT.write_text('\n'.join(parts), encoding='utf-8')
print(f'Wrote {OUT}')
