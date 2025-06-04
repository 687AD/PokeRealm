from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from core.user_data import load_user
from core.pokemon_data import POKEMON_NAMES
from handlers.box import POKEDEX_ORDER
from utils.buttons import main_menu

SORT_OPTIONS = [
    ("pokedex", "📚 Pokédex"),
    ("name", "🔤 Nom"),
]

ITEMS_PER_PAGE = 30

def get_all_pokemon_names(lang):
    names = [(k, POKEMON_NAMES[k].get(lang, k)) for k in POKEMON_NAMES]
    names = sorted(names, key=lambda x: POKEDEX_ORDER.get(x[0], 9999))
    return names


def get_pokemon_owned_sets(data):
    """Retourne deux sets : (possédés, shiny possédés)"""
    normal = set()
    shiny = set()
    for pkm in data.get("box", []):
        name = pkm["name"]
        if name.startswith("shiny_"):
            shiny.add(name.replace("shiny_", ""))
        else:
            normal.add(name)
    return normal, shiny

def build_pokedex_keyboard(lang, page, max_page):
    kb = [["📊 Trier le Pokédex"]]  # bouton tri en premier

    nav = []
    if page > 0:
        nav.append("⬅️ Page précédente")
    if page < max_page:
        nav.append("➡️ Page suivante")
    if nav:
        kb.append(nav)

    kb.append(["⬅️ Retour"])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

async def pokedex_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    args = context.args if hasattr(context, "args") and context.args else []

    all_pokemon = get_all_pokemon_names(lang)
    owned, shiny_owned = get_pokemon_owned_sets(data)

    # Tri : /pokedex nom
    sort_type = context.user_data.get("pokedex_sort", "pokedex")
    page = 0

    for arg in args:
        if arg.isdigit():
            page = int(arg)
        elif arg.lower() in ["nom", "name"]:
            sort_type = "name"

    if sort_type == "name":
        all_pokemon = sorted(all_pokemon, key=lambda x: x[1])

    lines = []
    total = len(all_pokemon)
    caught = 0
    shiny_caught = 0

    for key, name in all_pokemon:
        has_normal = key in owned
        has_shiny = key in shiny_owned
        emoji = "✅" if has_normal else "❌"
        shiny_emoji = "✨" if has_shiny else ""
        line = f"{emoji}{shiny_emoji} {name}"
        lines.append(line)
        if has_normal:
            caught += 1
        if has_shiny:
            shiny_caught += 1

    max_page = (len(lines) - 1) // ITEMS_PER_PAGE
    page = max(0, min(page, max_page))
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE

    header = f"📖 Pokédex : {caught}/{total} capturés, {shiny_caught} shiny"
    subheader = f"📄 Page {page + 1}/{max_page + 1}"

    context.user_data["pokedex_page"] = page
    context.user_data["pokedex_args"] = args

    await update.message.reply_text(
        f"{header}\n{subheader}\n\n" + "\n".join(lines[start_index:end_index]),
        reply_markup=build_pokedex_keyboard(lang, page, max_page)
    )

async def handle_pokedex_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    text = update.message.text.strip().lower()

    if "pokedex_page" not in context.user_data:
        context.user_data["pokedex_page"] = 0
    page = context.user_data["pokedex_page"]

    next_texts = ["➡️ page suivante", "suivant", "next", "▶"]
    prev_texts = ["⬅️ page précédente", "précédent", "previous", "🔼"]

    if any(t in text for t in next_texts):
        context.user_data["pokedex_page"] = page + 1
    elif any(t in text for t in prev_texts):
        context.user_data["pokedex_page"] = max(0, page - 1)
    else:
        return  # ignore unrelated messages

    args = context.user_data.get("pokedex_args", [])
    # injecte la page dans les arguments
    args = [arg for arg in args if not arg.isdigit()] + [str(context.user_data["pokedex_page"])]
    context.args = args
    await pokedex_command(update, context)

async def handle_pokedex_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    context.user_data.pop("pokedex_page", None)
    context.user_data.pop("pokedex_args", None)
    await update.message.reply_text("⬅️ Retour au menu principal.", reply_markup=main_menu(lang))

def build_sort_pokedex_keyboard(lang):
    return ReplyKeyboardMarkup(
        [[label] for _, label in SORT_OPTIONS] + [["⬅️ Retour"]],
        resize_keyboard=True
    )

async def handle_pokedex_sort_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = load_user(user.id).get("lang", "fr")
    text = update.message.text.strip().lower()

    if context.user_data.get("awaiting_pokedex_sort"):
        for key, label in SORT_OPTIONS:
            if label.lower() in text or key in text:
                context.user_data["pokedex_sort"] = key
                context.user_data["awaiting_pokedex_sort"] = False
                return await pokedex_command(update, context)
        await update.message.reply_text("❌ Choix invalide.", reply_markup=build_sort_pokedex_keyboard(lang))
        return

    context.user_data["awaiting_pokedex_sort"] = True
    await update.message.reply_text("📊 Choisis un tri :", reply_markup=build_sort_pokedex_keyboard(lang))