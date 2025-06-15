from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user

ADMINS = [2142091056]  # remplace avec ton vrai ID

async def give_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_user.id

    if sender_id not in ADMINS:
        await update.message.reply_text("🚫 Tu n'as pas la permission d'utiliser cette commande.")
        return

    # Vérifie le montant donné
    try:
        amount = int(context.args[-1])  # le dernier argument est toujours le montant
    except (IndexError, ValueError):
        await update.message.reply_text("❗ Utilisation : /give @username <montant> ou en réponse à un message.")
        return

    # Récupération du destinataire
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
    elif context.args and context.args[0].startswith("@"):
        username = context.args[0][1:]
        # Recherche du user par username dans Telegram => Pas possible sans base interne
        # donc on affiche un message d'erreur
        await update.message.reply_text("❗ Impossible de cibler un utilisateur par @. Utilise une réponse à un message ou redis ce message une fois que le joueur a interagi avec le bot.")
        return
    else:
        target_user = update.effective_user  # Par défaut l'admin se donne à lui-même

    target_id = target_user.id
    user_data = load_user(target_id)
    user_data["money"] = user_data.get("money", 0) + amount
    save_user(target_id, user_data)

    if target_id == sender_id:
        await update.message.reply_text(f"💸 Tu t'es donné {amount} Pokédollars. Solde total : {user_data['money']}")
    else:
        await update.message.reply_text(f"💸 Tu as donné {amount} Pokédollars à {target_user.first_name} (solde : {user_data['money']})")
