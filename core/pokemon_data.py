import random
from core.translation_data import NATURES

POKEMON_TALENTS = {
    "Bulbasaur":    {"normal": ["Engrais"], "hidden": "Chlorophylle"},
    "Ivysaur":      {"normal": ["Engrais"], "hidden": "Chlorophylle"},
    "Venusaur":     {"normal": ["Engrais"], "hidden": "Chlorophylle"},
    "Charmander":   {"normal": ["Brasier"], "hidden": "Force Soleil"},
    "Charmeleon":   {"normal": ["Brasier"], "hidden": "Force Soleil"},
    "Charizard":    {"normal": ["Brasier"], "hidden": "Force Soleil"},
    "Squirtle":     {"normal": ["Torrent"], "hidden": "Cuvette"},
    "Wartortle":    {"normal": ["Torrent"], "hidden": "Cuvette"},
    "Blastoise":    {"normal": ["Torrent"], "hidden": "Cuvette"},
    "Caterpie":     {"normal": ["Écran Poudre"], "hidden": "Fuite"},
    "Metapod":      {"normal": ["Mue"], "hidden": "Fuite"},
    "Butterfree":   {"normal": ["Œil Composé"], "hidden": "Lentiteintée"},
    "Weedle":       {"normal": ["Écran Poudre"], "hidden": "Fuite"},
    "Kakuna":       {"normal": ["Mue"], "hidden": "Fuite"},
    "Beedrill":     {"normal": ["Essaim"], "hidden": "Sniper"},
    "Pidgey":       {"normal": ["Regard Vif", "Téméraire"], "hidden": "Cœur de Coq"},
    "Pidgeotto":    {"normal": ["Regard Vif", "Téméraire"], "hidden": "Cœur de Coq"},
    "Pidgeot":      {"normal": ["Regard Vif", "Téméraire"], "hidden": "Cœur de Coq"},
    "Rattata":      {"normal": ["Fuite", "Agitation"], "hidden": "Cran"},
    "Raticate":     {"normal": ["Fuite", "Agitation"], "hidden": "Cran"},
}

def generate_iv():
    return {stat: random.randint(0, 31) for stat in ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]}

def generate_pokemon(name: str, rarity: str, chroma_bonus: int = 0):
    shiny_chance = 1 / 4096 + (chroma_bonus * 0.01)
    shiny = random.random() < shiny_chance

    ivs = {
        "hp": random.randint(0, 31),
        "atk": random.randint(0, 31),
        "def": random.randint(0, 31),
        "spa": random.randint(0, 31),
        "spd": random.randint(0, 31),
        "spe": random.randint(0, 31),
    }

    nature = random.choice(list(NATURES))
    talents = POKEMON_TALENTS.get(name, {})
    hidden_chance = random.random() < (1 / 1000)

    if hidden_chance and "hidden" in talents:
        ability = talents["hidden"]
    else:
        ability = random.choice(talents.get("normal", ["Aucun"]))

    return {
        "name": name,
        "rarity": rarity,
        "shiny": shiny,
        "ivs": ivs,
        "nature": nature,
        "ability": ability,
        "level": 1,
        "quantity": 1
    }

