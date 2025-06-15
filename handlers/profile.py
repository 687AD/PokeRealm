from telegram import Update
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from datetime import datetime

DEFAULT_USER = {
    "pokeballs": {"pokeball": 10, "superball": 5, "hyperball": 2, "masterball": 0},
    "items": {"chroma": 0, "multi_exp": 0, "piece_rune": 0},  # ajoute "piece_rune" si absent !
    "money": 500,
    "box": [],
    "daily_claimed": None,
    "balls_used": {"pokeball": 0, "superball": 0, "hyperball": 0, "masterball": 0}  # <--- AJOUTE ICI
}

def sync_stats(data):
    box = data.get("box", [])
    data["pokemons_captured"] = sum(p.get("quantity", 1) for p in box)
    data["nb_shinies"] = sum(p.get("quantity", 1) for p in box if p.get("shiny"))
    data["nb_mythics"] = sum(p.get("quantity", 1) for p in box if p.get("rarity") == "mythic")
    items = data.get("items", {})
    data["shiny_charms"] = items.get("chroma", 0)
    data["money_bonus"] = items.get("piece_rune", 0) * 5
    data["balls_used"] = data.get("balls_used", {"pokeball": 0, "superball": 0, "hyperball": 0, "masterball": 0})
    data["pokemons_sold"] = data.get("pokemons_sold", 0)
    data["pokemons_fled"] = data.get("pokemons_fled", 0)
    data["max_streak"] = data.get("max_streak", 0)
    data["nb_trades"] = data.get("nb_trades", 0)
    data["money"] = data.get("money", 0)
    data["total_earned_money"] = data.get("total_earned_money", data["money"])
    if not data.get("creation_date"):
        from datetime import datetime
        data["creation_date"] = datetime.utcnow().strftime("%Y-%m-%d")
    return data

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    data = sync_stats(data)
    save_user(user.id, data)  # pour garder les valeurs corrigées
    money_bonus = data.get("money_bonus", 0)
    balls_used = data.get("balls_used", {"pokeball": 0, "superball": 0, "hyperball": 0, "masterball": 0})
    pokemons_captured = data.get("pokemons_captured", 0)
    pokemons_sold = data.get("pokemons_sold", 0)
    pokemons_fled = data.get("pokemons_fled", 0)
    shiny_charms = data.get("shiny_charms", 0)
    shiny_base_rate = 1 / 4096
    shiny_bonus = min(0.5, shiny_charms * 0.05)  # 20 charmes = 100%, soit 50% de bonus effectif
    shiny_rate = shiny_base_rate / (1 - shiny_bonus)
    shiny_chance = int(1 / shiny_rate) if shiny_rate > 0 else "∞"
    total_captured = pokemons_captured + pokemons_sold
    nb_shinies = data.get("nb_shinies", 0)
    nb_mythics = data.get("nb_mythics", 0)

    # Âge du compte (toujours correct, même si la date vient d'être créée)
    creation_date_str = data.get("creation_date")
    try:
        creation_date = datetime.strptime(creation_date_str, "%Y-%m-%d")
        account_age_days = (datetime.utcnow() - creation_date).days
    except Exception:
        account_age_days = "?"

    name = user.first_name

    message = (
        f"👤 *Profil de {name}*\n\n"
        f"📅 *Âge du compte* : {account_age_days} jours\n\n"
        f"📦 *Pokémons capturés* : {total_captured}\n"
        f"✨ *Shinies capturés* : {nb_shinies}\n"
        f"🌈 *Mythiques capturés* : {nb_mythics}\n"
        f"🏃‍♂️ *Fuites Pokémon* : {pokemons_fled}\n"
        f"🎯 *Pokéball utilisées* : {balls_used.get('pokeball', 0)}\n"
        f"🎯 *Superball utilisées* : {balls_used.get('superball', 0)}\n"
        f"🎯 *Hyperball utilisées* : {balls_used.get('hyperball', 0)}\n"
        f"🎯 *Masterball utilisées* : {balls_used.get('masterball', 0)}\n\n"
        f"💸 *Bonus Pokédollars* : {money_bonus}%\n"
        f"✨ *Taux shiny actuel* : 1 / {shiny_chance} ({round(shiny_bonus*100, 2)}% bonus)\n"
        f"🔮 *Charme Chroma possédés* : {shiny_charms}\n"
    )

    await update.message.reply_text(message, parse_mode="Markdown")

