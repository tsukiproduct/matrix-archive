# MATRIX COMPLETE ARCHIVE (Bilingual)

An independent research archive of the Matrix canon.
Bilingual: Japanese (default) + English.
Static site generated from structured YAML data via Python + Jinja2.

## Quick start

```bash
pip install jinja2 pyyaml
python3 build.py
```

Output:
- `dist/index.html` — root landing (auto-redirects to user's language)
- `dist/ja/` — Japanese version (5 pages)
- `dist/en/` — English version (5 pages)

## Language behavior

1. **First visit**: browser language detected; English browsers go to `/en/`, everyone else to `/ja/`.
2. **User toggles**: clicking the EN/日本語 button saves the choice to `localStorage`.
3. **Return visit**: saved choice wins over browser language.

## Architecture

```
matrix-archive/
├── data/
│   ├── i18n/
│   │   ├── ja.yaml          ← UI strings (Japanese)
│   │   └── en.yaml          ← UI strings (English)
│   ├── works.yaml           ← Canon works, fields as {ja, en} dicts
│   ├── timeline.yaml        ← Events, multilingual
│   ├── characters.yaml      ← Characters, multilingual
│   └── cycles.yaml          ← Six cycles, multilingual
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── timeline.html
│   ├── cycles.html
│   ├── characters.html
│   ├── works.html
│   └── root_lang_redirect.html
├── assets/                  ← CSS, JS (shared across languages)
│   ├── css/matrix.css
│   └── js/  (code-rain.js, filters.js, lang.js)
├── build.py
└── dist/
    ├── index.html           ← root redirect
    ├── assets/
    ├── ja/                  ← 5 Japanese pages
    └── en/                  ← 5 English pages
```

## To add content

All canon data uses `{ja: "...", en: "..."}` dicts for any string that should
be translated. Numeric/ID fields stay plain.

### New event example
```yaml
- id: new_event_id
  era: cycle_6
  title:
    en: "Some English title"
    ja: "日本語のタイトル"
  description:
    en: "What happened, in English."
    ja: "起きたことの日本語説明。"
  sources: [reloaded]
```

Run `python3 build.py`. Both language sites regenerate.

### New UI string
Add the same key to both `data/i18n/en.yaml` and `data/i18n/ja.yaml`.
Reference in templates as `{{ t.your_key }}`.

## Typography

- **English**: JetBrains Mono (UI) + Cormorant Garamond (display serif)
- **Japanese**: JetBrains Mono (UI) + Noto Serif JP (display) + Noto Sans JP (body)

CSS applies the JP fonts automatically when `html[lang="ja"]`.

## Design principles

1. **No copyrighted material.** Every word is original prose.
   No images, no dialogue, no music, no footage from the films.
2. **Single source of truth.** All canon facts live in YAML.
   One file edit propagates to both language builds.
3. **Buildable.** Plain static HTML. Hostable anywhere.
4. **Accessible.** Respects `prefers-reduced-motion`, semantic HTML.
   Mobile-first.

## Legal posture

- Independent fan research project
- Non-commercial
- No reproduction of copyrighted assets
- Nominative use of names for scholarly commentary
- Footer disclaimer on every page in both languages

## Deploy to GitHub Pages

```bash
git init && git add . && git commit -m "Initial"
git remote add origin git@github.com:USER/REPO.git
git push -u origin main

# In repo settings → Pages → deploy from /dist
```

For `matrix.tsukilab.jp`:
1. Create `CNAME` file in `dist/` containing `matrix.tsukilab.jp`
2. Configure DNS at お名前.com (same flow as `signal.tsukilab.jp`)

## Stats (v1.1)

- 11 generated HTML pages (5 ja + 5 en + 1 root)
- 37 canonical events
- 16 characters tracked
- 6 cycles documented
- 9 works integrated
- ~232 KB total
