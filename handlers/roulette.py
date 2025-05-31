from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import random
import json
import os
import re
import time

from core.user_data import load_user, save_user, update_or_merge_pokemon_with_feedback, get_and_update_user
from core.pokemon_data import generate_pokemon
from core.items import get_capture_chance, ITEMS
from core.lang import get_text
from core.translation_data import POKEMON_NAMES, NATURES
from utils.buttons import main_menu

POKEDEX_PATH = "data/pokedex.json"
if os.path.exists(POKEDEX_PATH):
    with open(POKEDEX_PATH, "r") as f:
        POKEDEX = json.load(f)
else:
    POKEDEX = []

BALL_CHOICES = ["pokeball", "superball", "hyperball", "masterball"]

RARITY_EMOJIS = {
    "common": "⚪️",
    "uncommon": "🟢",
    "rare": "🔵",
    "epic": "🟣",
    "legendary": "🟡",
    "mythic": "🔴",
}


def build_ball_keyboard(pokeballs: dict, lang: str):
    buttons = []
    for b in BALL_CHOICES:
        qty = pokeballs.get(b, 0)
        label = f"{ITEMS[b][lang]} ({qty})"
        buttons.append(label)
    return ReplyKeyboardMarkup([buttons], resize_keyboard=True, one_time_keyboard=True)


def sanitize_for_url(name):
    name = name.lower()
    name = name.replace("nidoran♀", "nidoran-f").replace("nidoran♂", "nidoran-m")
    name = name.replace("farfetch’d", "farfetchd")
    name = name.replace("mr. mime", "mr-mime").replace("mime jr.", "mime-jr")
    name = name.replace("type: null", "type-null")
    name = name.replace("jangmo-o", "jangmoo").replace("hakamo-o", "hakamoo").replace("kommo-o", "kommoo")
    name = name.replace("’", "").replace("‘", "").replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
    name = name.replace(" ", "-").replace(".", "").replace(":", "")
    name = re.sub(r"[^a-z0-9\-]", "", name)
    return name


def get_money_reward(rarity):
    ranges = {
        "common": (150, 300),
        "uncommon": (300, 600),
        "rare": (600, 1200),
        "epic": (1200, 2000),
        "legendary": (2000, 5000),
        "mythic": (5000, 10000),
    }
    return random.randint(*ranges.get(rarity, (150, 300)))


def already_captured(data, name):
    for pkm in data.get("box", []):
        if pkm.get("locked") and pkm["name"] == name:
            return True
    return False


def get_money_bonus_multiplier(user_data):
    return 1.5 if user_data.get("items", {}).get("piece_rune", 0) > 0 else 1.0


async def roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = get_and_update_user(user.id, user.username)
    lang = data.get("lang", "fr")

    if all(data["pokeballs"].get(b, 0) <= 0 for b in BALL_CHOICES):
        await update.message.reply_text(get_text("no_more_balls", lang), reply_markup=main_menu(lang))
        return

    if not POKEDEX:
        await update.message.reply_text(get_text("no_pokemon_available", lang), reply_markup=main_menu(lang))
        return

    now = time.time()
    if now - context.user_data.get("last_roulette", 0) < 5:
        await update.message.reply_text(get_text("wait_roulette", lang, seconds=5))
        return

    context.user_data["last_roulette"] = now
    context.user_data["state"] = "roulette"

    names = [mon["name"] for mon in POKEDEX]
    weights = [mon["weight"] for mon in POKEDEX]
    chosen_base = random.choices(names, weights=weights, k=1)[0]
    rarity = next((m["rarity"] for m in POKEDEX if m["name"] == chosen_base), "common")

    chroma_bonus = min(data["items"].get("chroma", 0), 10)
    shiny_rate = 1 / (4096 / (1 + chroma_bonus))
    is_shiny = random.random() < shiny_rate

    chosen = f"shiny_{chosen_base}" if is_shiny else chosen_base
    context.user_data["current_encounter"] = {"name": chosen, "rarity": rarity, "shiny": is_shiny}

    display_name = POKEMON_NAMES.get(chosen_base, {}).get(lang, chosen_base)
    if is_shiny:
        display_name = f"✨ {display_name}"

    rarity_emoji = RARITY_EMOJIS.get(rarity, "")
    # Vérifie si un Pokémon de cette espèce est déjà dans le box (verrouillé)
    base_name = chosen.replace("shiny_", "")
    main_pokemon = next((pkm for pkm in data.get("box", []) if pkm.get("locked") and pkm["name"].replace("shiny_", "") == base_name), None)

    # Statut par défaut
    captured = False

    # Si un main_pokemon existe, on vérifie les natures et talents
    if main_pokemon:
        known_natures = main_pokemon.get("known_natures", [])
        known_talents = main_pokemon.get("known_talents", [])
        has_hidden = main_pokemon.get("hidden_ability", False)
    
        # On simule un Pokémon pour obtenir les futurs talents/natures
        fake = generate_pokemon(chosen, rarity, chroma_bonus=0)

        # Détection de nouveauté
        is_new_nature = fake["nature"] not in known_natures
        is_new_talent = fake["ability"] not in known_talents
        is_new_hidden = fake.get("hidden_ability", False) and not has_hidden
        is_new_shiny = "shiny_" in chosen and not main_pokemon["name"].startswith("shiny_")

        # Si aucune nouveauté détectée
        if not (is_new_nature or is_new_talent or is_new_hidden or is_new_shiny):
            captured = True

    status_text = get_text("already_caught" if captured else "new_catch", lang)

    image_base = sanitize_for_url(chosen_base)

    image_paths = [f"images/{image_base}.jpg", f"images/{image_base}.png", f"data/shiny/{image_base}.jpg", f"data/shiny/{image_base}.png"]
    for path in image_paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(photo=f)
            break
    else:
        await update.message.reply_photo(photo=f"https://img.pokemondb.net/artwork/{image_base}.jpg")

    await update.message.reply_text(
        f"🎯 *{get_text('wild_appears_simple', lang)}*\n\n"
        f"🆔 *Nom :* {display_name}\n"
        f"⭐ *Rareté :* {rarity_emoji} {get_text(rarity, lang)}\n"
        f"📌 *Statut :* {status_text}\n\n"
        f"🎒 *{get_text('choose_ball', lang)}*",
        reply_markup=build_ball_keyboard(data["pokeballs"], lang),
        parse_mode="Markdown"
    )

async def handle_ball_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = get_and_update_user(user.id, user.username)
    lang = data.get("lang", "fr")
    text = update.message.text.lower().replace("(", "").replace(")", "").replace("✨", "").strip()

    selected = None
    for ball in BALL_CHOICES:
        if ITEMS[ball][lang].lower() in text:
            selected = ball
            break

    if not selected:
        await update.message.reply_text("❌ Ball non reconnue.")
        return

    if data["pokeballs"].get(selected, 0) <= 0:
        still_have = any(data["pokeballs"].get(b, 0) > 0 for b in BALL_CHOICES)
        msg = get_text("choose_another_ball" if still_have else "no_more_balls", lang)
        kb = build_ball_keyboard(data["pokeballs"], lang) if still_have else main_menu(lang)
        await update.message.reply_text(msg, reply_markup=kb)
        return

    encounter = context.user_data.get("current_encounter")
    if not encounter:
        await update.message.reply_text("⚠️ Aucun Pokémon à capturer.", reply_markup=main_menu(lang))
        return

    chroma_bonus = min(data["items"].get("chroma", 0), 10)
    success = selected == "masterball" or random.random() < get_capture_chance(selected, encounter["rarity"])
    data["pokeballs"][selected] -= 1

    if success:
        pkm = generate_pokemon(encounter["name"], encounter["rarity"], chroma_bonus)
        messages = update_or_merge_pokemon_with_feedback(data, pkm, lang)
        reward = int(get_money_reward(encounter["rarity"]) * get_money_bonus_multiplier(data))
        data["money"] += reward
        save_user(user.id, data)
        await update.message.reply_text(get_text("catch_success", lang, name=POKEMON_NAMES.get(pkm["name"], {}).get(lang, pkm["name"]), money=reward), reply_markup=main_menu(lang))
        for m in messages:
            await update.message.reply_text(m)
    else:
        save_user(user.id, data)
        await update.message.reply_text(get_text("catch_failed", lang), reply_markup=main_menu(lang))

    context.user_data["current_encounter"] = None
    context.user_data["state"] = None