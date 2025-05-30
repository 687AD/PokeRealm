from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.lang import get_text
from core.stats import calculate_stats, format_stats
from core.moves import use_move
import json
import os

ADVENTURE_PATH = "data/adventure.json"
POKEDEX_PATH = "data/pokedex.json"

if os.path.exists(ADVENTURE_PATH):
    with open(ADVENTURE_PATH, "r") as f:
        ADVENTURE = json.load(f)
else:
    ADVENTURE = []

if os.path.exists(POKEDEX_PATH):
    with open(POKEDEX_PATH, "r") as f:
        POKEDEX = json.load(f)
else:
    POKEDEX = []

async def handle_adventure_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    args = context.args
    if not args:
        # Afficher la liste des adversaires
        msg = "🗺️ Liste des adversaires :\n"
        for adv in ADVENTURE:
            msg += f"/adventure {adv['id']} - {adv['name']} (niveau {adv['pokemons'][0]['level']})\n"
        await update.message.reply_text(msg)
        return

    # Récupérer l'id du PNJ
    try:
        adv_id = int(args[0])
    except ValueError:
        await update.message.reply_text("Utilisation : /adventure <numéro>")
        return

    adv = next((a for a in ADVENTURE if a["id"] == adv_id), None)
    if not adv:
        await update.message.reply_text("Adversaire introuvable.")
        return

    # Récupère le Pokémon principal du joueur
    pkm = next((p for p in data["box"] if p.get("locked")), None)
    if not pkm:
        await update.message.reply_text("❌ Tu n'as pas de Pokémon principal.")
        return

    # Récupère le premier Pokémon de l'adversaire
    adv_pkm = adv["pokemons"][0]

    # Prépare les boutons des attaques du joueur
    attack_buttons = [[KeyboardButton(m)] for m in pkm.get("moves", [])]
    markup = ReplyKeyboardMarkup(attack_buttons, resize_keyboard=True, one_time_keyboard=True)

    # Stocke le combat en cours dans user_data/context (pour la suite du tour par tour)
    context.user_data["battle"] = {
        "player": pkm,
        "opponent": adv_pkm,
        "adv_id": adv_id
    }

    await update.message.reply_text(
        f"⚔️ Tu affrontes {adv['name']} !\n\n"
        f"Ton Pokémon : {pkm['name']} (niveau {pkm.get('level',1)})\n"
        f"Adversaire : {adv_pkm['name']} (niveau {adv_pkm['level']})\n\n"
        "Choisis une attaque pour commencer :",
        reply_markup=markup
    )
