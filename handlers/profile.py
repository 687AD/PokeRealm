from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user
from datetime import datetime

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)

    balls_used = data.get("balls_used", {"pokeball": 0, "superball": 0, "hyperball": 0, "masterball": 0})
    pokemons_captured = data.get("pokemons_captured", 0)
    pokemons_sold = data.get("pokemons_sold", 0)
    pokemons_fled = data.get("pokemons_fled", 0)
    shiny_charms = data.get("shiny_charms", 0)
    shiny_base_rate = 1 / 4096
    shiny_bonus = shiny_charms * 0.05
    shiny_rate = shiny_base_rate * (1 - shiny_bonus)
    money_bonus = data.get("money_bonus", 0)
    total_money = data.get("money", 0)
    total_earned_money = data.get("total_earned_money", total_money)
    total_captured = pokemons_captured + pokemons_sold
    shiny_chance = int(1 / shiny_rate) if shiny_rate > 0 else "∞"
    nb_shinies = data.get("nb_shinies", 0)
    nb_mythics = data.get("nb_mythics", 0)
    max_streak = data.get("max_streak", 0)
    nb_trades = data.get("nb_trades", 0)

    # Âge du compte en jours
    creation_date_str = data.get("creation_date")
    if creation_date_str:
        try:
            creation_date = datetime.strptime(creation_date_str, "%Y-%m-%d")
            account_age_days = (datetime.utcnow() - creation_date).days
        except Exception:
            account_age_days = "?"
    else:
        account_age_days = "?"

    name = user.first_name

    message = (
        f"👤 *Profil de {name}*\n\n"
        f"💰 *Pokédollars* : {total_money}\n"
        f"💸 *Pokédollars gagnés* : {total_earned_money}\n"
        f"📅 *Âge du compte* : {account_age_days} jours\n\n"
        f"📦 *Pokémons capturés* : {total_captured}\n"
        f"✨ *Shinies capturés* : {nb_shinies}\n"
        f"🌈 *Mythiques capturés* : {nb_mythics}\n"
        f"🏃‍♂️ *Fuites Pokémon* : {pokemons_fled}\n"
        f"🔁 *Échanges* : {nb_trades}\n"
        f"🔥 *Série max de captures* : {max_streak}\n\n"
        f"🎯 *Pokéball utilisées* : {balls_used.get('pokeball', 0)}\n"
        f"🎯 *Superball utilisées* : {balls_used.get('superball', 0)}\n"
        f"🎯 *Hyperball utilisées* : {balls_used.get('hyperball', 0)}\n"
        f"🎯 *Masterball utilisées* : {balls_used.get('masterball', 0)}\n\n"
        f"💸 *Bonus Pokédollars* : {money_bonus}%\n"
        f"✨ *Taux shiny actuel* : 1 / {shiny_chance} ({round(shiny_bonus*100, 2)}% bonus)\n"
        f"🔮 *Charme Chroma possédés* : {shiny_charms}\n"
    )

    await update.message.reply_text(message, parse_mode="Markdown")
