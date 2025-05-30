from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.translation_data import resolve_pokemon_internal_name, POKEMON_NAMES

async def handle_team_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    args = context.args
    box = data.get("box", [])
    team = data.setdefault("team", [])
    lang = data.get("lang", "fr")

    if len(args) != 2:
        await update.message.reply_text("Utilisation : /team <1-6> <nom du Pokémon>")
        return

    try:
        pos = int(args[0]) - 1
        if not (0 <= pos < 6):
            raise ValueError
    except ValueError:
        await update.message.reply_text("La position doit être comprise entre 1 et 6.")
        return

    name_arg = args[1]
    name_internal = resolve_pokemon_internal_name(name_arg, lang)

    idx = next(
        (i for i, p in enumerate(box) if p["name"].lower() == name_internal.lower()),
        None
    )
    if idx is None:
        noms = [
            POKEMON_NAMES.get(p["name"], {}).get(lang, p["name"])
            for p in box
        ]
        await update.message.reply_text(
            "Pokémon introuvable dans ta box. Voici ceux que tu possèdes :\n" + "\n".join(noms)
        )
        return

    # Vérifie que le Pokémon n'est pas déjà dans la team (hors la position courante)
    if idx in [team[i] for i in range(len(team)) if i != pos and team[i] is not None]:
        poke_name = POKEMON_NAMES.get(box[idx]["name"], {}).get(lang, box[idx]["name"])
        await update.message.reply_text(f"{poke_name} est déjà dans ton équipe à une autre position.")
        return

    # Ajoute ou remplace
    if len(team) < pos + 1:
        team += [None] * (pos + 1 - len(team))
    team[pos] = idx
    save_user(user.id, data)

    poke_name = POKEMON_NAMES.get(box[idx]["name"], {}).get(lang, box[idx]["name"])
    await update.message.reply_text(f"{poke_name} a été placé à la position {pos+1} dans l'équipe.")

async def show_team_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    team = data.get("team", [])
    box = data.get("box", [])
    lang = data.get("lang", "fr")
    if not team or all(i is None for i in team):
        await update.message.reply_text("Ton équipe est vide.")
        return
    text = "👥 Ton équipe :\n"
    for n, idx in enumerate(team):
        if idx is not None and idx < len(box):
            p = box[idx]
            name = POKEMON_NAMES.get(p['name'], {}).get(lang, p['name'])
            text += f"{n+1}. {name} (Niveau {p.get('level',1)})\n"
        else:
            text += f"{n+1}. (vide)\n"
    await update.message.reply_text(text)
