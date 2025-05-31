from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)

from handlers.spawn import spawn
from handlers.trade import propose_trade
from handlers.confirm_trade import confirm_trade
from handlers.callbacks_trade import handle_trade_callback
from handlers.pay import pay
from handlers.lang import ask_language, handle_language_choice
from handlers.choice import handle_choice
from handlers.start import start
from handlers.daily import daily
from handlers.roulette import roulette, handle_ball_choice
from handlers.inventory import show_inventory
from handlers.shop import show_shop, handle_shop_selection
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
from handlers.ability import ability_command
from handlers.fight import fight, handle_fight_response
from core.battle_engine import handle_attack_selection

# ✅ Routeur texte intelligent
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    state = context.user_data.get("state")

    # Priorité au shop
    if (isinstance(state, str) and state.startswith("shop")) or context.user_data.get("pending_item"):
        await handle_shop_selection(update, context)
        return

    # Détection de tri box
    if any(k in text for k in ["nom", "rareté", "niveau", "pokédex", "shiny", "iv"]):
        await handle_sort_choice(update, context)
        return

    # Sinon : logique par défaut
    await handle_choice(update, context)

TOKEN = "8171438159:AAEC58M69Ddxprn645xTO-WuakzABqJnEUA"

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    async def handle_return(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        data = load_user(user.id)
        lang = data.get("lang", "fr")
        await update.message.reply_text("⬅️ Retour au menu principal.", reply_markup=main_menu(lang))
        context.user_data.clear()

    langs = ["fr", "en"]

    # ✅ Commandes
    app.add_handler(CommandHandler("spawn", spawn))
    app.add_handler(CommandHandler("fight", fight))
    app.add_handler(CallbackQueryHandler(handle_fight_response, pattern="^(accept_fight|decline_fight):"))
    app.add_handler(CallbackQueryHandler(handle_attack_selection, pattern="^move:"))
    app.add_handler(CommandHandler("trade", propose_trade))
    app.add_handler(CommandHandler("confirmtrade", confirm_trade))
    app.add_handler(CallbackQueryHandler(handle_trade_callback, pattern="^(accept_trade|refuse_trade):"))
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
    app.add_handler(CommandHandler("ability", ability_command))
    app.add_handler(CommandHandler("pay", pay))

    # ✅ Boutons textes
    app.add_handler(MessageHandler(filters.Regex("^👥 Mon équipe$"), show_team_command))
    app.add_handler(MessageHandler(filters.Regex("^👥 My Team$"), show_team_command))
    app.add_handler(MessageHandler(filters.Text([get_text("menu_help", lang) for lang in langs]), help_command))
    app.add_handler(MessageHandler(filters.Text(["🔼 Page précédente", "🔽 Page suivante"]), handle_box_navigation))
    app.add_handler(MessageHandler(filters.Text([get_text("button_sort_box", lang) for lang in langs]), handle_sort_choice))
    app.add_handler(MessageHandler(filters.Text(["📁 Box"]), show_box))
    app.add_handler(MessageHandler(filters.Text(["🗑️ Sell duplicates", "🗑️ Vendre les doublons"]), handle_box_choice))
    app.add_handler(MessageHandler(filters.Text([get_text("button_sell_duplicates", lang) for lang in langs]), sell_duplicates))
    app.add_handler(MessageHandler(filters.Regex("(?i)(français|english)"), handle_language_choice))
    app.add_handler(MessageHandler(filters.Text([get_text("menu_roulette", lang) for lang in langs]), roulette))
    app.add_handler(MessageHandler(filters.Text([get_text("menu_inventory", lang) for lang in langs]), show_inventory))
    app.add_handler(MessageHandler(filters.Text([get_text("menu_shop", lang) for lang in langs]), show_shop))
    app.add_handler(MessageHandler(filters.Text([get_text("menu_box", lang) for lang in langs]), show_box))
    app.add_handler(MessageHandler(filters.Text([get_text("menu_money", lang) for lang in langs]), show_money))
    app.add_handler(MessageHandler(filters.Text([get_text("menu_lang", lang) for lang in langs]), ask_language))
    app.add_handler(MessageHandler(filters.Text([get_text("menu_back", lang) for lang in langs]), handle_return))

    # ✅ Routeur texte libre
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # ✅ Inconnues
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("🤖 Bot démarré.")
    app.run_polling()
