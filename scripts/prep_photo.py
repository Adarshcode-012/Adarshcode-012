from pathlib import Path
import sys
import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'assets' / 'source-photo.png'
OUT = ROOT / 'assets' / 'source-prepped.png'

img = cv2.imread(str(SRC), cv2.IMREAD_COLOR)
if img is None:
    raise SystemExit(f'Could not read {SRC}')

# The supplied portrait already has a very light, nearly uniform background.
# Keep the subject while making the background pure white and increasing local contrast.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
contrast = clahe.apply(gray)

# Detect the pale background from saturation + brightness. Preserve darker subject pixels.
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
background = (hsv[:, :, 1] < 45) & (hsv[:, :, 2] > 205)
processed = contrast.copy()
processed[background] = 255

# Mild blur avoids harsh JPEG/phone-photo noise in the ASCII conversion.
processed = cv2.GaussianBlur(processed, (3, 3), 0)
# Crop away the large blank margin so the ASCII portrait uses the available width.
mask = processed < 235
ys, xs = np.where(mask)
if len(xs):
    pad_x, pad_y = 18, 18
    x0, x1 = max(0, xs.min()-pad_x), min(processed.shape[1], xs.max()+pad_x+1)
    y0, y1 = max(0, ys.min()-pad_y), min(processed.shape[0], ys.max()+pad_y+1)
    processed = processed[y0:y1, x0:x1]
Image.fromarray(processed).save(OUT)
print(f'Wrote {OUT}')
