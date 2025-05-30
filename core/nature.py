NATURE_EFFECTS = {
    "Rigide":    {"up": "atk",  "down": "spa"},
    "Solo":      {"up": "atk",  "down": "def"},
    "Brave":     {"up": "atk",  "down": "spe"},
    "Malpoli":   {"up": "atk",  "down": "spd"},
    "Assuré":    {"up": "def",  "down": "atk"},
    "Lâche":      {"up": "def",  "down": "spa"},
    "Relax":     {"up": "def",  "down": "spe"},
    "Malin":     {"up": "def",  "down": "spd"},
    "Modeste":   {"up": "spa",  "down": "atk"},
    "Doux":      {"up": "spa",  "down": "def"},
    "Discret":   {"up": "spa",  "down": "spe"},
    "Foufou":    {"up": "spa",  "down": "spd"},
    "Calme":     {"up": "spd",  "down": "atk"},
    "Gentil":    {"up": "spd",  "down": "def"},
    "Prudent":   {"up": "spd",  "down": "spa"},
    "Bizarre":   {"up": "spd",  "down": "spe"},
    "Timide":    {"up": "spe",  "down": "atk"},
    "Pressé":    {"up": "spe",  "down": "def"},
    "Jovial":    {"up": "spe",  "down": "spa"},
    "Naïf":      {"up": "spe",  "down": "spd"},
    "Hardy":     {"up": None,   "down": None},
    "Docile":    {"up": None,   "down": None},
    "Sérieux":   {"up": None,   "down": None},
    "Pudique":   {"up": None,   "down": None},
    "Bizarre":   {"up": None,   "down": None}
}

NATURE_EFFECTS_EN = {
    "Adamant":   {"up": "atk",  "down": "spa"},
    "Lonely":    {"up": "atk",  "down": "def"},
    "Brave":     {"up": "atk",  "down": "spe"},
    "Naughty":   {"up": "atk",  "down": "spd"},
    "Bold":      {"up": "def",  "down": "atk"},
    "Lax":       {"up": "def",  "down": "spa"},
    "Relaxed":   {"up": "def",  "down": "spe"},
    "Impish":    {"up": "def",  "down": "spd"},
    "Modest":    {"up": "spa",  "down": "atk"},
    "Mild":      {"up": "spa",  "down": "def"},
    "Quiet":     {"up": "spa",  "down": "spe"},
    "Rash":      {"up": "spa",  "down": "spd"},
    "Calm":      {"up": "spd",  "down": "atk"},
    "Gentle":    {"up": "spd",  "down": "def"},
    "Careful":   {"up": "spd",  "down": "spa"},
    "Sassy":     {"up": "spd",  "down": "spe"},
    "Timid":     {"up": "spe",  "down": "atk"},
    "Hasty":     {"up": "spe",  "down": "def"},
    "Jolly":     {"up": "spe",  "down": "spa"},
    "Naive":     {"up": "spe",  "down": "spd"},
    "Hardy":     {"up": None,   "down": None},
    "Docile":    {"up": None,   "down": None},
    "Serious":   {"up": None,   "down": None},
    "Bashful":   {"up": None,   "down": None},
    "Quirky":    {"up": None,   "down": None}
}

def apply_nature_effects(stats: dict, nature: str, lang: str = "fr") -> dict:
    effects = (
        NATURE_EFFECTS.get(nature)
        if lang == "fr"
        else NATURE_EFFECTS_EN.get(nature)
    )

    if not effects:
        return stats

    boosted = stats.copy()

    if effects["up"]:
        boosted[effects["up"]] = int(boosted[effects["up"]] * 1.1)
    if effects["down"]:
        boosted[effects["down"]] = int(boosted[effects["down"]] * 0.9)

    return boosted
