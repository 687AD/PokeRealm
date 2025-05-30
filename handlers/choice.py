# handlers/choice.py

from telegram import Update
from telegram.ext import ContextTypes
from handlers.shop import handle_shop_selection
from handlers.roulette import handle_ball_choice

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")

    if state == "shop":
        await handle_shop_selection(update, context)
    elif state == "roulette":
        await handle_ball_choice(update, context)
    else:
        await update.message.reply_text("❓ Je ne sais pas quoi faire avec ça.")


