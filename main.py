from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)

from handlers.profile import profile_command
from handlers.spawn import spawn
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
from handlers.box import show_box, sell_duplicates, handle_box_choice, handle_sort_choice
from utils.buttons import main_menu
from core.user_data import load_user
from core.lang import get_text
from handlers.nature import handle_nature_command
from handlers.help import help_command
from handlers.stats import handle_stats_command
from handlers.team import handle_team_command, show_team_command
from handlers.ability import ability_command
from handlers.pokedex import pokedex_command, handle_pokedex_sort_choice, handle_pokedex_back


# ✅ Routeur texte intelligent
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    state = context.user_data.get("state")

    # 🧭 Navigation générique
    prev_texts = [get_text("previous_page", l).lower() for l in ["fr", "en"]] + ["⬅️ page précédente", "précédent", "previous", "🔼"]
    next_texts = [get_text("next_page", l).lower() for l in ["fr", "en"]] + ["➡️ page suivante", "suivant", "next", "▶"]

    # 📖 Pokédex navigation (🔁 doit venir en premier)
    if context.user_data.get("pokedex_page") is not None and (text in prev_texts or text in next_texts):
        from handlers.pokedex import handle_pokedex_navigation
        await handle_pokedex_navigation(update, context)
        return

    # 📦 Shop navigation
    if state and state.startswith("shop") and (text in prev_texts or text in next_texts):
        await handle_shop_selection(update, context)
        return

    # 📁 Box navigation
    if (state == "box" or context.user_data.get("box_page") is not None) and (text in prev_texts or text in next_texts):
        await handle_sort_choice(update, context)
        return

    # 📦 Shop prioritaire
    if state in ["shop_category", "shop_items"] or context.user_data.get("pending_item"):
        await handle_shop_selection(update, context)
        return

    # 📁 Box manuelle (uniquement si pas en shop)
    if text in ["📁 box", "📁 Box"] and not state.startswith("shop"):
        context.user_data["state"] = "box"
        await show_box(update, context)
        return

    # 📖 Tri du Pokédex
    if context.user_data.get("awaiting_pokedex_sort"):
        from handlers.pokedex import handle_pokedex_sort_choice
        await handle_pokedex_sort_choice(update, context)
        return

    # 🧮 Tri de la box
    if context.user_data.get("awaiting_sort_choice") or any(k in text for k in ["nom", "rareté", "niveau", "pokédex", "shiny", "iv"]):
        await handle_sort_choice(update, context)
        return

    # 🔄 Logique par défaut
    await handle_choice(update, context)

TOKEN = "7300187027:AAHWwvyvZKMN0VbCBTkeceIUDfO9-97h0eE"

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
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(CommandHandler("profil", profile_command))
    app.add_handler(CommandHandler("pokedex", pokedex_command))
    app.add_handler(CommandHandler("spawn", spawn))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("lang", ask_language))
    app.add_handler(CommandHandler("money", show_money))
    app.add_handler(CommandHandler("nature", handle_nature_command))
    app.add_handler(CommandHandler("sell_duplicates", sell_duplicates))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", handle_stats_command))
    app.add_handler(CommandHandler("team", handle_team_command))
    app.add_handler(CommandHandler("show_team", show_team_command))
    app.add_handler(CommandHandler("ability", ability_command))
    app.add_handler(CommandHandler("pay", pay))

    # ✅ Boutons textes
    app.add_handler(MessageHandler(filters.Text(["📊 Trier le Pokédex"]), handle_pokedex_sort_choice))
    app.add_handler(MessageHandler(filters.Text(["⬅️ Retour"]), handle_pokedex_back))
    app.add_handler(MessageHandler(filters.Text([get_text("button_sort_box", lang) for lang in langs]), handle_sort_choice))
    app.add_handler(MessageHandler(filters.Regex("^👥 Mon équipe$"), show_team_command))
    app.add_handler(MessageHandler(filters.Regex("^👥 My Team$"), show_team_command))
    app.add_handler(MessageHandler(filters.Text([get_text("menu_help", lang) for lang in langs]), help_command))
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
