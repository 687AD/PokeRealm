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
from handlers.box import POKEBALL_EMOJIS

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
    ball_emojis = {
        "pokeball": "🔴",
        "superball": "🔵",
        "hyperball": "🟡",
        "masterball": "🟣"
    }
    ball_labels = {
        "pokeball": "Pokéball",
        "superball": "Superball",
        "hyperball": "Hyperball",
        "masterball": "Masterball"
    }
    row1 = [f"{ball_emojis['pokeball']} {ball_labels['pokeball']} ({pokeballs.get('pokeball',0)})",
            f"{ball_emojis['superball']} {ball_labels['superball']} ({pokeballs.get('superball',0)})"]
    row2 = [f"{ball_emojis['hyperball']} {ball_labels['hyperball']} ({pokeballs.get('hyperball',0)})",
            f"{ball_emojis['masterball']} {ball_labels['masterball']} ({pokeballs.get('masterball',0)})"]
    row3 = [f"🏃 {get_text('flee', lang)}"]
    return ReplyKeyboardMarkup([row1, row2, row3], resize_keyboard=True, one_time_keyboard=True)

def sanitize_for_url(name):
    # Clean for Pokemondb url
    name = name.lower()
    name = name.replace("nidoran♀", "nidoran-f").replace("nidoran♂", "nidoran-m")
    name = name.replace("farfetch’d", "farfetchd").replace("farfetch'd", "farfetchd")
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

def get_money_bonus_multiplier(user_data):
    """Retourne le multiplicateur de gain lié à la Pièce Rune."""
    amount = min(user_data.get("items", {}).get("piece_rune", 0), 20)
    return 1.0 + amount * 0.05  # +5% par Pièce Rune, max +100%

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
    cooldown = 5  # en secondes
    last = context.user_data.get("last_roulette", 0)
    wait_left = int(cooldown - (now - last))
    if wait_left > 0:
        await update.message.reply_text(get_text("wait_roulette", lang, seconds=wait_left))
        return

    context.user_data["last_roulette"] = now
    context.user_data["state"] = "roulette"

    names = [mon["name"] for mon in POKEDEX]
    weights = [mon["weight"] for mon in POKEDEX]
    chosen_base = random.choices(names, weights=weights, k=1)[0]
    rarity = next((m["rarity"] for m in POKEDEX if m["name"] == chosen_base), "common")

    nb_charmes = min(data["items"].get("chroma", 0), 20)
    taux_base = 1 / 4096
    shiny_rate = taux_base * (1 + 0.05 * nb_charmes)
    is_shiny = random.random() < shiny_rate

    chosen = f"shiny_{chosen_base}" if is_shiny else chosen_base
    context.user_data["current_encounter"] = {"name": chosen, "rarity": rarity, "shiny": is_shiny}

    display_name = POKEMON_NAMES.get(chosen_base, {}).get(lang, chosen_base)
    if is_shiny:
        display_name = f"✨ {display_name}"

    rarity_emoji = RARITY_EMOJIS.get(rarity, "")
    base_name = chosen.replace("shiny_", "")
    # Récupère tous les Pokémon du joueur de ce nom (base_name, shiny ou pas)
    box_pokemons = [pkm for pkm in data.get("box", []) if pkm["name"].replace("shiny_", "") == base_name]

    status_key = "new_catch"
    if box_pokemons:
        is_shiny_encounter = chosen.startswith("shiny_")
        # Est-ce qu'on possède déjà CE TYPE (shiny ou non) ?
        is_already_owned = any(
            (pkm["name"].startswith("shiny_") if is_shiny_encounter else not pkm["name"].startswith("shiny_"))
            for pkm in box_pokemons
        )

        # Simulation de la rencontre
        fake = generate_pokemon(chosen, rarity, chroma_bonus=0)
        info_nouvelle = False

        # Pour chaque Pokémon du même type déjà possédé, regarde si cette nouvelle rencontre apporte quelque chose de neuf
        for pkm in box_pokemons:
            # On ne compare qu'aux exemplaires de même type (shiny ou non)
            if pkm["name"].startswith("shiny_") == is_shiny_encounter:
                known_natures = pkm.get("known_natures", [])
                known_talents = pkm.get("known_abilities", [])
                has_hidden = pkm.get("hidden_ability", False)
                known_ivs = pkm.get("ivs", {})

                is_new_nature = fake["nature"] not in known_natures
                is_new_talent = fake["ability"] not in known_talents
                is_new_hidden = fake.get("hidden_ability", False) and not has_hidden
                is_new_ivs = any(fake["ivs"].get(stat, 0) > known_ivs.get(stat, -1) for stat in fake["ivs"])

                if is_new_nature or is_new_talent or is_new_hidden or is_new_ivs:
                    info_nouvelle = True
                    break

        if is_already_owned:
            status_key = "already_caught_with_new_info" if info_nouvelle else "already_caught"
        else:
            status_key = "new_catch"

    status_text = get_text(status_key, lang)
    image_base = sanitize_for_url(chosen_base)
    is_shiny_encounter = chosen.startswith("shiny_")

    if is_shiny_encounter:
        # Priorité aux images shiny
        image_paths = [
            f"data/shiny/{image_base}.png",
            f"data/shiny/{image_base}.jpg",
            f"images/{image_base}.png",
            f"images/{image_base}.jpg"
        ]
    else:
        # Priorité aux images normales
        image_paths = [
            f"images/{image_base}.png",
            f"images/{image_base}.jpg",
            f"data/shiny/{image_base}.png",
            f"data/shiny/{image_base}.jpg"
        ]

    sent_image = False
    for path in image_paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(photo=f)
                sent_image = True
                break

    if not sent_image:
        # Fallback web : cherche une image shiny ou normale selon le cas
        if is_shiny_encounter:
            url = f"https://img.pokemondb.net/sprites/home/shiny/{image_base}.png"
        else:
            url = f"https://img.pokemondb.net/sprites/home/normal/{image_base}.png"
        try:
            await update.message.reply_photo(photo=url)
        except Exception:
            await update.m

    # Message bonus si shiny ou mythique
    if is_shiny or rarity == "mythic":
        special_msg = "🤯 Quelle singerie ! Ce Pokémon est ultra rare !" if lang == "fr" else "🤯 What madness! This Pokémon is ultra rare!"
        await update.message.reply_text(special_msg)

    # Message principal
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
    text = update.message.text.lower().replace("(", "").replace(")", "").replace("✨", "").replace("🏃‍♂️", "").strip()

    # Vérifier la fuite
    flee_label = get_text("flee", lang).lower()
    if flee_label in text or "fuite" in text or "flee" in text:
        await update.message.reply_text(get_text("flee_success", lang), reply_markup=main_menu(lang))
        context.user_data["current_encounter"] = None
        context.user_data["state"] = None
        return

    ball_labels = {
        "pokeball": "pokéball",
        "superball": "superball",
        "hyperball": "hyperball",
        "masterball": "masterball"
    }
    selected = None
    for ball in BALL_CHOICES:
        # On vérifie si le texte contient le nom complet de la ball (insensible à la casse, ignore l’emoji et la quantité)
        if ball_labels[ball] in text:
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
    chance = get_capture_chance(selected, encounter["rarity"])
    success = selected == "masterball" or random.random() < (chance / 100)
    data["pokeballs"][selected] -= 1


    if success:
        pkm = generate_pokemon(encounter["name"], encounter["rarity"], chroma_bonus)
        pkm["caught_with"] = selected
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
