import json
import os

LANGS = {}

for lang_code in ["fr", "en"]:
    path = os.path.join(os.path.dirname(__file__), lang_code + ".json")
    with open(path, "r", encoding="utf-8") as f:
        LANGS[lang_code] = json.load(f)

def get_text(key, lang="fr", **kwargs):
    text = LANGS.get(lang, {}).get(key, key)
    return text.format(**kwargs)
