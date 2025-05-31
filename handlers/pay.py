import os
from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import get_and_update_user, load_user, save_user, DATA_DIR
from core.lang import get_text

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user
    sender_data = get_and_update_user(sender.id, sender.username)
    lang = sender_data.get("lang", "fr")

    args = context.args
    if len(args) != 2:
        await update.message.reply_text(get_text("pay_usage", lang))
        return

    username = args[0].lstrip('@').lower()

    try:
        amount = int(args[1])
        if amount <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text(get_text("pay_invalid_amount", lang))
        return

    if sender_data["money"] < amount:
        await update.message.reply_text(get_text("pay_not_enough", lang))
        return

    # Recherche du destinataire dans tous les fichiers utilisateur
    receiver_id = None
    for filename in os.listdir(DATA_DIR):
        user_id = filename.replace(".json", "")
        data = load_user(user_id)
        if data.get("username", "").lower() == username:
            receiver_id = user_id
            break

    if receiver_id is None:
        await update.message.reply_text(get_text("pay_user_not_found", lang))
        return

    # Effectuer le transfert
    receiver_data = load_user(receiver_id)
    receiver_data["money"] += amount
    sender_data["money"] -= amount

    save_user(sender.id, sender_data)
    save_user(receiver_id, receiver_data)

    await update.message.reply_text(
        get_text("pay_success", lang).format(user=username, amount=amount)
    )
