from core.user_data import load_user
from utils.buttons import main_menu

async def handle_return(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = load_user(user.id).get("lang", "fr")
    await update.message.reply_text("⬅️ Retour au menu principal.", reply_markup=main_menu(lang))
    context.user_data["state"] = None
    context.user_data["current_encounter"] = None
    context.user_data["pending_item"] = None
