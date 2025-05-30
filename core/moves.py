import json
import os

MOVES_PATH = "data/moves.json"

if os.path.exists(MOVES_PATH):
    with open(MOVES_PATH, "r", encoding="utf-8") as f:
        MOVES = json.load(f)
else:
    MOVES = []

def get_move(name: str) -> dict | None:
    """Retourne l’attaque par nom (case insensitive)."""
    name = name.lower()
    for move in MOVES:
        if move["name"].lower() == name:
            return move
    return None

def pokemon_has_move(pokemon: dict, move_name: str) -> bool:
    """Vérifie si le Pokémon possède cette attaque (par nom)."""
    return move_name in pokemon.get("moves", [])

def use_move(pokemon: dict, move_name: str) -> dict | None:
    """
    Renvoie l’objet move (infos attaque) si le Pokémon possède cette attaque.
    Sinon, renvoie None.
    """
    if pokemon_has_move(pokemon, move_name):
        return get_move(move_name)
    return None

def list_moves() -> list:
    """Retourne la liste complète des attaques."""
    return MOVES
