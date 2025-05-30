from core.stats import calculate_stats

# XP nécessaire pour chaque niveau (courbe médiane simplifiée)
def get_exp_to_next_level(level: int) -> int:
    return int((4 * (level ** 3)) / 5)

# Trouve le niveau en fonction de l'XP totale (courbe médiane)
def get_level_from_exp(exp: int) -> int:
    level = 1
    while get_exp_to_next_level(level + 1) <= exp and level < 100:
        level += 1
    return level

# Applique un gain d'expérience, retourne True si level up
def add_exp(pkm: dict, exp_gain: int, base_stats: dict, lang: str = "fr") -> bool:
    current_exp = pkm.get("exp", 0)
    pkm["exp"] = current_exp + exp_gain

    old_level = pkm.get("level", 1)
    new_level = get_level_from_exp(pkm["exp"])
    pkm["level"] = new_level

    # Si le niveau a changé, recalcul des stats
    if new_level > old_level:
        pkm["stats"] = calculate_stats(base_stats, pkm["ivs"], pkm["nature"], lang, new_level, evs=pkm.get("evs"))
        return True

    return False

# Ajoute les EVs gagnés dans les stats correspondantes
def add_evs(pkm: dict, ev_gain: dict):
    if "evs" not in pkm:
        pkm["evs"] = {"hp": 0, "atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0}

    for stat, value in ev_gain.items():
        if stat in pkm["evs"]:
            pkm["evs"][stat] += value

    # Cap global optionnel à 510 total (comme dans les jeux officiels)
    total_evs = sum(pkm["evs"].values())
    if total_evs > 510:
        excess = total_evs - 510
        for stat in pkm["evs"]:
            if excess <= 0:
                break
            if pkm["evs"][stat] > 0:
                reduction = min(pkm["evs"][stat], excess)
                pkm["evs"][stat] -= reduction
                excess -= reduction
