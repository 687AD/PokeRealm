from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.translation_data import NATURES, get_english_name, NATURES_FR_TO_EN, normalize
from core.lang import get_text, resolve_pokemon_internal_name
from utils.buttons import main_menu
from core.stats import calculate_stats
from core.nature import NATURE_EFFECTS, NATURE_EFFECTS_EN
import json
import os

# Charger les stats depuis le Pokédex JSON
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

    name_input_raw = args[0]
    name_input = resolve_pokemon_internal_name(name_input_raw, lang)
    english_name = get_english_name(name_input, lang)

    if not english_name:
        await update.message.reply_text(get_text("pokemon_not_found", lang))
        return

    chosen_raw = args[1]
    normalized = normalize(chosen_raw)
    nature_key = NATURES_FR_TO_EN.get(normalized, None)

    if not nature_key:
        nature_key = chosen_raw.capitalize()

    for pkm in data["box"]:
        if pkm.get("locked") and pkm["name"].lower() == english_name.lower():
            known_natures = pkm.get("known_natures", [pkm["nature"]])
            if nature_key in known_natures:
                pkm["nature"] = nature_key

                # Récupération des stats de base
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

                pkm["stats"] = calculate_stats(base, pkm["ivs"], nature_key, lang, level=pkm.get("level", 1))
                save_user(user.id, data)

                # Texte de réponse
                msg = f"✅ {get_text('nature_changed', lang, nature=NATURES.get(nature_key, {}).get(lang, nature_key))}"

                # Afficher uniquement les stats modifiées par la nature
                effects = NATURE_EFFECTS.get(nature_key) if lang == "fr" else NATURE_EFFECTS_EN.get(nature_key)
                labels = {
                    "fr": {
                        "atk": "Attaque",
                        "def": "Défense",
                        "spa": "Attaque Spéciale",
                        "spd": "Défense Spéciale",
                        "spe": "Vitesse",
                        "hp": "PV"
                    },
                    "en": {
                        "atk": "Attack",
                        "def": "Defense",
                        "spa": "Sp. Attack",
                        "spd": "Sp. Defense",
                        "spe": "Speed",
                        "hp": "HP"
                    }
                }

                if effects:
                    up = effects.get("up")
                    down = effects.get("down")
                    if up:
                        msg += f"\n🔺 {labels[lang].get(up, up)} +10%"
                    if down:
                        msg += f"\n🔻 {labels[lang].get(down, down)} -10%"

                await update.message.reply_text(msg, reply_markup=main_menu(lang))
                return
            else:
                await update.message.reply_text(get_text("nature_not_known", lang))
                return

    await update.message.reply_text(get_text("pokemon_not_found", lang))
