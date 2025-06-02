from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from core.user_data import get_and_update_user, save_user
from core.lang import get_text
from core.items import ITEMS  # Assure-toi que ITEMS contient tous les noms pour chaque ball/lang

def get_ball_emoji(ball):
    return {
        "pokeball": "🔴",
        "superball": "🔵",
        "hyperball": "🟣",
        "masterball": "🟪"
    }.get(ball, "🎲")

def get_streak_bonus(streak, lang="fr"):
    PALIER_REWARDS = [
        # (palier, récompenses, message FR, message EN)
        (1, {"money": 1000, "pokeball": 10}, "🎉 Premier jour ! +10 Pokéballs", "🎉 First day! +10 Pokéballs"),
        (7, {"money": 5000, "pokeball": 20, "superball": 10}, "✨ 7 jours ! +20 Pokéballs, +10 Superballs", "✨ 7 days! +20 Pokéballs, +10 Superballs"),
        (14, {"money": 8000, "pokeball": 25, "superball": 15}, "✨ 14 jours ! +25 Pokéballs, +15 Superballs", "✨ 14 days! +25 Pokéballs, +15 Superballs"),
        (30, {"money": 15000, "pokeball": 30, "superball": 20, "hyperball": 5}, "🟪 30 jours ! +30 Pokéballs, +20 Superballs, +5 Hyperballs", "🟪 30 days! +30 Pokéballs, +20 Superballs, +5 Hyperballs"),
        (50, {"money": 20000, "pokeball": 40, "superball": 25, "hyperball": 10}, "🔥 50 jours ! +40 Pokéballs, +25 Superballs, +10 Hyperballs", "🔥 50 days! +40 Pokéballs, +25 Superballs, +10 Hyperballs"),
        (75, {"money": 30000, "pokeball": 50, "superball": 30, "hyperball": 15}, "💎 75 jours ! +50 Pokéballs, +30 Superballs, +15 Hyperballs", "💎 75 days! +50 Pokéballs, +30 Superballs, +15 Hyperballs"),
        (100, {"money": 50000, "pokeball": 60, "superball": 40, "hyperball": 20}, "👑 100 jours ! +60 Pokéballs, +40 Superballs, +20 Hyperballs", "👑 100 days! +60 Pokéballs, +40 Superballs, +20 Hyperballs"),
        (150, {"money": 80000, "pokeball": 75, "superball": 50, "hyperball": 30}, "🥇 150 jours ! +75 Pokéballs, +50 Superballs, +30 Hyperballs", "🥇 150 days! +75 Pokéballs, +50 Superballs, +30 Hyperballs"),
        (200, {"money": 120000, "pokeball": 90, "superball": 60, "hyperball": 40}, "🚀 200 jours ! +90 Pokéballs, +60 Superballs, +40 Hyperballs", "🚀 200 days! +90 Pokéballs, +60 Superballs, +40 Hyperballs"),
        (300, {"money": 250000, "pokeball": 120, "superball": 80, "hyperball": 60, "masterball": 1}, "🌟 300 jours ! +120 Pokéballs, +80 Superballs, +60 Hyperballs, +1 Masterball", "🌟 300 days! +120 Pokéballs, +80 Superballs, +60 Hyperballs, +1 Masterball"),
        (365, {"money": 1000000, "pokeball": 200, "superball": 150, "hyperball": 100, "masterball": 3}, "🎆 1 AN ! +200 Pokéballs, +150 Superballs, +100 Hyperballs, +3 Masterballs — LÉGENDAIRE !", "🎆 1 YEAR! +200 Pokéballs, +150 Superballs, +100 Hyperballs, +3 Masterballs — LEGENDARY!"),
    ]
    bonus = None
    msg = ""
    for palier, rewards, txt, txt_en in reversed(PALIER_REWARDS):
        if streak >= palier:
            bonus = rewards
            msg = txt if lang == "fr" else txt_en
            break
    # Récompense daily générique si pas de gros palier
    if not bonus:
        bonus = {"money": 1200, "pokeball": 12}
        msg = "🎁 Récompense quotidienne : +12 Pokéballs" if lang == "fr" else "🎁 Daily reward: +12 Pokéballs"

    # Entre deux gros paliers, on file un bonus boosté
    palier_list = [palier for palier, _, _, _ in PALIER_REWARDS]
    if streak not in palier_list:
        if streak > 1:
            bonus = {"money": bonus["money"] + 800, **{k: v + 3 for k, v in bonus.items() if k != "money"}}
            msg = f"🎉 Streak quotidien ! +{bonus.get('pokeball', 0)} Pokéballs" if lang == "fr" else f"🎉 Daily streak! +{bonus.get('pokeball', 0)} Pokéballs"
            if "superball" in bonus:
                msg += f", +{bonus['superball']} Superballs"
            if "hyperball" in bonus:
                msg += f", +{bonus['hyperball']} Hyperballs"
            if "masterball" in bonus:
                msg += f", +{bonus['masterball']} Masterballs"
    return bonus, msg

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = get_and_update_user(user.id, user.username)
    lang = data.get("lang", "fr")
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    last_claimed = data.get("daily_claimed")
    streak = data.get("daily_streak", 0)
    best = data.get("daily_best", 0)

    if last_claimed == today.isoformat():
        await update.message.reply_text(get_text("daily_already", lang, streak=streak))
        return

    if last_claimed == yesterday.isoformat():
        streak += 1
    else:
        streak = 1  # reset

    best = max(streak, best)
    bonus, palier_msg = get_streak_bonus(streak, lang)
    data["money"] = data.get("money", 0) + bonus["money"]
    data.setdefault("pokeballs", {})
    ball_lines = []
    for ball, qty in bonus.items():
        if ball == "money":
            continue
        data["pokeballs"][ball] = data["pokeballs"].get(ball, 0) + qty
        ball_lines.append(f"{get_ball_emoji(ball)} +{qty} {ITEMS[ball][lang]}")
    balls_txt = "\n".join(ball_lines)

    data["daily_claimed"] = today.isoformat()
    data["daily_streak"] = streak
    data["daily_best"] = best

    save_user(user.id, data)

    msg = (
        f"{palier_msg}\n\n"
        f"💰 +{bonus['money']} Pokédollars\n"
        f"{balls_txt}\n"
        f"🔥 Streak actuel : {streak} jour(s)\n"
        f"🏆 Meilleur streak : {best} jour(s)"
    )
    await update.message.reply_text(msg)

PALIER_REWARDS_EN = [
    (1, {"money": 1000, "pokeball": 10}, "🎉 First day! +10 Pokéballs"),
    (7, {"money": 5000, "pokeball": 20, "superball": 10}, "✨ 7 days! +20 Pokéballs, +10 Superballs"),
    (14, {"money": 8000, "pokeball": 25, "superball": 15}, "✨ 14 days! +25 Pokéballs, +15 Superballs"),
    (30, {"money": 15000, "pokeball": 30, "superball": 20, "hyperball": 5}, "🟪 30 days! +30 Pokéballs, +20 Superballs, +5 Hyperballs"),
    (50, {"money": 20000, "pokeball": 40, "superball": 25, "hyperball": 10}, "🔥 50 days! +40 Pokéballs, +25 Superballs, +10 Hyperballs"),
    (75, {"money": 30000, "pokeball": 50, "superball": 30, "hyperball": 15}, "💎 75 days! +50 Pokéballs, +30 Superballs, +15 Hyperballs"),
    (100, {"money": 50000, "pokeball": 60, "superball": 40, "hyperball": 20}, "👑 100 days! +60 Pokéballs, +40 Superballs, +20 Hyperballs"),
    (150, {"money": 80000, "pokeball": 75, "superball": 50, "hyperball": 30}, "🥇 150 days! +75 Pokéballs, +50 Superballs, +30 Hyperballs"),
    (200, {"money": 120000, "pokeball": 90, "superball": 60, "hyperball": 40}, "🚀 200 days! +90 Pokéballs, +60 Superballs, +40 Hyperballs"),
    (300, {"money": 250000, "pokeball": 120, "superball": 80, "hyperball": 60, "masterball": 1}, "🌟 300 days! +120 Pokéballs, +80 Superballs, +60 Hyperballs, +1 Masterball"),
    (365, {"money": 1000000, "pokeball": 200, "superball": 150, "hyperball": 100, "masterball": 3}, "🎆 1 YEAR! +200 Pokéballs, +150 Superballs, +100 Hyperballs, +3 Masterballs — LEGENDARY!")
]
