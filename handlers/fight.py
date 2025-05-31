from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.user_data import load_user
from core.lang import get_text
from core.battle_state import active_battles, create_battle_state
import asyncio

pending_fights = {}

async def fight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    challenger = update.effective_user
    if not context.args or not context.args[0].startswith("@"):
        await update.message.reply_text("❌ Mentionne un joueur : /fight @pseudo")
        return

    target_username = context.args[0][1:]

    # 🔁 Remplacement de get_chat par une recherche locale
    target_user_id = None
    for user_id, user_data in context.application.user_data.items():
        if user_data.get("username") == target_username:
            target_user_id = user_id
            break

    if not target_user_id:
        await update.message.reply_text("❌ Ce joueur n’a pas encore utilisé le bot.")
        return

    if target_username in pending_fights:
        await update.message.reply_text("⏳ Ce joueur a déjà une demande en attente.")
        return

    pending_fights[target_username] = {
        "challenger_id": challenger.id,
        "challenger_username": challenger.username,
        "message_id": None
    }

    # Message + boutons
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Accepter", callback_data=f"accept_fight:{challenger.id}"),
            InlineKeyboardButton("❌ Refuser", callback_data=f"decline_fight:{challenger.id}")
        ]
    ])
    msg = await context.bot.send_message(
        chat_id=target_user_id,
        text=f"⚔️ @{challenger.username} te défie en duel Pokémon !",
        reply_markup=keyboard
    )
    pending_fights[target_username]["message_id"] = msg.message_id

    # Timeout 60 sec
    await asyncio.sleep(60)
    if target_username in pending_fights:
        await context.bot.edit_message_text(
            chat_id=target_user_id,
            message_id=msg.message_id,
            text="⌛ Défi expiré."
        )
        del pending_fights[target_username]

async def handle_fight_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    action, challenger_id = data.split(":")
    challenger_id = int(challenger_id)
    responder = update.effective_user

    if responder.username not in pending_fights:
        await query.edit_message_text("❌ Ce défi n'est plus actif.")
        return

    if action == "decline_fight":
        await query.edit_message_text("🚫 Défi refusé.")
        del pending_fights[responder.username]
        return

    if action == "accept_fight":
        await query.edit_message_text("✅ Défi accepté ! Le combat commence...")
        del pending_fights[responder.username]
        # Création de l'état de combat
        await create_battle_state(context, challenger_id, responder.id)
