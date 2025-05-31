from core.nature import NATURE_EFFECTS, NATURE_EFFECTS_EN
from core.user_data import load_user, save_user

def calculate_stats(base, ivs, nature, lang="fr", level=1, evs=None) -> dict:
    if evs is None:
        evs = {stat: 0 for stat in base}
    stats = {}

    effects = (
        NATURE_EFFECTS.get(nature)
        if lang == "fr"
        else NATURE_EFFECTS_EN.get(nature)
    )

    for stat in base:
        base_val = base[stat]
        iv = ivs.get(stat, 0)
        ev = evs.get(stat, 0)

        if stat == "hp":
            stat_val = int(((base_val * 2 + iv + ev // 4) * level / 100) + level + 10)
        else:
            stat_val = int(((base_val * 2 + iv + ev // 4) * level / 100) + 5)
            if effects:
                if stat == effects.get("up"):
                    stat_val = int(stat_val * 1.1)
                elif stat == effects.get("down"):
                    stat_val = int(stat_val * 0.9)

        stats[stat] = stat_val

    return stats

def format_stats(stats: dict, lang: str = "fr", level: int = 1, exp: int = 0, evs: dict = None) -> str:
    labels = {
        "fr": {
            "hp": "❤️ PV",
            "atk": "🗡️ Attaque",
            "def": "🛡️ Défense",
            "spa": "✨ Atq Spé",
            "spd": "🔮 Déf Spé",
            "spe": "⚡ Vitesse",
        },
        "en": {
            "hp": "❤️ HP",
            "atk": "🗡️ Attack",
            "def": "🛡️ Defense",
            "spa": "✨ Sp. Atk",
            "spd": "🔮 Sp. Def",
            "spe": "⚡ Speed",
        }
    }

    l = labels.get(lang, labels["fr"])
    order = ["hp", "atk", "def", "spa", "spd", "spe"]

    lines = [f"{l[k]}: {stats[k]}" for k in order]
    lines.append(f"\n🎯 Niveau: {level} | 📈 XP: {exp}")

    if evs:
        ev_lines = [f"{k.upper()} +{v}" for k, v in evs.items() if v > 0]
        if ev_lines:
            lines.append("📊 EVs: " + ", ".join(ev_lines))

    return "📊 *Statistiques :*\n" + "\n".join(lines)

