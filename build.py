#!/usr/bin/env python3
"""
MATRIX COMPLETE ARCHIVE — Multilingual Build System
Generates dist/en/ and dist/ja/ from shared YAML data,
plus a root index.html that auto-redirects by browser language.
"""

import shutil
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# === PATHS ===
ROOT = Path(__file__).parent
DATA = ROOT / "data"
I18N = DATA / "i18n"
TEMPLATES = ROOT / "templates"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"

LANGS = ["ja", "en"]
DEFAULT_LANG = "ja"

# === LOAD ===
def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

works_data = load_yaml(DATA / "works.yaml")
timeline_data = load_yaml(DATA / "timeline.yaml")
characters_data = load_yaml(DATA / "characters.yaml")
cycles_data = load_yaml(DATA / "cycles.yaml")

works = works_data["works"]
eras = timeline_data["eras"]
events = timeline_data["events"]
characters = characters_data["characters"]
cycles = cycles_data["cycles"]

# Group events by era for the timeline page
era_events = {era["id"]: [] for era in eras}
for ev in events:
    eid = ev.get("era")
    if eid in era_events:
        era_events[eid].append(ev)

# === JINJA ===
env = Environment(
    loader=FileSystemLoader(str(TEMPLATES)),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)

# === HELPERS ===
def make_tr(lang):
    """Field translator: returns the value for the requested language,
    falling back to English if missing, then to raw value if not a dict."""
    def tr(field):
        if isinstance(field, dict):
            return field.get(lang) or field.get("en") or next(iter(field.values()), "")
        return field if field is not None else ""
    return tr

def make_label(lang, ui_strings, prefix):
    """Resolve a category label (medium/faction/type) from UI strings, fallback to raw key."""
    def lookup(key):
        return ui_strings.get(f"{prefix}_{key}", key)
    return lookup

# === BUILD ===
def clean_dist():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

def copy_assets():
    shutil.copytree(ASSETS, DIST / "assets")

def render_lang(lang):
    """Render all pages for a given language into dist/<lang>/."""
    ui = load_yaml(I18N / f"{lang}.yaml")
    tr = make_tr(lang)

    # Build a per-language work title lookup
    work_titles = {w["id"]: tr(w["title"]) for w in works}

    other = "en" if lang == "ja" else "ja"

    # Shared context for all pages of this language
    base_ctx = {
        "t": ui,
        "tr": tr,
        "work_titles": work_titles,
        "medium_label": make_label(lang, ui, "medium"),
        "faction_label": make_label(lang, ui, "faction"),
        "type_label": make_label(lang, ui, "type"),

        # Path roots
        "root": "",                # within the language directory
        "asset_root": "../assets/",
        "site_root": "../",
        "alt_root": f"../{other}/",   # other language same page
        "alt_lang": other,
        "alt_root_ja": "../ja/",
        "alt_root_en": "../en/",
    }

    pages = [
        ("index.html",      "Index",      "index"),
        ("timeline.html",   ui["nav_timeline"], "timeline"),
        ("cycles.html",     ui["nav_cycles"],   "cycles"),
        ("characters.html", ui["nav_characters"], "characters"),
        ("works.html",      ui["nav_works"],    "works"),
    ]

    out_dir = DIST / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    for tmpl, page_title, page in pages:
        ctx = dict(base_ctx)
        ctx.update({
            "page": page,
            "page_title": page_title,
            "page_filename": tmpl,
        })

        if tmpl == "index.html":
            visible_works = [w for w in works if not w.get("hidden")]
            tracked = [c for c in characters if c["type"] in ("human", "program", "machine")]
            ctx.update({
                "event_count": f"{len(events):03d}",
                "char_count":  f"{len(tracked):03d}",
                "work_count":  f"{len(visible_works):02d}",
            })

        if tmpl == "timeline.html":
            ctx.update({"eras": eras, "era_events": era_events})

        if tmpl == "cycles.html":
            ctx.update({"cycles": cycles})

        if tmpl == "characters.html":
            ctx.update({"characters": characters})

        if tmpl == "works.html":
            ctx.update({"works": works})

        html = env.get_template(tmpl).render(**ctx)
        (out_dir / tmpl).write_text(html, encoding="utf-8")
        print(f"  ✓ {lang}/{tmpl}")

def render_root_redirect():
    """The root index.html: auto-detects browser language and redirects."""
    html = env.get_template("root_lang_redirect.html").render()
    (DIST / "index.html").write_text(html, encoding="utf-8")
    print(f"  ✓ index.html (root redirect)")

def main():
    print("MATRIX ARCHIVE — Multilingual build")
    clean_dist()
    copy_assets()
    print("Generating pages:")
    for lang in LANGS:
        render_lang(lang)
    render_root_redirect()
    print(f"\nDone.")
    print(f"  Default language: {DEFAULT_LANG}")
    print(f"  Languages built:  {', '.join(LANGS)}")
    print(f"  Output:           {DIST}")
    total_pages = sum(1 for _ in DIST.rglob("*.html"))
    print(f"  Total pages:      {total_pages}")

if __name__ == "__main__":
    main()
