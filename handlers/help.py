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
            "/daily \\- Réclamer la récompense quotidienne\n"
            "/money \\- Voir ton argent\n"
            "/ability \\<Nom\\> \\<Talent\\> \\- Changer le talent actif du Pokémon séléctionner\n"
            "/nature \\<Nom\\> \\<Nature\\> \\- Changer la nature du Pokémon séléctionner\n"
            "/stats \\<Nom\\> \\- Voir les stats réelles du Pokémon séléctionner\n"
            "/team \\<1\\-6\\> \\<Nom\\> \\- Placer un Pokémon dans ton équipe\n"
            "/pay \\<@pseudo\\> \\<Montant\\> \\- Envoyer des Pokédollars\n"
            "/profile \\- Visionnez ses infos\n"
        ),
        "en": (
            "📖 *Available commands:*\n\n"
            "/start \\- Restart the bot\n"
            "/lang \\- Change language\n"
            "/daily \\- Claim your daily reward\n"
            "/money \\- Check your money\n"
            "/ability \\<Name\\> \\<Ability\\> \\- Change the active ability of your Pokemon\n"
            "/nature \\<Name\\> \\<Nature\\> \\- Change nature of your Pokemon\n"
            "/stats \\<Name\\> \\- View Pokemon stats\n"
            "/team \\<1\\-6\\> \\<Name\\> \\- Assign Pokémon to your team\n"
            "/pay \\<@user\\> \\<Amount\\> \\- Send Pokedollars\n"
            "/profile \\- View our infos\n"
        )
    }

    await update.message.reply_text(
        text.get(lang, text["fr"]),
        parse_mode="MarkdownV2",
        reply_markup=main_menu(lang)
    )
