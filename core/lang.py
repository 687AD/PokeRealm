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

def get_ability_name(ability_key, lang="fr"):
    if not ability_key or ability_key == "Aucun":
        return "Aucun" if lang == "fr" else "None"
    from core.translation_data import ABILITIES 
    return ABILITIES.get(ability_key, {}).get(lang, ability_key)

