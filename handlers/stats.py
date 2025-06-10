from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user
from core.translation_data import get_english_name, resolve_pokemon_internal_name, POKEMON_NAMES
from core.lang import get_text
from core.stats import calculate_stats
import json
import os

def get_pokemon_image_path(pkm):
    import re
    import os

    def sanitize_for_url(name):
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

    image_base = sanitize_for_url(pkm["name"].replace("shiny_", ""))
    is_shiny = pkm["name"].startswith("shiny_") or pkm.get("shiny", False)
    if is_shiny:
        image_paths = [
            f"data/shiny/{image_base}.png",
            f"data/shiny/{image_base}.jpg",
            f"images/{image_base}.png",
            f"images/{image_base}.jpg"
        ]
    else:
        image_paths = [
            f"images/{image_base}.png",
            f"images/{image_base}.jpg",
            f"data/shiny/{image_base}.png",
            f"data/shiny/{image_base}.jpg"
        ]
    for path in image_paths:
        if os.path.exists(path):
            return path
    # Fallback web
    if is_shiny:
        return f"https://img.pokemondb.net/sprites/home/shiny/{image_base}.png"
    else:
        return f"https://img.pokemondb.net/sprites/home/normal/{image_base}.png"

# Chargement du Pokédex
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
    box = data.get("box", [])

    args = context.args
    if not args:
        await update.message.reply_text(get_text("stats_command_usage", lang))
        return

    name_input = args[0]
    internal_name = resolve_pokemon_internal_name(name_input, lang)
    pkm = next((p for p in box if p["name"].lower() == internal_name.lower()), None)

    if not pkm:
        await update.message.reply_text(get_text("pokemon_not_found", lang))
        return

    # Vérifie que c’est bien un Pokémon principal
    if not pkm.get("locked"):
        await update.message.reply_text(get_text("pokemon_not_found", lang))
        return

    # Récupère les bases stats
    base_entry = next((p for p in POKEDEX if p["name"].lower() == pkm["name"].lower()), None)
    base = {
        "hp": base_entry.get("hp", 40) if base_entry else 40,
        "atk": base_entry.get("atk", 40) if base_entry else 40,
        "def": base_entry.get("def", 40) if base_entry else 40,
        "spa": base_entry.get("spa", 40) if base_entry else 40,
        "spd": base_entry.get("spd", 40) if base_entry else 40,
        "spe": base_entry.get("spe", 40) if base_entry else 40,
    }

    stats = calculate_stats(
        base=base,
        ivs=pkm["ivs"],
        nature=pkm["nature"],
        lang=lang,
        level=pkm.get("level", 1),
        evs=pkm.get("evs", {})
    )

    # Format propre
    msg = f"📊 *Stats de {POKEMON_NAMES.get(pkm['name'], {}).get(lang, pkm['name'])}* (Lvl {pkm.get('level', 1)})\n"
    msg += f"`PV  : {stats['hp']}`\n"
    msg += f"`ATK : {stats['atk']}`\n"
    msg += f"`DEF : {stats['def']}`\n"
    msg += f"`SPA : {stats['spa']}`\n"
    msg += f"`SPD : {stats['spd']}`\n"
    msg += f"`SPE : {stats['spe']}`"

    image_path = get_pokemon_image_path(pkm)

    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                await update.message.reply_photo(photo=f, caption=msg, parse_mode="Markdown")
        else:
            await update.message.reply_photo(photo=image_path, caption=msg, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(msg, parse_mode="Markdown")

