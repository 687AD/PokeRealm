import os
import unicodedata
from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user, update_or_merge_pokemon_with_feedback
from core.pokemon_data import generate_pokemon
from core.translation_data import POKEMON_NAMES
from core.lang import get_text
from utils.buttons import main_menu
from handlers.roulette import sanitize_for_url

ADMIN_IDS = [2142091056]  # Mets ton/tes ID(s)

# Helper pour rendre le nom super standard (minuscule, sans accents, sans espace, sans point, etc.)
def clean_name(s):
    s = s.lower()
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode("utf-8")
    s = s.replace("’", "").replace("'", "")
    s = s.replace(".", "").replace("-", "").replace(" ", "")
    return s

async def spawn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in ADMIN_IDS:
        await update.message.reply_text("❌ Accès refusé.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("Utilisation : /spawn <NomPokemon> [rarete] [shiny]")
        return

    # Parsing des arguments (shiny & rareté tolérés à n'importe quelle place)
    is_shiny = False
    rarity = "common"
    name_parts = []
    for part in args:
        if part.lower() == "shiny":
            is_shiny = True
        elif part.lower() in ["common", "uncommon", "rare", "epic", "legendary", "mythic"]:
            rarity = part.lower()
        else:
            name_parts.append(part)
    raw_name_input = " ".join(name_parts).strip()
    name_input = clean_name(raw_name_input)

    # Recherche ultra tolérante dans POKEMON_NAMES
    found_key = None
    for k, v in POKEMON_NAMES.items():
        all_aliases = [
            k,
            v.get("fr", ""),
            v.get("en", ""),
            k.replace("-", "").replace(" ", "").replace(".", ""),
            v.get("fr", "").replace("-", "").replace(" ", "").replace(".", ""),
            v.get("en", "").replace("-", "").replace(" ", "").replace(".", ""),
            clean_name(k),
            clean_name(v.get("fr", "")),
            clean_name(v.get("en", ""))
        ]
        if name_input in [clean_name(alias) for alias in all_aliases]:
            found_key = k
            break

    if not found_key:
        # Suggestion intelligente
        suggestions = []
        for k, v in POKEMON_NAMES.items():
            if name_input in clean_name(k) or name_input in clean_name(v.get("fr", "")) or name_input in clean_name(v.get("en", "")):
                suggestions.append(v.get("fr", k))
        suggestion_msg = f"❌ Pokémon introuvable : {raw_name_input}"
        if suggestions:
            suggestion_msg += "\nTu voulais peut-être : " + ", ".join(suggestions)
        await update.message.reply_text(suggestion_msg)
        return

    # Génération du Pokémon
    pkm_name = f"shiny_{found_key}" if is_shiny else found_key
    pkm = generate_pokemon(pkm_name, rarity)
    if is_shiny:
        pkm["shiny"] = True

    data = load_user(user.id)
    lang = data.get("lang", "fr")
    feedback = update_or_merge_pokemon_with_feedback(data, pkm, lang)
    save_user(user.id, data)

    # Affichage image comme dans la roulette
    image_base = sanitize_for_url(found_key)
    try:
        if is_shiny:
            shiny_path_jpg = f"data/shiny/{image_base}.jpg"
            shiny_path_png = f"data/shiny/{image_base}.png"
            if os.path.exists(shiny_path_jpg):
                with open(shiny_path_jpg, "rb") as f:
                    await update.message.reply_photo(photo=f)
            elif os.path.exists(shiny_path_png):
                with open(shiny_path_png, "rb") as f:
                    await update.message.reply_photo(photo=f)
            else:
                await update.message.reply_photo(photo=f"https://img.pokemondb.net/sprites/home/shiny/1x/{image_base}.png")
        else:
            image_path_jpg = f"images/{image_base}.jpg"
            image_path_png = f"images/{image_base}.png"
            if os.path.exists(image_path_jpg):
                with open(image_path_jpg, "rb") as f:
                    await update.message.reply_photo(photo=f)
            elif os.path.exists(image_path_png):
                with open(image_path_png, "rb") as f:
                    await update.message.reply_photo(photo=f)
            else:
                await update.message.reply_photo(photo=f"https://img.pokemondb.net/artwork/{image_base}.jpg")
    except Exception as e:
        await update.message.reply_text("🌐 Image non trouvée. Le Pokémon apparaît sans image.")

    # Affichage final ultra clean
    display_name = POKEMON_NAMES.get(found_key, {}).get(lang, found_key)
    if is_shiny:
        display_name = f"✨ {display_name}"
    await update.message.reply_text(
        f"Pokémon {display_name} généré !\n{feedback if feedback else ''}",
        reply_markup=main_menu(lang)
    )
