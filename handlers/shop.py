# handlers/shop.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.items import BALL_COSTS, ITEM_COSTS, buy_item
from core.translation_data import ITEMS
from core.lang import get_text
from utils.buttons import main_menu

SHOP_ITEMS = list(BALL_COSTS.keys()) + list(ITEM_COSTS.keys())

def build_shop_keyboard(lang):
    return ReplyKeyboardMarkup(
        [[ITEMS[i][lang].capitalize()] for i in SHOP_ITEMS] + [["🔙 Retour"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def show_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    context.user_data["state"] = "shop"
    context.user_data["pending_item"] = None

    text = get_text("shop_intro", lang)
    for item in SHOP_ITEMS:
        label = ITEMS[item][lang]
        price = BALL_COSTS.get(item) or ITEM_COSTS.get(item)
        text += f"• {label} — {price}💰\n"

    text += "\n" + get_text("shop_instruction", lang)
    await update.message.reply_text(text, reply_markup=build_shop_keyboard(lang))

async def handle_shop_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    text = update.message.text.lower()

    # 🔙 Retour
    if "retour" in text or "back" in text:
        context.user_data["state"] = None
        context.user_data["pending_item"] = None
        await update.message.reply_text(get_text("back_to_menu", lang), reply_markup=main_menu(lang))
        return

    # attente de quantité
    if context.user_data.get("pending_item"):
        item = context.user_data["pending_item"]
        try:
            quantity = int(text)
        except ValueError:
            await update.message.reply_text(get_text("invalid_number", lang))
            return

        price = (BALL_COSTS.get(item) or ITEM_COSTS.get(item)) * quantity
        if data["money"] >= price:
            buy_item(data, item, quantity)
            save_user(user.id, data)
            context.user_data["pending_item"] = None
            context.user_data["state"] = None
            await update.message.reply_text(
                get_text("purchase_confirm", lang, item=ITEMS[item][lang], quantity=quantity, price=price),
                reply_markup=main_menu(lang)
            )
        else:
            await update.message.reply_text(get_text("not_enough_money", lang))
        return

    # choix d'un objet
    for key, val in ITEMS.items():
        if text == val[lang].lower():
            context.user_data["pending_item"] = key
            await update.message.reply_text(get_text("enter_quantity", lang))
            return

    await update.message.reply_text(get_text("item_unknown", lang))
