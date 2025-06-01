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
            "/sell\\_duplicates \\- Vendre automatiquement les doublons\n"
            "/ability \\<Nom\\> \\<Talent\\> \\- Changer le talent actif du Pokémon principal\n"
            "/nature \\<Nom\\> \\<Nature\\> \\- Changer la nature d’un Pokémon principal\n"
            "/stats \\<Nom\\> \\- Voir les stats réelles du Pokémon principal\n"
            "/team \\<1\\-6\\> \\<Nom\\> \\- Placer un Pokémon dans ton équipe\n"
            "/show\\_team \\- Afficher ton équipe actuelle\n"
            "/pay \\<@pseudo\\> \\<Montant\\> \\- Envoyer des Pokédollars\n"
            "/fight \\- Lancer un combat contre un autre joueur\n"
            "/trade \\<@pseudo\\> \\<Nom\\> \\- Proposer un échange de Pokémon\n"
        ),
        "en": (
            "📖 *Available commands:*\n\n"
            "/start \\- Restart the bot\n"
            "/lang \\- Change language\n"
            "/daily \\- Claim your daily reward\n"
            "/money \\- Check your money\n"
            "/sell\\_duplicates \\- Auto\\-sell duplicates\n"
            "/ability \\<Name\\> \\<Ability\\> \\- Change the active ability of your main Pokémon\n"
            "/nature \\<Name\\> \\<Nature\\> \\- Change nature of your main Pokémon\n"
            "/stats \\<Name\\> \\- View main Pokémon's real stats\n"
            "/team \\<1\\-6\\> \\<Name\\> \\- Assign Pokémon to your team\n"
            "/show\\_team \\- Show your current team\n"
            "/pay \\<@user\\> \\<Amount\\> \\- Send Pokédollars\n"
            "/fight \\- Start a battle against another player\n"
            "/trade \\<@user\\> \\<Name\\> \\- Propose a Pokémon trade\n"
        )
    }

    await update.message.reply_text(
        text.get(lang, text["fr"]),
        parse_mode="MarkdownV2",
        reply_markup=main_menu(lang)
    )
