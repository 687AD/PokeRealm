from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from handlers.lang import ask_language, handle_language_choice
from handlers.choice import handle_choice
from handlers.start import start
from handlers.daily import daily
from handlers.roulette import roulette, handle_ball_choice
from handlers.inventory import show_inventory
from handlers.shop import show_shop
from handlers.unknown import unknown
from handlers.money import show_money
from handlers.box import show_box, sell_duplicates, handle_box_choice, handle_sort_choice, handle_box_navigation
from utils.buttons import main_menu
from core.user_data import load_user
from core.lang import get_text
from handlers.nature import handle_nature_command
from handlers.help import help_command
from handlers.stats import handle_stats_command
from handlers.adventure import handle_adventure_command
from handlers.team import handle_team_command, show_team_command

TOKEN = "8171438159:AAEC58M69Ddxprn645xTO-WuakzABqJnEUA"

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # 🔙 Retour
    async def handle_return(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        data = load_user(user.id)
        lang = data.get("lang", "fr")

        await update.message.reply_text("⬅️ Retour au menu principal.", reply_markup=main_menu(lang))
        context.user_data.clear()

    langs = ["fr", "en"]

    # ✅ Commandes classiques
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("lang", ask_language))
    app.add_handler(CommandHandler("money", show_money))
    app.add_handler(CommandHandler("nature", handle_nature_command))
    app.add_handler(CommandHandler("sell_duplicates", sell_duplicates))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", handle_stats_command))
    app.add_handler(CommandHandler("adventure", handle_adventure_command))
    app.add_handler(CommandHandler("team", handle_team_command))
    app.add_handler(CommandHandler("show_team", show_team_command))

    # ✅ Boutons traduits (multilingue)
    app.add_handler(MessageHandler(filters.Regex("^👥 Mon équipe$"), show_team_command))
    app.add_handler(MessageHandler(filters.Regex("^👥 My Team$"), show_team_command))
    app.add_handler(MessageHandler(
    filters.Text([get_text("menu_help", lang) for lang in langs]),
    help_command
    ))
    app.add_handler(MessageHandler(
    filters.Text(["🔼 Page précédente", "🔽 Page suivante"]),
    handle_box_navigation
    ))
    app.add_handler(MessageHandler(
    filters.Text([get_text("button_sort_box", lang) for lang in ["fr", "en"]]),
    handle_sort_choice
    ))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🔤|🔺|📉|📦|✨|💯"), handle_sort_choice))
    app.add_handler(MessageHandler(filters.Text("📁 Box"), show_box))
    app.add_handler(MessageHandler(filters.Text(["🗑️ Sell duplicates", "🗑️ Vendre les doublons"]), handle_box_choice))
    app.add_handler(MessageHandler(
    filters.Text([get_text("button_sell_duplicates", lang) for lang in ["fr", "en"]]),
    sell_duplicates
    ))
    app.add_handler(MessageHandler(filters.Regex("(?i)(français|english)"), handle_language_choice))

    app.add_handler(MessageHandler(
        filters.Text([get_text("menu_roulette", lang) for lang in langs]),
        roulette
    ))
    app.add_handler(MessageHandler(
        filters.Text([get_text("menu_inventory", lang) for lang in langs]),
        show_inventory
    ))
    app.add_handler(MessageHandler(
        filters.Text([get_text("menu_shop", lang) for lang in langs]),
        show_shop
    ))
    app.add_handler(MessageHandler(
        filters.Text([get_text("menu_box", lang) for lang in langs]),
        show_box
    ))
    app.add_handler(MessageHandler(
        filters.Text([get_text("menu_money", lang) for lang in langs]),
        show_money
    ))
    app.add_handler(MessageHandler(
        filters.Text([get_text("menu_lang", lang) for lang in langs]),
        ask_language
    ))
    app.add_handler(MessageHandler(
        filters.Text([get_text("menu_back", lang) for lang in langs]),
        handle_return
    ))

    # ✅ Choix contextuels (ex: Pokéballs)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_choice))

    # ✅ Commandes inconnues
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("🤖 Bot démarré.")
    app.run_polling()
