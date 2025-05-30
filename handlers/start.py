# handlers/start.py

from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from utils.buttons import main_menu
from core.lang import get_text
from handlers.lang import LANG_BUTTONS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = load_user(user.id)

    # Si la langue n'est pas encore choisie
    if "lang" not in user_data:
        await update.message.reply_text("Choisis ta langue / Choose your language:", reply_markup=LANG_BUTTONS)
        return

    lang = user_data["lang"]
    await update.message.reply_text(
        get_text("start_welcome", lang, name=user.first_name),
        reply_markup=main_menu(lang)
    )
