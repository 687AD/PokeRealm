from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.translation_data import NATURES, get_english_name, NATURES_FR_TO_EN, normalize, resolve_pokemon_internal_name
from core.lang import get_text
from utils.buttons import main_menu
from core.stats import calculate_stats
from core.nature import NATURE_EFFECTS, NATURE_EFFECTS_EN
import json
import os

POKEDEX_PATH = "data/pokedex.json"
if os.path.exists(POKEDEX_PATH):
    with open(POKEDEX_PATH, "r") as f:
        POKEDEX = json.load(f)
else:
    POKEDEX = []

async def handle_nature_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    args = context.args
    if len(args) < 2:
        await update.message.reply_text(get_text("nature_command_usage", lang))
        return

    # 🔍 Resolve Pokémon name
    name_arg = args[0]
    internal_name = resolve_pokemon_internal_name(name_arg, lang)

    # 🎯 Find matching Pokémon
    box = data.get("box", [])
    pkm = next((p for p in box if p["name"].lower() == internal_name.lower() and p.get("locked")), None)
    if not pkm:
        await update.message.reply_text(get_text("pokemon_not_found", lang))
        return

    # 🧠 Normalize nature
    chosen_raw = args[1]
    normalized = normalize(chosen_raw)
    nature_key = NATURES_FR_TO_EN.get(normalized, chosen_raw.capitalize())

    if nature_key not in pkm.get("known_natures", [pkm["nature"]]):
        await update.message.reply_text(get_text("nature_not_known", lang))
        return

    # ✅ Apply nature
    pkm["nature"] = nature_key

    # 📈 Recalculate stats
    base_entry = next((p for p in POKEDEX if p["name"].lower() == pkm["name"].lower()), None)
    base = {
        "hp": base_entry.get("hp", 40) if base_entry else 40,
        "atk": base_entry.get("atk", 40) if base_entry else 40,
        "def": base_entry.get("def", 40) if base_entry else 40,
        "spa": base_entry.get("spa", 40) if base_entry else 40,
        "spd": base_entry.get("spd", 40) if base_entry else 40,
        "spe": base_entry.get("spe", 40) if base_entry else 40,
    }

    pkm["stats"] = calculate_stats(base, pkm["ivs"], nature_key, lang, level=pkm.get("level", 1))
    save_user(user.id, data)

    # 💬 Confirmation message
    msg = f"✅ {get_text('nature_changed', lang, nature=NATURES.get(nature_key, {}).get(lang, nature_key))}"

    effects = NATURE_EFFECTS.get(nature_key) if lang == "fr" else NATURE_EFFECTS_EN.get(nature_key)
    labels = {
        "fr": {"atk": "Attaque", "def": "Défense", "spa": "Attaque Spéciale", "spd": "Défense Spéciale", "spe": "Vitesse", "hp": "PV"},
        "en": {"atk": "Attack", "def": "Defense", "spa": "Sp. Attack", "spd": "Sp. Defense", "spe": "Speed", "hp": "HP"}
    }

    if effects:
        if effects.get("up"):
            msg += f"\n🔺 {labels[lang].get(effects['up'], effects['up'])} +10%"
        if effects.get("down"):
            msg += f"\n🔻 {labels[lang].get(effects['down'], effects['down'])} -10%"

    await update.message.reply_text(msg, reply_markup=main_menu(lang))

