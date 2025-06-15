import os
import json
from core.translation_data import NATURES
from core.lang import get_text, get_ability_name


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

    for existing in box:
        if existing.get("locked") and existing["name"] == name:
            main = existing
            break
    else:
        new_pkm["locked"] = True
        new_pkm["known_natures"] = [new_pkm["nature"]]
        new_pkm["known_abilities"] = [new_pkm["ability"]]
        new_pkm["quantity"] = 1
        box.append(new_pkm)
        data["box"] = box
        return

    for stat in new_pkm["ivs"]:
        if new_pkm["ivs"][stat] > main["ivs"].get(stat, 0):
            main["ivs"][stat] = new_pkm["ivs"][stat]

    if "known_natures" not in main:
        main["known_natures"] = [main["nature"]]
    if new_pkm["nature"] not in main["known_natures"]:
        main["known_natures"].append(new_pkm["nature"])

    main.setdefault("known_abilities", [])
    ability = new_pkm["ability"]
    hidden_ability = new_pkm.get("hidden_ability")
    if ability not in main["known_abilities"]:
        main["known_abilities"].append(ability)
    if ability == ability and main.get("ability") != hidden_ability:
        main["ability"] = hidden_ability

    main["quantity"] += 1
    data["box"] = box

def sync_with_sibling(box, pkm):
    name = pkm["name"]
    # Trouve l’autre version dans la box
    if name.startswith("shiny_"):
        sibling_name = name[len("shiny_"):]
    else:
        sibling_name = "shiny_" + name

    sibling = next((poke for poke in box if poke["name"] == sibling_name), None)
    if sibling:
        for field in ["known_natures", "known_abilities"]:
            known_self = set(pkm.get(field, []))
            known_sibling = set(sibling.get(field, []))
            merged = list(known_self | known_sibling)
            pkm[field] = merged
            sibling[field] = merged

def update_or_merge_pokemon_with_feedback(data, new_pkm, lang):
    # Synchronise avant tout si stack ou fusion
    sync_with_sibling(data["box"], new_pkm)
    messages = []
    box = data.get("box", [])
    name = new_pkm["name"]

    for existing in box:
        if existing.get("locked") and existing["name"] == name:
            main = existing
            break
    else:
        # Nouveau Pokémon : initialisation
        new_pkm["locked"] = True
        new_pkm["known_natures"] = [new_pkm["nature"]]
        new_pkm["known_abilities"] = [new_pkm["ability"]]
        new_pkm["quantity"] = 1
        box.append(new_pkm)
        data["box"] = box
        # Synchronisation rétroactive tout de suite après ajout à la box !
        sync_with_sibling(box, new_pkm)
        return []

    # Stack IVs
    for stat in new_pkm["ivs"]:
        if new_pkm["ivs"][stat] > main["ivs"].get(stat, 0):
            main["ivs"][stat] = new_pkm["ivs"][stat]
            messages.append(f"🧬 IV {stat} stacké !")

    # Stack natures
    if "known_natures" not in main:
        main["known_natures"] = [main["nature"]]
    if new_pkm["nature"] not in main["known_natures"]:
        main["known_natures"].append(new_pkm["nature"])
        localized_nature = NATURES.get(new_pkm['nature'], {}).get(lang, new_pkm['nature'])
        messages.append(f"🍃 Nouvelle nature connue : {localized_nature}")

    # Stack abilities
    main.setdefault("known_abilities", [])
    ability = new_pkm["ability"]
    hidden_ability = new_pkm.get("hidden_ability")

    if ability not in main["known_abilities"]:
        main["known_abilities"].append(ability)
        # On récupère le nom traduit
        ability_txt = get_ability_name(ability, lang)
        if ability == hidden_ability:
            messages.append(f"👻 Nouveau talent caché trouvé : {ability_txt} !")
        else:
            messages.append(f"🎯 Nouveau talent trouvé : {ability_txt} !")

    if ability == hidden_ability and main.get("ability") != hidden_ability:
        main["ability"] = hidden_ability

    main["quantity"] += 1
    data["box"] = box
    # Synchronise après stack, au cas où on ait enrichi la liste
    sync_with_sibling(box, main)
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
        data = json.load(f)
    # C’est ICI qu’il faut mettre le patch :
    if "balls_used" not in data:
        data["balls_used"] = {"pokeball": 0, "superball": 0, "hyperball": 0, "masterball": 0}
    return data


def save_user(user_id: int, data: dict):
    path = get_user_file(user_id)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    
def get_and_update_user(user_id: int, username: str = None):
    """Charge les données et met à jour le username si besoin."""
    data = load_user(user_id)

    if username:
        current = data.get("username", "").lower()
        new_username = username.lower()
        if new_username != current:
            data["username"] = new_username
            save_user(user_id, data)

    return data
