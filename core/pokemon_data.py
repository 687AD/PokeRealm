import random
import os
import json

# Chemin vers ton fichier JSON (modifie si besoin)
TALENTS_PATH = os.path.join("data", "pokemon_talents.json")

if os.path.exists(TALENTS_PATH):
    with open(TALENTS_PATH, "r", encoding="utf-8") as f:
        POKEMON_TALENTS = json.load(f)
else:
    POKEMON_TALENTS = {}

from core.translation_data import NATURES
from core.translation_data import POKEMON_NAMES
from core.moves import get_move



def generate_pokemon(name: str, rarity: str, chroma_bonus: int = 0):
    forced_shiny = name.startswith("shiny_")
    base_name = name.replace("shiny_", "")

    from core.translation_data import POKEMON_NAMES
    for eng, names in POKEMON_NAMES.items():
        if base_name == names.get("fr") or base_name == names.get("en"):
            base_name = eng
            break
    
    shiny_chance = 1 / 4096 + (chroma_bonus * 0.05)
    shiny = forced_shiny or (random.random() < shiny_chance)

    if shiny:
        ivs = {stat: 31 for stat in ["hp", "atk", "def", "spa", "spd", "spe"]}
    else:
        ivs = {stat: random.randint(0, 31) for stat in ["hp", "atk", "def", "spa", "spd", "spe"]}

    nature = random.choice(list(NATURES))

    # Récupération des talents
    talents = POKEMON_TALENTS.get(base_name, {})
    normal_abilities = talents.get("normal", [])
    hidden_ability = talents.get("hidden")

    # Par défaut on met Aucun si aucune data trouvée
    ability = "Aucun"

    if hidden_ability and random.random() < 0.02:
        ability = hidden_ability
    elif normal_abilities:
        ability = random.choice(normal_abilities)


    return {
        "name": name,
        "rarity": rarity,
        "shiny": shiny,
        "ivs": ivs,
        "nature": nature,
        "ability": ability,
        "hidden_ability": hidden_ability,
        "level": 1,
        "quantity": 1
    }

def get_pokemon_stats_and_moves(pkm):
    # Si le Pokémon a déjà ses stats enregistrées, on les utilise
    stats = pkm.get("stats", {
        "hp": 100,
        "attack": 50,
        "defense": 50,
        "speed": 50,
    })

    # Construction des attaques avec PP depuis ton moves.json
    moves = []
    for move_name in pkm.get("moves", []):
        move_data = get_move(move_name)
        if move_data:
            moves.append({
                "name": move_data["name"],
                "power": move_data["power"],
                "pp": move_data["pp"]
            })

    return stats, moves
