from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user
from utils.buttons import main_menu

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    text = {
        "fr": (
            "📖 *Commandes disponibles :*\n\n"
            "/start \\- Redémarrer le bot\n"
            "/lang \\- Changer la langue\n"
            "/daily \\- Récompense quotidienne\n"
            "/money \\- Voir votre argent\n"
            "/nature \\<NomPokémon\\> \\<Nature\\> \\- Changer la nature d’un Pokémon principal \\(ex : `/nature Salamèche Modeste`\\)\n"
            "/stats \\<NomPokémon\\> \\- Voir les statistiques réelles du Pokémon principal \\(ex : `/stats Pikachu`\\)\n"
            "/team \\<1\\-6\\> \\<NomPokémon\\> \\- Placer un Pokémon à une position de ton équipe \\(ex : `/team 1 Bulbizarre`\\)\n"
            "/show\\_team \\- Afficher ton équipe Pokémon actuelle\n"
            "/sell\\_duplicates \\- Vendre les doublons automatiquement"
        ),
        "en": (
            "📖 *Available commands:*\n\n"
            "/start \\- Restart the bot\n"
            "/lang \\- Change language\n"
            "/daily \\- Claim your daily reward\n"
            "/money \\- Check your money\n"
            "/nature \\<PokemonName\\> \\<Nature\\> \\- Change your main Pokémon's nature \\(e\\.g\\. `/nature Charmander Modest`\\)\n"
            "/stats \\<PokemonName\\> \\- View your main Pokémon’s real stats \\(e\\.g\\. `/stats Pikachu`\\)\n"
            "/team \\<1\\-6\\> \\<PokemonName\\> \\- Put a Pokémon in a slot of your team \\(e\\.g\\. `/team 1 Bulbasaur`\\)\n"
            "/show\\_team \\- Display your current Pokémon team\n"
            "/sell\\_duplicates \\- Automatically sell duplicates"
        )
    }
    await update.message.reply_text(
        text.get(lang, text["fr"]),
        parse_mode="MarkdownV2",
        reply_markup=main_menu(lang)
    )
