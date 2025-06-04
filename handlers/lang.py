# handlers/lang.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.lang import get_text
from utils.buttons import main_menu

# Clavier des langues
LANG_BUTTONS = ReplyKeyboardMarkup(
    [[KeyboardButton("🇫🇷 Français"), KeyboardButton("🇬🇧 English")]],
    resize_keyboard=True
)

async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Demande à l'utilisateur de choisir sa langue
    await update.message.reply_text("👅 Choisis ta langue : / 🌍 Choose your langage :", reply_markup=LANG_BUTTONS)

async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang_choice = update.message.text

    lang = "fr" if "français" in lang_choice.lower() else "en"
    data = load_user(user.id)
    data["lang"] = lang
    save_user(user.id, data)

    confirmation = get_text("lang_set", lang)
    await update.message.reply_text(confirmation, reply_markup=main_menu(lang)
)
