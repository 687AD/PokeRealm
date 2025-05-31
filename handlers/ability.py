from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.translation_data import resolve_pokemon_internal_name
from core.lang import get_text

async def ability_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    args = context.args
    if len(args) < 2:
        await update.message.reply_text(get_text("ability_command_usage", lang))
        return

    name_input = args[0]
    new_ability = " ".join(args[1:])  # cas où le talent a un espace

    internal_name = resolve_pokemon_internal_name(name_input)
    if not internal_name:
        await update.message.reply_text(get_text("pokemon_not_found", lang))
        return

    box = data.get("box", [])
    for pkm in box:
        if pkm.get("locked") and pkm["name"] == internal_name:
            known_abilities = pkm.get("known_abilities", [pkm.get("ability", "")])
            if new_ability not in known_abilities:
                await update.message.reply_text(get_text("ability_not_known", lang))
                return

            pkm["ability"] = new_ability
            save_user(user.id, data)
            await update.message.reply_text(get_text("ability_changed", lang, ability=new_ability))
            return

    await update.message.reply_text(get_text("pokemon_not_found", lang))
