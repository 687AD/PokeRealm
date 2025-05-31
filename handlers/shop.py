from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.items import BALL_COSTS, ITEM_COSTS, CATEGORIES_ITEMS, GENERAL_ITEMS, buy_item, CATEGORY_NAMES, SHOP_CATEGORY_PREFIX, ITEMS
from core.lang import get_text
from utils.buttons import main_menu

# Emojis par catégorie
CATEGORY_EMOJIS = {
    "Poké Balls": "🎯",
    "Objets spéciaux": "✨",
    "Soins": "❤️",
    "Statuts": "🧪",
    "PP & Boissons": "🥤",
    "Boosts de combat": "⚔️",
    "Exploration": "🧭",
    "Entraînement / EV": "📘",
    "Objets tenus": "🎒"
}
#emoji d'items
ITEM_EMOJIS = {
    "pokeball": "🔴",
    "superball": "🔵",
    "hyperball": "🟡",
    "masterball": "🟣",
    "chroma": "🌈",
    "multi_exp": "⛓️",
    "piece_rune": "💰",
    "potion": "🧴",
    "super_potion": "🧪",
    "hyper_potion": "💉",
    "max_potion": "🧬",
    "revive": "💀",
    "max_revive": "👻",
    "full_restore": "💊",
    "antidote": "🍃",
    "paralyze_heal": "⚡",
    "burn_heal": "🔥",
    "ice_heal": "❄️",
    "awakening": "😴",
    "full_heal": "💠",
    "ether": "🔋",
    "elixir": "💧",
    "lemonade": "🍋",
    "x_attack": "💥",
    "x_defense": "🛡️",
    "x_speed": "💨",
    "x_special": "🔮",
    "x_sp_def": "🧠",
    "x_accuracy": "🎯",
    "guard_spec": "🛑",
    "repel": "🚫",
    "super_repel": "🚷",
    "max_repel": "⛔",
    "escape_rope": "🪢",
    "rare_candy": "🍬",
    "pp_up": "🔝",
    "hp_up": "❤️",
    "protein": "🥩",
    "iron": "🧲",
    "calcium": "🥛",
    "zinc": "⚙️",
    "carbos": "🍞",
    "casque_brut": "🪖",
    "restes": "🍽️",
    "bandeau_choix": "🎗️",
    "lunettes_choix": "🕶️",
    "mouchoir_choix": "🧣",
    "orbe_vie": "🔴",
    "ceinture_force": "🥋",
    "oeuf_chance": "🥚",
}

def build_category_keyboard(lang):
    keyboard = []
    for category in CATEGORIES_ITEMS.keys():
        emoji = CATEGORY_EMOJIS.get(category, "📦")
        label = CATEGORY_NAMES.get(category, {}).get(lang, category)
        keyboard.append([f"{emoji} {label}"])
    keyboard.append([get_text("back_button", lang)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def build_items_keyboard(category, lang):
    keyboard = []
    for item in CATEGORIES_ITEMS.get(category, []):
        label = ITEMS.get(item, {}).get(lang, item).capitalize()
        emoji = ITEM_EMOJIS.get(item, "📦")
        cost = BALL_COSTS.get(item) or ITEM_COSTS.get(item) or GENERAL_ITEMS.get(item, {}).get("cost", "?")
        keyboard.append([f"{emoji} {label} - {cost}💰"])
    keyboard.append([get_text("back_button", lang)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

async def show_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = load_user(update.effective_user.id).get("lang", "fr")
    context.user_data.update({"state": "shop_category", "selected_category": None, "pending_item": None})
    await update.message.reply_text(get_text("shop_select_category", lang), reply_markup=build_category_keyboard(lang))

async def handle_shop_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    text = update.message.text.strip()

    # 🔙 Retour
    if text == get_text("back_button", lang):
        if context.user_data.get("pending_item"):
            # Retour depuis le choix de quantité
            category = context.user_data.get("selected_category")
            context.user_data["pending_item"] = None
            context.user_data["state"] = "shop_items"
            await update.message.reply_text(get_text("shop_select_item", lang), reply_markup=build_items_keyboard(category, lang))
            return
        if context.user_data.get("selected_category"):
            context.user_data.update({"selected_category": None, "state": "shop_category"})
            await update.message.reply_text(get_text("shop_select_category", lang), reply_markup=build_category_keyboard(lang))
        else:
            context.user_data.clear()
            await update.message.reply_text(get_text("back_to_menu", lang), reply_markup=main_menu(lang))
        return

    # Quantité d’achat
    if context.user_data.get("pending_item"):
        if not text.isdigit():
            await update.message.reply_text(get_text("invalid_number", lang))
            return
        quantity = int(text)
        item = context.user_data["pending_item"]
        price = (BALL_COSTS.get(item) or ITEM_COSTS.get(item) or GENERAL_ITEMS.get(item, {}).get("cost", 0)) * quantity
        if data["money"] >= price:
            buy_item(data, item, quantity)
            save_user(user.id, data)
            context.user_data.clear()
            await update.message.reply_text(
                get_text("purchase_confirm", lang, item=ITEMS.get(item, {}).get(lang, item), quantity=quantity, price=price),
                reply_markup=main_menu(lang)
            )
        else:
            await update.message.reply_text(get_text("not_enough_money", lang))
        return

    # Sélection d’une catégorie
    if context.user_data.get("state") == "shop_category":
        for category in CATEGORIES_ITEMS:
            full_label = f"{CATEGORY_EMOJIS.get(category, '📦')} {CATEGORY_NAMES.get(category, {}).get(lang, category)}"
            if text.lower() == full_label.lower():
                context.user_data.update({"selected_category": category, "state": "shop_items"})
                await update.message.reply_text(get_text("shop_select_item", lang), reply_markup=build_items_keyboard(category, lang))
                return
        await update.message.reply_text(get_text("item_unknown", lang))
        return

    # Sélection d’un objet
    if context.user_data.get("state") == "shop_items":
        for item in CATEGORIES_ITEMS.get(context.user_data.get("selected_category"), []):
            label = ITEMS.get(item, {}).get(lang, item).capitalize()
            emoji = ITEM_EMOJIS.get(item, "📦")
            cost = BALL_COSTS.get(item) or ITEM_COSTS.get(item) or GENERAL_ITEMS.get(item, {}).get("cost", "?")
            full_label = f"{emoji} {label} - {cost}💰".lower()
            if text.lower() == full_label:
                context.user_data["pending_item"] = item
                await update.message.reply_text(get_text("enter_quantity", lang))
                return

    await update.message.reply_text(get_text("item_unknown", lang))