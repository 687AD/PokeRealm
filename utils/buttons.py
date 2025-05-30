from telegram import ReplyKeyboardMarkup

def main_menu(lang="fr"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [("🎰 Roulette" if lang == "fr" else "🎰 Catch"), ("🎒 Sac" if lang == "fr" else "🎒 Bag")],
            [("📦 Boîte Pokémon" if lang == "fr" else "📦 PokéBox"), ("🛒 Boutique" if lang == "fr" else "🛒 Shop")],
            [("👥 Mon équipe" if lang == "fr" else "👥 My Team")],
            [("📖 Aide" if lang == "fr" else "📖 Help")]
        ],
        resize_keyboard=True
    )
