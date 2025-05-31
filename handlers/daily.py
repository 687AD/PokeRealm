# handlers/daily.py

from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from core.user_data import load_user, save_user
from core.lang import get_text
from core.user_data import get_and_update_user

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = get_and_update_user(user.id, user.username)
    lang = data.get("lang", "fr")

    today = datetime.now().date().isoformat()

    if data.get("daily_claimed") == today:
        await update.message.reply_text(get_text("daily_already", lang))
        return

    data["daily_claimed"] = today
    data["money"] += 1000
    data["pokeballs"]["pokeball"] += 10

    save_user(user.id, data)
    await update.message.reply_text(get_text("daily_reward", lang))
