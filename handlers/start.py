from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from utils.buttons import main_menu
from core.lang import get_text
from handlers.lang import LANG_BUTTONS
from core.user_data import get_and_update_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = get_and_update_user(user.id, user.username)

    # ✅ Sauvegarde du nom d'utilisateur
    if user.username:
        user_data["username"] = user.username.lower()  # en minuscule pour éviter les erreurs

    # Si la langue n'est pas encore choisie
    if "lang" not in user_data:
        await update.message.reply_text("Choisis ta langue / Choose your language:", reply_markup=LANG_BUTTONS)
        save_user(user.id, user_data)  # Sauvegarde ici si on retourne déjà
        return

    lang = user_data["lang"]
    save_user(user.id, user_data)  # Toujours sauvegarder le username
    await update.message.reply_text(
        get_text("start_welcome", lang, name=user.first_name),
        reply_markup=main_menu(lang)
    )
