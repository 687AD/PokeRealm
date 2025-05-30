# utils/errors.py

import traceback
from telegram import Update
from telegram.ext import ContextTypes

from core.user_data import load_user
from utils.buttons import main_menu
from core.lang import get_text

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        raise context.error
    except Exception as e:
        user = update.effective_user if isinstance(update, Update) else None
        user_id = user.id if user else None
        lang = "fr"

        if user_id:
            try:
                data = load_user(user_id)
                lang = data.get("lang", "fr")
            except:
                pass

        # Affiche l'erreur dans la console
        print("🔥 Une erreur est survenue :")
        traceback.print_exc()

        # Message utilisateur
        if isinstance(update, Update) and update.message:
            await update.message.reply_text(
                get_text("generic_error", lang),
                reply_markup=main_menu(lang)
            )
