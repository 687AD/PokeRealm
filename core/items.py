BALL_RATES = {
    "pokeball": 0.4,
    "superball": 0.6,
    "hyperball": 0.8,
    "masterball": 1.0
}

RARITY_RATES = {
    "common": 0.9,
    "uncommon": 0.7,
    "rare": 0.5,
    "epic": 0.3,
    "legendary": 0.1,
    "mythic": 0.01
}

# Prix des balls et objets spéciaux
BALL_COSTS = {
    "pokeball": 100,
    "superball": 300,
    "hyperball": 1000,
    "masterball": 10000
}

ITEM_COSTS = {
    "chroma": 20000,
    "multi_exp": 20000,
    "oeuf_chance": 20000,
    "piece_rune": 20000
}

def get_capture_chance(ball_type, rarity):
    return BALL_RATES.get(ball_type, 0) * RARITY_RATES.get(rarity, 0)

def can_afford(user_data, item, quantity=1):
    price = BALL_COSTS.get(item) or ITEM_COSTS.get(item) or GENERAL_ITEMS.get(item, {}).get("cost", 0)
    return user_data["money"] >= price * quantity

def buy_item(user_data, item, quantity):
    price = BALL_COSTS.get(item) or ITEM_COSTS.get(item) or GENERAL_ITEMS.get(item, {}).get("cost", 0)
    total = price * quantity
    if user_data["money"] >= total:
        user_data["money"] -= total
        if item in user_data["pokeballs"]:
            user_data["pokeballs"][item] += quantity
        elif item in user_data["items"]:
            user_data["items"][item] += quantity
        else:
            user_data["items"][item] = quantity
        return True
    return False

# === Objets de soins ===
HEALING_ITEMS = {
    "potion": {"cost": 300, "effect": "heal", "value": 20},
    "super_potion": {"cost": 700, "effect": "heal", "value": 50},
    "hyper_potion": {"cost": 1200, "effect": "heal", "value": 120},
    "max_potion": {"cost": 2500, "effect": "heal", "value": "full"},
    "revive": {"cost": 2000, "effect": "revive", "value": 0.5},
    "max_revive": {"cost": 4000, "effect": "revive", "value": 1.0},
    "full_restore": {"cost": 3000, "effect": "heal_and_cure", "value": "full"}
}

# === Objets de statut ===
STATUS_ITEMS = {
    "antidote": {"cost": 100, "effect": "cure", "status": "poison"},
    "paralyze_heal": {"cost": 200, "effect": "cure", "status": "paralysis"},
    "burn_heal": {"cost": 250, "effect": "cure", "status": "burn"},
    "ice_heal": {"cost": 250, "effect": "cure", "status": "freeze"},
    "awakening": {"cost": 250, "effect": "cure", "status": "sleep"},
    "full_heal": {"cost": 600, "effect": "cure", "status": "all"}
}

# === Objets de PP ===
PP_ITEMS = {
    "ether": {"cost": 1200, "effect": "pp_restore", "value": 10},
    "elixir": {"cost": 3000, "effect": "pp_restore", "value": "all"},
    "lemonade": {"cost": 350, "effect": "heal", "value": 70}
}

# === Boosts de combat (X Stat Items) ===
X_ITEMS = {
    "x_attack": {"cost": 500, "effect": "boost", "stat": "atk"},
    "x_defense": {"cost": 500, "effect": "boost", "stat": "def"},
    "x_speed": {"cost": 500, "effect": "boost", "stat": "spe"},
    "x_special": {"cost": 500, "effect": "boost", "stat": "spa"},
    "x_sp_def": {"cost": 500, "effect": "boost", "stat": "spd"},
    "x_accuracy": {"cost": 500, "effect": "boost", "stat": "accuracy"},
    "guard_spec": {"cost": 700, "effect": "protect_stats"}
}

# === Objets d'exploration ===
FIELD_ITEMS = {
    "repel": {"cost": 350, "effect": "repel", "steps": 100},
    "super_repel": {"cost": 500, "effect": "repel", "steps": 200},
    "max_repel": {"cost": 700, "effect": "repel", "steps": 250},
    "escape_rope": {"cost": 99999, "effect": "escape_dungeon"}
}

# === Objets d'entraînement et EV ===
TRAINING_ITEMS = {
    "rare_candy": {"cost": 4800, "effect": "gain_level"},
    "pp_up": {"cost": 9800, "effect": "increase_pp"},
    "hp_up": {"cost": 9800, "effect": "ev_boost", "stat": "hp"},
    "protein": {"cost": 9800, "effect": "ev_boost", "stat": "atk"},
    "iron": {"cost": 9800, "effect": "ev_boost", "stat": "def"},
    "calcium": {"cost": 9800, "effect": "ev_boost", "stat": "spa"},
    "zinc": {"cost": 9800, "effect": "ev_boost", "stat": "spd"},
    "carbos": {"cost": 9800, "effect": "ev_boost", "stat": "spe"}
}

# === Objets de tenue en combat ===
HELD_ITEMS = {
    "casque_brut": {"cost": 10000, "effect": "damage_on_contact", "value": 0.16},
    "restes": {"cost": 15000, "effect": "heal_each_turn", "value": 0.0625},
    "bandeau_choix": {"cost": 18000, "effect": "boost_stat", "stat": "atk", "value": 1.5, "restriction": "one_move_only"},
    "lunettes_choix": {"cost": 18000, "effect": "boost_stat", "stat": "spa", "value": 1.5, "restriction": "one_move_only"},
    "mouchoir_choix": {"cost": 18000, "effect": "boost_stat", "stat": "spe", "value": 1.5, "restriction": "one_move_only"},
    "orbe_vie": {"cost": 20000, "effect": "boost_all_damage", "value": 1.3, "recoil": 0.1},
    "ceinture_force": {"cost": 12000, "effect": "survive_one_hit"},
}

# === Fusion de tout (pour accès global) ===
GENERAL_ITEMS = {}
for group in [HEALING_ITEMS, STATUS_ITEMS, PP_ITEMS, X_ITEMS, FIELD_ITEMS, TRAINING_ITEMS, HELD_ITEMS]:
    GENERAL_ITEMS.update(group)

# === Ajout des objets spéciaux à GENERAL_ITEMS ===
for key in ITEM_COSTS:
    GENERAL_ITEMS[key] = {"cost": ITEM_COSTS[key], "effect": "special"}

# === Catégorisation des objets pour la boutique ou les menus ===
CATEGORIES_ITEMS = {
    "Poké Balls": list(BALL_COSTS.keys()),
    "Objets spéciaux": list(ITEM_COSTS.keys()),
    "Soins": list(HEALING_ITEMS.keys()),
    "Statuts": list(STATUS_ITEMS.keys()),
    "PP & Boissons": list(PP_ITEMS.keys()),
    "Boosts de combat": list(X_ITEMS.keys()),
    "Exploration": list(FIELD_ITEMS.keys()),
    "Entraînement / EV": list(TRAINING_ITEMS.keys()),
    "Objets tenus": list(HELD_ITEMS.keys())
}

# === Traductions des noms des objets ===
ITEMS = {
    "pokeball": {"fr": "Poké Ball", "en": "Poké Ball"},
    "superball": {"fr": "Super Ball", "en": "Great Ball"},
    "hyperball": {"fr": "Hyper Ball", "en": "Ultra Ball"},
    "masterball": {"fr": "Master Ball", "en": "Master Ball"},
    "chroma": {"fr": "Charme Chroma", "en": "Shiny Charm"},
    "multi_exp": {"fr": "Multi Exp", "en": "Exp. Share"},
    "potion": {"fr": "Potion", "en": "Potion"},
    "super_potion": {"fr": "Super Potion", "en": "Super Potion"},
    "hyper_potion": {"fr": "Hyper Potion", "en": "Hyper Potion"},
    "max_potion": {"fr": "Potion Max", "en": "Max Potion"},
    "revive": {"fr": "Rappel", "en": "Revive"},
    "max_revive": {"fr": "Rappel Max", "en": "Max Revive"},
    "full_restore": {"fr": "Guérison", "en": "Full Restore"},
    "antidote": {"fr": "Antidote", "en": "Antidote"},
    "paralyze_heal": {"fr": "Anti-Para", "en": "Paralyze Heal"},
    "burn_heal": {"fr": "Anti-Brûle", "en": "Burn Heal"},
    "ice_heal": {"fr": "Anti-Gel", "en": "Ice Heal"},
    "awakening": {"fr": "Réveil", "en": "Awakening"},
    "full_heal": {"fr": "Total Soin", "en": "Full Heal"},
    "ether": {"fr": "Élixir Max", "en": "Ether"},
    "elixir": {"fr": "Max Élixir", "en": "Elixir"},
    "lemonade": {"fr": "Limonade", "en": "Lemonade"},
    "x_attack": {"fr": "Attaque +", "en": "X Attack"},
    "x_defense": {"fr": "Défense +", "en": "X Defense"},
    "x_speed": {"fr": "Vitesse +", "en": "X Speed"},
    "x_special": {"fr": "Att. Spé. +", "en": "X Sp. Atk"},
    "x_sp_def": {"fr": "Déf. Spé. +", "en": "X Sp. Def"},
    "x_accuracy": {"fr": "Précision +", "en": "X Accuracy"},
    "guard_spec": {"fr": "Barrage", "en": "Guard Spec."},
    "repel": {"fr": "Repousse", "en": "Repel"},
    "super_repel": {"fr": "Super Repousse", "en": "Super Repel"},
    "max_repel": {"fr": "Max Repousse", "en": "Max Repel"},
    "escape_rope": {"fr": "Corde Sortie", "en": "Escape Rope"},
    "rare_candy": {"fr": "Bonbon Rare", "en": "Rare Candy"},
    "pp_up": {"fr": "PP Plus", "en": "PP Up"},
    "hp_up": {"fr": "PV Plus", "en": "HP Up"},
    "protein": {"fr": "Protéine", "en": "Protein"},
    "iron": {"fr": "Fer", "en": "Iron"},
    "calcium": {"fr": "Calcium", "en": "Calcium"},
    "zinc": {"fr": "Zinc", "en": "Zinc"},
    "carbos": {"fr": "Carbone", "en": "Carbos"},
    "casque_brut": {"fr": "Casque Brut", "en": "Rocky Helmet"},
    "restes": {"fr": "Restes", "en": "Leftovers"},
    "bandeau_choix": {"fr": "Bandeau Choix", "en": "Choice Band"},
    "lunettes_choix": {"fr": "Lunettes Choix", "en": "Choice Specs"},
    "mouchoir_choix": {"fr": "Mouchoir Choix", "en": "Choice Scarf"},
    "orbe_vie": {"fr": "Orbe Vie", "en": "Life Orb"},
    "ceinture_force": {"fr": "Ceinture Force", "en": "Focus Sash"},
    "oeuf_chance": {"fr": "Œuf Chance", "en": "Lucky Egg"},
    "piece_rune": {"fr": "Pièce Rune", "en": "Amulet Coin"}
}

CATEGORY_NAMES = {
    "Poké Balls": {"fr": "Poké Balls", "en": "Poké Balls"},
    "Objets spéciaux": {"fr": "Objets spéciaux", "en": "Special Items"},
    "Soins": {"fr": "Soins", "en": "Healing"},
    "Statuts": {"fr": "Statuts", "en": "Status"},
    "PP & Boissons": {"fr": "PP & Boissons", "en": "PP & Drinks"},
    "Boosts de combat": {"fr": "Boosts de combat", "en": "Battle Boosts"},
    "Exploration": {"fr": "Exploration", "en": "Exploration"},
    "Entraînement / EV": {"fr": "Entraînement / EV", "en": "Training / EV"},
    "Objets tenus": {"fr": "Objets tenus", "en": "Held Items"},
    "Unknown": {"fr": "Inconnu", "en": "Unknown"}
}

# ✅ Ajout pour éviter erreur d'import
SHOP_CATEGORY_PREFIX = "🛒"