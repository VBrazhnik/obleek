#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "template.html"
CONTENT_DIR = ROOT / "content"

LANGUAGES = {
    "en": {"out": "index.html", "url": "https://vbrazhnik.github.io/obleek/", "og_locale": "en_US", "asset_base": ""},
    "cs": {"out": "cs/index.html", "url": "https://vbrazhnik.github.io/obleek/cs/", "og_locale": "cs_CZ", "asset_base": "../"},
    "de": {"out": "de/index.html", "url": "https://vbrazhnik.github.io/obleek/de/", "og_locale": "de_DE", "asset_base": "../"},
    "es": {"out": "es/index.html", "url": "https://vbrazhnik.github.io/obleek/es/", "og_locale": "es_ES", "asset_base": "../"},
    "fr": {"out": "fr/index.html", "url": "https://vbrazhnik.github.io/obleek/fr/", "og_locale": "fr_FR", "asset_base": "../"},
    "it": {"out": "it/index.html", "url": "https://vbrazhnik.github.io/obleek/it/", "og_locale": "it_IT", "asset_base": "../"},
    "pl": {"out": "pl/index.html", "url": "https://vbrazhnik.github.io/obleek/pl/", "og_locale": "pl_PL", "asset_base": "../"},
    "pt": {"out": "pt/index.html", "url": "https://vbrazhnik.github.io/obleek/pt/", "og_locale": "pt_PT", "asset_base": "../"},
    "uk": {"out": "uk/index.html", "url": "https://vbrazhnik.github.io/obleek/uk/", "og_locale": "uk_UA", "asset_base": "../"},
}


def hreflang_block():
    lines = []
    for lang, cfg in LANGUAGES.items():
        lines.append(f'<link rel="alternate" hreflang="{lang}" href="{cfg["url"]}" />')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{LANGUAGES["en"]["url"]}" />')
    return "\n".join(lines)


def build(lang, cfg):
    strings = json.loads((CONTENT_DIR / f"{lang}.json").read_text(encoding="utf-8"))
    strings.setdefault("canonical_url", cfg["url"])
    strings.setdefault("og_locale", cfg["og_locale"])
    strings.setdefault("asset_base", cfg["asset_base"])

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("{{hreflang_links}}", hreflang_block())

    def sub(match):
        key = match.group(1)
        if key not in strings:
            raise KeyError(f"{lang}.json is missing key '{key}' used in template.html")
        return strings[key]

    html = re.sub(r"\{\{(\w+)\}\}", sub, html)

    out_path = ROOT / cfg["out"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"wrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    for lang, cfg in LANGUAGES.items():
        build(lang, cfg)
