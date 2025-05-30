# core/types_data.py

TYPE_CHART = {
    "Normal":     {"weak": ["Fighting"], "resist": [], "immune": ["Ghost"]},
    "Fire":       {"weak": ["Water", "Ground", "Rock"], "resist": ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"], "immune": []},
    "Water":      {"weak": ["Electric", "Grass"], "resist": ["Fire", "Water", "Ice", "Steel"], "immune": []},
    "Electric":   {"weak": ["Ground"], "resist": ["Electric", "Flying", "Steel"], "immune": []},
    "Grass":      {"weak": ["Fire", "Ice", "Poison", "Flying", "Bug"], "resist": ["Water", "Electric", "Grass", "Ground"], "immune": []},
    "Ice":        {"weak": ["Fire", "Fighting", "Rock", "Steel"], "resist": ["Ice"], "immune": []},
    "Fighting":   {"weak": ["Flying", "Psychic", "Fairy"], "resist": ["Bug", "Rock", "Dark"], "immune": []},
    "Poison":     {"weak": ["Ground", "Psychic"], "resist": ["Grass", "Fighting", "Poison", "Bug", "Fairy"], "immune": []},
    "Ground":     {"weak": ["Water", "Ice", "Grass"], "resist": ["Poison", "Rock"], "immune": ["Electric"]},
    "Flying":     {"weak": ["Electric", "Ice", "Rock"], "resist": ["Grass", "Fighting", "Bug"], "immune": ["Ground"]},
    "Psychic":    {"weak": ["Bug", "Ghost", "Dark"], "resist": ["Fighting", "Psychic"], "immune": []},
    "Bug":        {"weak": ["Fire", "Flying", "Rock"], "resist": ["Grass", "Fighting", "Ground"], "immune": []},
    "Rock":       {"weak": ["Water", "Grass", "Fighting", "Ground", "Steel"], "resist": ["Normal", "Fire", "Poison", "Flying"], "immune": []},
    "Ghost":      {"weak": ["Ghost", "Dark"], "resist": ["Poison", "Bug"], "immune": ["Normal", "Fighting"]},
    "Dragon":     {"weak": ["Ice", "Dragon", "Fairy"], "resist": ["Fire", "Water", "Electric", "Grass"], "immune": []},
    "Dark":       {"weak": ["Fighting", "Bug", "Fairy"], "resist": ["Ghost", "Dark"], "immune": ["Psychic"]},
    "Steel":      {"weak": ["Fire", "Fighting", "Ground"], "resist": ["Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Fairy"], "immune": ["Poison"]},
    "Fairy":      {"weak": ["Poison", "Steel"], "resist": ["Fighting", "Bug", "Dark"], "immune": ["Dragon"]}
}

TYPE_TRANSLATION = {
    "Normal": {"fr": "Normal", "en": "Normal"},
    "Fire": {"fr": "Feu", "en": "Fire"},
    "Water": {"fr": "Eau", "en": "Water"},
    "Electric": {"fr": "Électrik", "en": "Electric"},
    "Grass": {"fr": "Plante", "en": "Grass"},
    "Ice": {"fr": "Glace", "en": "Ice"},
    "Fighting": {"fr": "Combat", "en": "Fighting"},
    "Poison": {"fr": "Poison", "en": "Poison"},
    "Ground": {"fr": "Sol", "en": "Ground"},
    "Flying": {"fr": "Vol", "en": "Flying"},
    "Psychic": {"fr": "Psy", "en": "Psychic"},
    "Bug": {"fr": "Insecte", "en": "Bug"},
    "Rock": {"fr": "Roche", "en": "Rock"},
    "Ghost": {"fr": "Spectre", "en": "Ghost"},
    "Dragon": {"fr": "Dragon", "en": "Dragon"},
    "Dark": {"fr": "Ténèbres", "en": "Dark"},
    "Steel": {"fr": "Acier", "en": "Steel"},
    "Fairy": {"fr": "Fée", "en": "Fairy"}
}
