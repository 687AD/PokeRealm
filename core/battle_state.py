import random
from core.user_data import load_user
from core.pokemon_data import get_pokemon_stats_and_moves  # à créer pour extraire stats et attaques

active_battles = {}  # key: user_id, value: battle_state

def init_team_state(team):
    team_state = []
    for pkm in team:
        stats, moves = get_pokemon_stats_and_moves(pkm)
        team_state.append({
            "name": pkm["name"],
            "level": pkm.get("level", 50),
            "current_hp": stats["hp"],
            "max_hp": stats["hp"],
            "stats": stats,
            "moves": [{"name": m["name"], "power": m["power"], "pp": m["pp"]} for m in moves],
            "current_pokemon": False,
            "status": None,
            "fainted": False,
        })
    return team_state

async def create_battle_state(context, player1_id, player2_id):
    user1_data = load_user(player1_id)
    user2_data = load_user(player2_id)

    team1 = init_team_state(user1_data.get("team", []))
    team2 = init_team_state(user2_data.get("team", []))

    if not team1 or not team2:
        return  # Évite les combats vides

    # Définit le premier Pokémon actif
    team1[0]["current_pokemon"] = True
    team2[0]["current_pokemon"] = True

    state = {
        "players": {
            player1_id: {"team": team1, "turn_done": False},
            player2_id: {"team": team2, "turn_done": False}
        },
        "turn_order": [player1_id, player2_id] if random.random() < 0.5 else [player2_id, player1_id],
        "current_turn": 0,
        "log": [],
        "waiting_for_move": True
    }

    # Enregistre le combat pour les deux joueurs
    active_battles[player1_id] = state
    active_battles[player2_id] = state

    # Annonce début du combat
    await context.bot.send_message(chat_id=player1_id, text="🔥 Le combat commence ! Choisis une attaque.")
    await context.bot.send_message(chat_id=player2_id, text="🔥 Le combat commence ! Choisis une attaque.")

    # Ici on appelle une fonction pour envoyer les choix d’attaque
    from core.battle_engine import prompt_attack_choice
    await prompt_attack_choice(context, player1_id)
    await prompt_attack_choice(context, player2_id)
