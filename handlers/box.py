from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.translation_data import POKEMON_NAMES, NATURES
from core.lang import get_text
from utils.buttons import main_menu

ITEMS_PER_PAGE = 10

user_box_pages = {}

RARITY_ORDER = {"common": 0, "uncommon": 1, "rare": 2, "epic": 3, "legendary": 4}
RARITY_EMOJIS = {"common": "⚪", "uncommon": "🟢", "rare": "🔵", "epic": "🟣", "legendary": "🟡"}

POKEDEX_ORDER = {
    "Bulbasaur": 1, "Ivysaur": 2, "Venusaur": 3, "Charmander": 4, "Charmeleon": 5, "Charizard": 6,
    "Squirtle": 7, "Wartortle": 8, "Blastoise": 9, "Caterpie": 10, "Metapod": 11, "Butterfree": 12,
    "Weedle": 13, "Kakuna": 14, "Beedrill": 15, "Pidgey": 16, "Pidgeotto": 17, "Pidgeot": 18,
    "Rattata": 19, "Raticate": 20
}

def format_iv(iv_dict):
    return " / ".join([f"{k}:{v}" for k, v in iv_dict.items()])

def build_box_keyboard(lang, page, max_page):
    buttons = []
    if page > 0:
        buttons.append(get_text("previous_page", lang))
    if page < max_page:
        buttons.append(get_text("next_page", lang))
    nav_buttons = [btn for btn in buttons]
    return ReplyKeyboardMarkup(
        [
            [get_text("button_sort_box", lang)],
            [get_text("button_sell_duplicates", lang)],
            nav_buttons if nav_buttons else [],
            [get_text("menu_back", lang)]
        ],
        resize_keyboard=True
    )

async def show_box(update: Update, context: ContextTypes.DEFAULT_TYPE, page=0):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    box = data.get("box", [])
    if not box:
        await update.message.reply_text(get_text("box_empty", lang), reply_markup=main_menu(lang))
        return

    max_page = (len(box) - 1) // ITEMS_PER_PAGE
    page = max(0, min(page, max_page))
    user_box_pages[user.id] = page

    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE

    message = f"\U0001F4E6 *BOX* (Page {page + 1}/{max_page + 1})\n\n"

    for pkm in box[start_index:end_index]:
        name = POKEMON_NAMES.get(pkm["name"], {}).get(lang, pkm["name"])
        shiny_icon = "✨ " if pkm.get("shiny") else ""
        rarity = pkm.get("rarity", "common")
        rarity_emoji = RARITY_EMOJIS.get(rarity, "⚪")
        pokedex_number = POKEDEX_ORDER.get(pkm["name"], "?")
        nature = NATURES.get(pkm["nature"], {}).get(lang, pkm["nature"])
        known_natures = pkm.get("known_natures", [])
        if known_natures:
            known_text = ", ".join(NATURES.get(n, {}).get(lang, n) for n in known_natures)
            nature += f" ({known_text})"
        ivs_formatted = format_iv(pkm["ivs"])
        quantity = pkm.get("quantity", 1)
        level = pkm.get("level", 1)
        ability = pkm.get("ability", "❓")
        ha = pkm.get("hidden_ability", "❓")

        message += (
            f"{rarity_emoji} *#{pokedex_number} {shiny_icon}{name}*  _(x{quantity})_\n"
            f"Lvl: *{level}*  |  Nature: _{nature}_\n"
            f"Talent: _{ability}_  |  Caché: _{ha}_\n"
            f"IVs: `{ivs_formatted}`\n\n"
        )

    await update.message.reply_text(message.strip(), reply_markup=build_box_keyboard(lang, page, max_page), parse_mode="Markdown")

async def handle_box_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = load_user(user.id).get("lang", "fr")
    current_page = user_box_pages.get(user.id, 0)
    text = update.message.text

    if text == get_text("previous_page", lang):
        await show_box(update, context, page=current_page - 1)
    elif text == get_text("next_page", lang):
        await show_box(update, context, page=current_page + 1)

async def handle_box_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = load_user(user.id).get("lang", "fr")
    current_page = user_box_pages.get(user.id, 0)
    text = update.message.text

    if text == get_text("previous_page", lang):
        await show_box(update, context, page=current_page - 1)
    elif text == get_text("next_page", lang):
        await show_box(update, context, page=current_page + 1)

async def handle_box_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_sort_choice(update, context)
async def sell_duplicates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    box = data.get("box", [])
    if not box:
        await update.message.reply_text(get_text("box_empty", lang), reply_markup=main_menu(lang))
        return

    locked_map = {pkm["name"]: pkm for pkm in box if pkm.get("locked")}
    new_box = []
    stacked_iv = 0
    stacked_ha = False
    stacked_nature = 0
    sold_count = 0
    total_units_sold = 0
    sale_summary = {}

    for pkm in box:
        name = pkm["name"]

        if pkm.get("locked"):
            quantity = pkm.get("quantity", 1)
            if quantity > 1:
                rarity_value = {"common": 100, "uncommon": 250, "rare": 500, "epic": 1000, "legendary": 3000}
                reward = rarity_value.get(pkm.get("rarity", "common"), 100) * (quantity - 1)
                data["money"] += reward
                sold_count += reward
                total_units_sold += (quantity - 1)
                sale_summary[pkm["name"]] = sale_summary.get(pkm["name"], 0) + (quantity - 1)
                pkm["quantity"] = 1
            new_box.append(pkm)
            continue

        if pkm.get("shiny"):
            new_box.append(pkm)
            continue

        if name in locked_map:
            main = locked_map[name]
            for stat in pkm["ivs"]:
                if pkm["ivs"][stat] > main["ivs"].get(stat, 0):
                    main["ivs"][stat] = pkm["ivs"][stat]
                    stacked_iv += 1
            if pkm.get("ability") == pkm.get("hidden_ability") and main.get("ability") != main.get("hidden_ability"):
                main["ability"] = pkm["ability"]
                stacked_ha = True
            if pkm["nature"] not in main.get("known_natures", []):
                main.setdefault("known_natures", []).append(pkm["nature"])
                stacked_nature += 1
            qty = pkm.get("quantity", 1)
            rarity_value = {"common": 100, "uncommon": 250, "rare": 500, "epic": 1000, "legendary": 3000}
            reward = rarity_value.get(pkm.get("rarity", "common"), 100) * qty
            data["money"] += reward
            sold_count += reward
            total_units_sold += qty
            sale_summary[pkm["name"]] = sale_summary.get(pkm["name"], 0) + qty
        else:
            qty = pkm.get("quantity", 1)
            rarity_value = {"common": 100, "uncommon": 250, "rare": 500, "epic": 1000, "legendary": 3000}
            reward = rarity_value.get(pkm.get("rarity", "common"), 100) * qty
            data["money"] += reward
            sold_count += reward
            total_units_sold += qty
            sale_summary[pkm["name"]] = sale_summary.get(pkm["name"], 0) + qty

    data["box"] = new_box
    save_user(user.id, data)

    messages = []
    if sold_count > 0:
        messages.append(get_text("duplicates_sold", lang, money=sold_count))
    if stacked_iv > 0:
        messages.append(get_text("iv_stack_message", lang, count=stacked_iv))
    if stacked_ha:
        messages.append(get_text("hidden_ability_stack_message", lang))
    if stacked_nature > 0:
        messages.append(get_text("nature_stack_message", lang, count=stacked_nature))
    if not messages and total_units_sold == 0:
        messages.append(get_text("no_duplicates", lang))

    if sale_summary:
        messages.append("\n📦 Résumé des ventes :")
        for name, qty in sale_summary.items():
            unit_price = {"common": 100, "uncommon": 250, "rare": 500, "epic": 1000, "legendary": 3000}.get(
                next((p["rarity"] for p in box if p["name"] == name), "common"), 100
            )
            messages.append(f"- {name} x{qty} → +{unit_price * qty}💰")

    await update.message.reply_text("\n".join(messages), reply_markup=main_menu(lang))

async def handle_sort_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    if get_text("button_sell_duplicates", lang).lower() in text:
        await sell_duplicates(update, context)
    elif get_text("button_sort_box", lang).lower() in text:
        keyboard = ReplyKeyboardMarkup([
            ["🔤 Nom", "🔺 Rareté"],
            ["📉 Niveau", "📦 Pokédex"],
            ["✨ Shiny", "💯 IV total"],
            [get_text("menu_back", lang)]
        ], resize_keyboard=True)
        await update.message.reply_text(get_text("choose_sorting", lang), reply_markup=keyboard)
    elif "nom" in text:
        data["box"].sort(key=lambda x: POKEMON_NAMES.get(x["name"], {}).get(lang, x["name"]).lower())
        save_user(user.id, data)
        await show_box(update, context)
    elif "rareté" in text:
        data["box"].sort(key=lambda x: RARITY_ORDER.get(x.get("rarity", "common"), 4), reverse=True)
        save_user(user.id, data)
        await show_box(update, context)
    elif "niveau" in text:
        data["box"].sort(key=lambda x: x.get("level", 1), reverse=True)
        save_user(user.id, data)
        await show_box(update, context)
    elif "pokédex" in text:
        data["box"].sort(key=lambda x: POKEDEX_ORDER.get(x.get("name"), 9999))
        save_user(user.id, data)
        await show_box(update, context)
    elif "shiny" in text:
        data["box"].sort(key=lambda x: not x.get("shiny", False))
        save_user(user.id, data)
        await show_box(update, context)
    elif "iv" in text:
        data["box"].sort(key=lambda x: sum(x.get("ivs", {}).values()), reverse=True)
        save_user(user.id, data)
        await show_box(update, context)
    else:
        await show_box(update, context)

async def handle_box_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_sort_choice(update, context)
