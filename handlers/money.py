# handlers/money.py

from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user


async def show_money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    amount = data.get("money", 0)

    if lang == "fr":
        message = f"💰 Tu as actuellement {amount} pokédollars."
    else:
        message = f"💰 You currently have {amount} Pokédollars."

    await update.message.reply_text(message)
