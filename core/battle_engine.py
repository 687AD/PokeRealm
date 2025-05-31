from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from core.battle_state import active_battles
import random

def get_active_pokemon(team):
    for pkm in team:
        if pkm["current_pokemon"] and not pkm["fainted"]:
            return pkm
    return None

async def prompt_attack_choice(context, player_id):
    state = active_battles.get(player_id)
    if not state:
        return

    player_data = state["players"][player_id]
    pkm = get_active_pokemon(player_data["team"])
    if not pkm:
        await context.bot.send_message(chat_id=player_id, text="❌ Aucun Pokémon actif !")
        return

    buttons = []
    for move in pkm["moves"]:
        label = f"{move['name']} ({move['pp']} PP)"
        buttons.append([InlineKeyboardButton(label, callback_data=f"move:{move['name']}")])

    await context.bot.send_message(
        chat_id=player_id,
        text=f"🎯 Choisis une attaque pour {pkm['name']} :",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def handle_attack_selection(update, context):
    query = update.callback_query
    await query.answer()
    player_id = update.effective_user.id
    state = active_battles.get(player_id)
    if not state:
        await query.edit_message_text("❌ Aucun combat trouvé.")
        return

    move_name = query.data.split(":")[1]
    player_data = state["players"][player_id]
    pkm = get_active_pokemon(player_data["team"])
    if not pkm:
        return

    move = next((m for m in pkm["moves"] if m["name"] == move_name), None)
    if not move or move["pp"] <= 0:
        await query.edit_message_text("❌ Cette attaque n'est plus disponible.")
        return

    move["pp"] -= 1
    player_data["selected_move"] = move
    player_data["turn_done"] = True
    await query.edit_message_text(f"✅ {pkm['name']} va utiliser {move_name} !")

    # Si les deux joueurs ont choisi, résoudre le tour
    if all(p["turn_done"] for p in state["players"].values()):
        await resolve_turn(context, state)

def can_attack(pkm):
    status = pkm.get("status")
    if status == "paralyzed":
        if random.random() < 0.75:
            return True
        else:
            return False
    if status == "sleep":
        # Ici tu peux gérer un compteur de tours de sommeil si tu veux
        return False
    # Par défaut
    return True

async def resolve_turn(context, state):
    players = list(state["players"].keys())
    pkm_data = {}
    moves_data = {}

    # Récupère Pokémon actifs et attaques choisies avec priorité
    for pid in players:
        pkm = get_active_pokemon(state["players"][pid]["team"])
        pkm_data[pid] = pkm
        move = state["players"][pid].get("selected_move")
        moves_data[pid] = move or {"priority": 0}

    # Tri par priorité puis vitesse
    def sort_key(pid):
        priority = moves_data[pid].get("priority", 0)
        speed = pkm_data[pid]["stats"].get("speed", 0) if pkm_data[pid] else 0
        return (priority, speed)

    order = sorted(players, key=sort_key, reverse=True)

    for attacker_id in order:
        defender_id = players[1] if attacker_id == players[0] else players[0]
        attacker = state["players"][attacker_id]
        defender = state["players"][defender_id]

        atk_pkm = pkm_data[attacker_id]
        def_pkm = pkm_data[defender_id]
        move = attacker.get("selected_move")

        if not atk_pkm or not def_pkm or atk_pkm["fainted"]:
            continue

        if not can_attack(atk_pkm):
            await context.bot.send_message(attacker_id, text=f"⚠️ {atk_pkm['name']} est {atk_pkm.get('status')} et ne peut pas attaquer ce tour !")
            continue

        dmg = calculate_damage(atk_pkm, def_pkm, move)
        def_pkm["current_hp"] -= dmg
        if def_pkm["current_hp"] <= 0:
            def_pkm["fainted"] = True
            def_pkm["current_hp"] = 0
            def_pkm["current_pokemon"] = False
            await context.bot.send_message(defender_id, text=f"💀 {def_pkm['name']} est K.O. !")
            await context.bot.send_message(attacker_id, text=f"✅ Tu as mis {def_pkm['name']} K.O. !")
            await try_auto_switch(context, defender_id, state)

    # Reset
    for p in state["players"].values():
        p["turn_done"] = False
        p["selected_move"] = None

    for pid in players:
        await prompt_attack_choice(context, pid)

def calculate_damage(attacker, defender, move):
    power = move.get("power", 30)
    atk = attacker["stats"].get("attack", 50)
    def_stat = defender["stats"].get("defense", 50)
    dmg = max(1, int(((power * atk / def_stat) / 2) * random.uniform(0.85, 1.0)))
    return dmg

async def try_auto_switch(context, player_id, state):
    team = state["players"][player_id]["team"]
    for pkm in team:
        if not pkm["fainted"]:
            pkm["current_pokemon"] = True
            await context.bot.send_message(player_id, text=f"🔁 {pkm['name']} entre en combat !")
            return
    # Plus de Pokémon dispo = défaite
    await context.bot.send_message(player_id, text="❌ Tous tes Pokémon sont K.O. !")
    opponent_id = [pid for pid in state["players"] if pid != player_id][0]
    await context.bot.send_message(opponent_id, text="🎉 Tu as gagné le combat !")

    # Supprime le combat
    for pid in state["players"]:
        del active_battles[pid]

