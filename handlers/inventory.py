# handlers/inventory.py

from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user
from core.translation_data import ITEMS

async def show_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    pokeballs = data.get("pokeballs", {})
    items = data.get("items", {})

    text = "🎒 INVENTAIRE\n\n🎯 Pokéballs :\n"
    for ball in ["pokeball", "superball", "hyperball", "masterball"]:
        label = ITEMS.get(ball, {}).get(lang, ball)
        count = pokeballs.get(ball, 0)
        text += f"• {label} : {count}\n"

    text += "\n🔮 Objets :\n"
    for obj in ["chroma", "multi_exp"]:
        label = ITEMS.get(obj, {}).get(lang, obj)
        count = items.get(obj, 0)
        text += f"• {label} : {count}\n"

    await update.message.reply_text(text)
