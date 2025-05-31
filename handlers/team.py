from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.translation_data import POKEMON_NAMES, resolve_pokemon_internal_name, get_english_name
from core.lang import get_text

async def handle_team_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    args = context.args

    if len(args) != 2:
        await update.message.reply_text("Utilisation : /team <1-6> <nom du Pokémon>")
        return

    # 🔢 Position
    try:
        pos = int(args[0]) - 1
        if not (0 <= pos < 6):
            raise ValueError
    except ValueError:
        await update.message.reply_text("La position doit être comprise entre 1 et 6.")
        return

    # 🔍 Nom du Pokémon
    name_input = args[1]
    internal_name = resolve_pokemon_internal_name(name_input, lang)

    box = data.get("box", [])
    pkm = next((p for p in box if p["name"].lower() == internal_name.lower()), None)
    if not pkm:
        available = [
            POKEMON_NAMES.get(p["name"], {}).get(lang, p["name"]) for p in box
        ]
        await update.message.reply_text("Pokémon introuvable dans ta box. Voici ceux que tu possèdes :\n" + "\n".join(available))
        return

    idx = box.index(pkm)
    team = data.setdefault("team", [])

    # 🛡️ Empêche les doublons
    if idx in [team[i] for i in range(len(team)) if i != pos and team[i] is not None]:
        poke_name = POKEMON_NAMES.get(pkm["name"], {}).get(lang, pkm["name"])
        await update.message.reply_text(f"{poke_name} est déjà dans ton équipe à une autre position.")
        return

    # 🧩 Ajout/remplacement
    if len(team) < pos + 1:
        team += [None] * (pos + 1 - len(team))
    team[pos] = idx
    save_user(user.id, data)

    poke_name = POKEMON_NAMES.get(pkm["name"], {}).get(lang, pkm["name"])
    await update.message.reply_text(f"{poke_name} a été placé à la position {pos+1} dans l'équipe.")

async def show_team_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    team = data.get("team", [])
    box = data.get("box", [])

    if not team or all(i is None for i in team):
        await update.message.reply_text("Ton équipe est vide.")
        return

    text = "👥 Ton équipe :\n"
    for n, idx in enumerate(team):
        if idx is not None and idx < len(box):
            p = box[idx]
            name = POKEMON_NAMES.get(p["name"], {}).get(lang, p["name"])
            shiny_icon = "✨ " if p.get("shiny") else ""
            level = p.get("level", 1)
            text += f"{n+1}. {shiny_icon}{name} (Niveau {level})\n"
        else:
            text += f"{n+1}. (vide)\n"

    await update.message.reply_text(text)
