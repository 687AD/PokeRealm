from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.translation_data import POKEMON_NAMES
from core.lang import get_text

pending_trades = {}

async def propose_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    data = load_user(user.id)
    lang = data.get("lang", "fr")

    if len(args) < 2:
        await update.message.reply_text(get_text("trade_usage", lang))
        return

    target_username = args[0].replace("@", "")
    pokemon_name = " ".join(args[1:])

    pokemon = next((p for p in data.get("box", []) if p["name"].lower() == pokemon_name.lower()), None)
    if not pokemon:
        await update.message.reply_text(get_text("trade_not_found", lang))
        return

    pending_trades[target_username] = {
        "from_id": user.id,
        "from_pokemon": pokemon,
        "state": "pending"
    }

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅", callback_data=f"accept_trade:{user.id}"),
         InlineKeyboardButton("❌", callback_data=f"refuse_trade:{user.id}")]
    ])

    await update.message.reply_text(get_text("trade_sent", lang).format(target=target_username))
    await context.bot.send_message(
        chat_id=f"@{target_username}",
        text=get_text("trade_proposal_received", lang).format(proposer=user.username, pokemon=pokemon["name"]),
        reply_markup=buttons
    )
