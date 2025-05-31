from telegram import Update
from telegram.ext import ContextTypes
from handlers.trade import pending_trades
from core.lang import get_text
from core.user_data import load_user

async def handle_trade_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    action, proposer_id = data.split(":")
    proposer_id = int(proposer_id)
    accepter = update.effective_user
    accepter_data = load_user(accepter.id)
    lang = accepter_data.get("lang", "fr")

    trade = pending_trades.get(accepter.username)
    if not trade:
        await query.edit_message_text(get_text("trade_expired", lang))
        return

    if action == "accept_trade":
        trade["accepted"] = True
        trade["to_id"] = accepter.id
        await query.edit_message_text(get_text("trade_accepted", lang))

    elif action == "refuse_trade":
        await query.edit_message_text(get_text("trade_refused", lang))
        del pending_trades[accepter.username]
