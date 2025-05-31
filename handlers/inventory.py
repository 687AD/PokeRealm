from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user
from core.items import CATEGORIES_ITEMS, CATEGORY_NAMES, ITEMS
from handlers.shop import CATEGORY_EMOJIS, ITEM_EMOJIS

async def show_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    pokeballs = data.get("pokeballs", {})
    items = data.get("items", {})

    title = "🎒 *INVENTORY*" if lang == "en" else "🎒 *INVENTAIRE*"
    text = f"{title}\n\n"

    # 🎯 Poké Balls
    category = "Poké Balls"
    emoji = CATEGORY_EMOJIS.get(category, "📦")
    translated = CATEGORY_NAMES.get(category, {}).get(lang, category)
    text += f"{emoji} *{translated}* :\n"
    for ball in CATEGORIES_ITEMS.get(category, []):
        label = ITEMS.get(ball, {}).get(lang, ball)
        icon = ITEM_EMOJIS.get(ball, "")
        count = pokeballs.get(ball, 0)
        text += f"{icon} {label} : {count}\n"

    # 📦 Autres catégories
    for raw_category, keys in CATEGORIES_ITEMS.items():
        if raw_category == "Poké Balls":
            continue

        section_items = []
        for key in keys:
            if key in items and items[key] > 0:
                label = ITEMS.get(key, {}).get(lang, key)
                icon = ITEM_EMOJIS.get(key, "")
                section_items.append(f"{icon} {label} : {items[key]}")

        if section_items:
            emoji = CATEGORY_EMOJIS.get(raw_category, "📦")
            translated = CATEGORY_NAMES.get(raw_category, {}).get(lang, raw_category)
            text += f"\n\n{emoji} *{translated}* :\n" + "\n".join(section_items)

    await update.message.reply_text(text, parse_mode="Markdown")