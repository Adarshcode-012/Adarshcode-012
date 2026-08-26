# Setup

## 1. Create the profile repository

The repository name must exactly match the GitHub username:

`Adarshcode-012/Adarshcode-012`

Create it as a public repository. Do not initialize it with another README if you are going to push this folder as-is.

## 2. Install locally

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r scripts/requirements.txt
```

## 3. Regenerate the portrait

```bash
python scripts/prep_photo.py
python scripts/make_ascii_svg.py
python scripts/make_info_card.py
```

## 4. Fetch your real LeetCode data

```bash
python scripts/fetch_leetcode.py
python scripts/render_leetcode_heatmap.py
```

The fetcher uses the public LeetCode GraphQL `userProfileCalendar` query and does not require a LeetCode password or token.

## 5. Preview

Open `README.md` through GitHub after pushing. SVG SMIL animations are intentionally embedded in the SVG files rather than the README.

## 6. Push

```bash
git init
git branch -M main
git add .
git commit -m "feat: animated developer profile"
git remote add origin https://github.com/Adarshcode-012/Adarshcode-012.git
git push -u origin main
```

## 7. Enable the daily refresh

After the first push, open **Actions → Update profile art → Run workflow** once. The scheduled workflow then refreshes the LeetCode JSON and SVG every day.
