import os
import json
from core.translation_data import NATURES 

DATA_DIR = "data/users"

DEFAULT_USER = {
    "pokeballs": {"pokeball": 10, "superball": 5, "hyperball": 2, "masterball": 0},
    "items": {"chroma": 0, "multi_exp": 0},
    "money": 500,
    "box": [],
    "daily_claimed": None
}

def update_or_merge_pokemon(data, new_pkm):
    """Empile les IVs, natures, et talent caché sur un Pokémon principal de même espèce, sinon l'ajoute."""
    box = data.get("box", [])
    name = new_pkm["name"]

    # Cherche s’il existe un Pokémon locké avec le même nom
    for existing in box:
        if existing.get("locked") and existing["name"] == name:
            main = existing
            break
    else:
        # Aucun Pokémon principal, on le crée
        new_pkm["locked"] = True
        new_pkm["known_natures"] = [new_pkm["nature"]]
        new_pkm["quantity"] = 1
        box.append(new_pkm)
        data["box"] = box
        return

    # Stack IV
    for stat in new_pkm["ivs"]:
        if new_pkm["ivs"][stat] > main["ivs"].get(stat, 0):
            main["ivs"][stat] = new_pkm["ivs"][stat]

    # Stack talent caché
    if new_pkm["ability"] == new_pkm.get("hidden_ability") and main.get("ability") != main.get("hidden_ability"):
        main["ability"] = new_pkm["ability"]

    # Stack nature
    if "known_natures" not in main:
        main["known_natures"] = [main["nature"]]
    if new_pkm["nature"] not in main["known_natures"]:
        main["known_natures"].append(new_pkm["nature"])

    main["quantity"] += 1
    data["box"] = box

def update_or_merge_pokemon_with_feedback(data, new_pkm, lang):
    """Version avec retour utilisateur pour annoncer les stack d’IVs, talents et natures."""
    messages = []
    box = data.get("box", [])
    name = new_pkm["name"]

    for existing in box:
        if existing.get("locked") and existing["name"] == name:
            main = existing
            break
    else:
        new_pkm["locked"] = True
        new_pkm["known_natures"] = [new_pkm["nature"]]
        new_pkm["quantity"] = 1
        box.append(new_pkm)
        data["box"] = box
        return []

    for stat in new_pkm["ivs"]:
        if new_pkm["ivs"][stat] > main["ivs"].get(stat, 0):
            main["ivs"][stat] = new_pkm["ivs"][stat]
            messages.append(f"🧬 IV {stat} stacké !")

    if new_pkm["ability"] == new_pkm.get("hidden_ability") and main.get("ability") != main.get("hidden_ability"):
        main["ability"] = new_pkm["ability"]
        messages.append("✨ Talent caché stacké !")

    if "known_natures" not in main:
        main["known_natures"] = [main["nature"]]
    if new_pkm["nature"] not in main["known_natures"]:
        main["known_natures"].append(new_pkm["nature"])
        localized_nature = NATURES.get(new_pkm['nature'], {}).get(lang, new_pkm['nature'])
        messages.append(f"🍃 Nouvelle nature connue : {localized_nature}")

    main["quantity"] += 1
    data["box"] = box
    return messages

def get_user_file(user_id: int):
    return os.path.join(DATA_DIR, f"{user_id}.json")

def load_user(user_id: int):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    path = get_user_file(user_id)
    if not os.path.isfile(path):
        with open(path, "w") as f:
            json.dump(DEFAULT_USER, f, indent=2)
        return DEFAULT_USER.copy()
    with open(path, "r") as f:
        return json.load(f)

def save_user(user_id: int, data: dict):
    path = get_user_file(user_id)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)