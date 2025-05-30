from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import random
import json
import os
import re
import time

from core.user_data import load_user, save_user, update_or_merge_pokemon_with_feedback
from core.pokemon_data import generate_pokemon
from core.items import get_capture_chance
from core.lang import get_text
from core.translation_data import POKEMON_NAMES, ITEMS, NATURES
from utils.buttons import main_menu

POKEDEX_PATH = "data/pokedex.json"
if os.path.exists(POKEDEX_PATH):
    with open(POKEDEX_PATH, "r") as f:
        POKEDEX = json.load(f)
else:
    POKEDEX = []

BALL_CHOICES = ["pokeball", "superball", "hyperball", "masterball"]

RARITY_EMOJIS = {
    "common": "⚪",
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
    
    # Exceptions spécifiques
    name = name.replace("nidoran♀", "nidoran-f").replace("nidoran♂", "nidoran-m")
    name = re.sub(r"unown[-_ ]?[a-z]?", "unown", name)
    name = name.replace("farfetch’d", "farfetchd")
    name = name.replace("mr. mime", "mr-mime").replace("mime jr.", "mime-jr")
    name = name.replace("type: null", "type-null")
    name = name.replace("jangmo-o", "jangmoo").replace("hakamo-o", "hakamoo").replace("kommo-o", "kommoo")

    # Nettoyage général
    name = re.sub(r"[♀♂.:'’/éèêà\- ]", "", name)
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

async def roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    last_spin = context.user_data.get("last_roulette", 0)
    now = time.time()
    if now - last_spin < 5:
        remaining = int(5 - (now - last_spin))
        await update.message.reply_text(get_text("wait_roulette", lang, seconds=remaining))
        return

    context.user_data["last_roulette"] = now
    context.user_data["state"] = "roulette"

    if not POKEDEX:
        await update.message.reply_text(get_text("no_pokemon_available", lang), reply_markup=main_menu(lang))
        return

    names = [mon["name"] for mon in POKEDEX]
    weights = [mon["weight"] for mon in POKEDEX]
    chosen = random.choices(names, weights=weights, k=1)[0]
    rarity = next((m["rarity"] for m in POKEDEX if m["name"] == chosen), "common")

    context.user_data["current_encounter"] = {
        "name": chosen,
        "rarity": rarity
    }

    translated_name = POKEMON_NAMES.get(chosen, {}).get(lang, chosen)
    rarity_emoji = RARITY_EMOJIS.get(rarity, "")
    captured = already_captured(data, chosen)
    status_text = get_text("already_caught" if captured else "new_catch", lang)

    image_base = sanitize_for_url(chosen)
    try:
        await update.message.reply_photo(photo=f"https://img.pokemondb.net/artwork/{image_base}.jpg")
    except Exception:
        try:
            await update.message.reply_photo(photo=f"https://img.pokemondb.net/artwork/{image_base}.png")
        except Exception:
            await update.message.reply_text("🌐 Image non trouvée. Le Pokémon apparaît sans image.")

    await update.message.reply_text(
        f"🔍 {get_text('wild_appears_simple', lang)}\n\n"
        f"🔸 {get_text('name_label', lang)} {translated_name}\n"
        f"🔸 {get_text('rarity_label', lang)} {rarity_emoji} {get_text(rarity, lang)}\n"
        f"🔸 {get_text('status_label', lang)} {status_text}\n\n"
        f"{get_text('choose_ball', lang)}",
        reply_markup=build_ball_keyboard(data["pokeballs"], lang)
    )

async def handle_ball_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    text = update.message.text.lower()

    ball_map = {
        "pokéball": "pokeball", "pokeball": "pokeball",
        "superball": "superball", "great ball": "superball",
        "hyperball": "hyperball", "ultra ball": "hyperball",
        "masterball": "masterball", "master ball": "masterball"
    }

    ball = None
    for label, key in ball_map.items():
        if label in text:
            ball = key
            break

    if ball is None or ball not in BALL_CHOICES:
        return

    if data["pokeballs"].get(ball, 0) <= 0:
        still_have = any(data["pokeballs"].get(b, 0) > 0 for b in BALL_CHOICES)
        if still_have:
            await update.message.reply_text(
                get_text("choose_another_ball", lang),
                reply_markup=build_ball_keyboard(data["pokeballs"], lang)
            )
        else:
            await update.message.reply_text(
                get_text("no_more_balls", lang),
                reply_markup=main_menu(lang)
            )
        return

    encounter = context.user_data.get("current_encounter")
    if not encounter:
        await update.message.reply_text("⚠️ Aucun Pokémon à capturer.", reply_markup=main_menu(lang))
        return

    chroma_bonus = min(data["items"].get("chroma", 0), 10)
    chance = get_capture_chance(ball, encounter["rarity"])
    capture = random.random() < chance or ball == "masterball"

    data["pokeballs"][ball] -= 1

    if capture:
        pkm = generate_pokemon(encounter["name"], encounter["rarity"], chroma_bonus)
        messages = update_or_merge_pokemon_with_feedback(data, pkm, lang)
        reward = get_money_reward(encounter["rarity"])
        data["money"] += reward
        save_user(user.id, data)

        translated = POKEMON_NAMES.get(pkm["name"], {}).get(lang, pkm["name"])
        await update.message.reply_text(
            get_text("catch_success", lang, name=translated, money=reward),
            reply_markup=main_menu(lang)
        )
        for msg in messages:
            await update.message.reply_text(msg)
    else:
        save_user(user.id, data)
        await update.message.reply_text(
            get_text("catch_failed", lang),
            reply_markup=main_menu(lang)
        )

    context.user_data["current_encounter"] = None
    context.user_data["state"] = None
