from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from handlers.trade import pending_trades
from core.lang import get_text

async def confirm_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    user_data = load_user(user.id)
    lang = user_data.get("lang", "fr")

    if not args:
        await update.message.reply_text(get_text("confirmtrade_usage", lang))
        return

    name = " ".join(args).strip().lower()
    trade = pending_trades.get(user.username)

    if not trade or not trade.get("accepted"):
        await update.message.reply_text(get_text("trade_no_pending", lang))
        return

    their_data = load_user(trade["from_id"])
    their_lang = their_data.get("lang", "fr")
    their_pokemon = trade.get("from_pokemon")

    # Vérifie que le Pokémon proposé par l'autre joueur est encore présent
    if not any(p == their_pokemon for p in their_data.get("box", [])):
        await update.message.reply_text(get_text("trade_cancelled_missing", lang))
        return

    # Récupère le Pokémon que l’utilisateur veut donner
    your_pokemon = next((p for p in user_data.get("box", []) if p.get("name", "").lower() == name), None)
    if not your_pokemon:
        await update.message.reply_text(get_text("trade_not_found", lang))
        return

    # 🔓 On autorise les échanges même si les Pokémon sont verrouillés
    # if your_pokemon.get("locked") or their_pokemon.get("locked"):
    #     await update.message.reply_text(get_text("trade_locked", lang))
    #     return

    try:
        user_data["box"].remove(your_pokemon)
        their_data["box"].remove(their_pokemon)

        user_data["box"].append(their_pokemon)
        their_data["box"].append(your_pokemon)

        save_user(user.id, user_data)
        save_user(trade["from_id"], their_data)

        await update.message.reply_text(get_text("trade_done", lang))
        await context.bot.send_message(chat_id=trade["from_id"], text=get_text("trade_done", their_lang))

        del pending_trades[user.username]

    except Exception as e:
        await update.message.reply_text(get_text("trade_error", lang))
        print(f"[TRADE ERROR] {e}")
