from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user
from core.translation_data import get_english_name, normalize
from core.lang import get_text, resolve_pokemon_internal_name
from core.stats import calculate_stats, format_stats
import json
import os

# Charger les base stats depuis le pokedex
POKEDEX_PATH = "data/pokedex.json"
if os.path.exists(POKEDEX_PATH):
    with open(POKEDEX_PATH, "r") as f:
        POKEDEX = json.load(f)
else:
    POKEDEX = []

async def handle_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    args = context.args
    if not args:
        await update.message.reply_text(get_text("stats_command_usage", lang))
        return

    name_input_raw = args[0]
    name_input = resolve_pokemon_internal_name(name_input_raw, lang)
    english_name = get_english_name(name_input, lang)

    if not english_name:
        await update.message.reply_text(get_text("pokemon_not_found", lang))
        return

    for pkm in data["box"]:
        if pkm.get("locked") and pkm["name"].lower() == english_name.lower():
            base_entry = next((p for p in POKEDEX if p["name"].lower() == pkm["name"].lower()), None)
            if base_entry:
                base = {
                    "hp": base_entry.get("hp", 40),
                    "atk": base_entry.get("atk", 40),
                    "def": base_entry.get("def", 40),
                    "spa": base_entry.get("spa", 40),
                    "spd": base_entry.get("spd", 40),
                    "spe": base_entry.get("spe", 40),
                }
            else:
                base = {"hp": 40, "atk": 40, "def": 40, "spa": 40, "spd": 40, "spe": 40}

            stats = calculate_stats(base, pkm["ivs"], pkm["nature"], lang, level=pkm.get("level", 1), evs=pkm.get("evs"))
            await update.message.reply_text(format_stats(stats, lang, level=pkm.get("level", 1), exp=pkm.get("exp", 0), evs=pkm.get("evs", {})))
            return

    await update.message.reply_text(get_text("pokemon_not_found", lang))
