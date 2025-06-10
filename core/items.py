BALL_RATES = {
    "pokeball": {
        "common": 80,
        "uncommon": 60,
        "rare": 40,
        "epic": 25,
        "legendary": 10,
        "mythic": 5,
    },
    "superball": {
        "common": 90,
        "uncommon": 75,
        "rare": 60,
        "epic": 45,
        "legendary": 25,
        "mythic": 15,
    },
    "hyperball": {
        "common": 100,
        "uncommon": 90,
        "rare": 80,
        "epic": 65,
        "legendary": 40,
        "mythic": 30,
    },
    "masterball": {
        "common": 100,
        "uncommon": 100,
        "rare": 100,
        "epic": 100,
        "legendary": 100,
        "mythic": 100,
    },
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
    "pokeball": 200,
    "superball": 500,
    "hyperball": 1000,
    "masterball": 10000
}

ITEM_COSTS = {
    "escape_rope": 100000,
    "multi_exp": 200000,
    "chroma": 0,
    "oeuf_chance": 0,
    "piece_rune": 0
}

def get_capture_chance(ball_type: str, rarity: str) -> int:
    return BALL_RATES.get(ball_type, {}).get(rarity, 0)

def can_afford(user_data, item, quantity=1):
    price = BALL_COSTS.get(item) or get_special_item_cost(user_data, item)
    return user_data["money"] >= price * quantity

SPECIAL_SCALING_ITEMS = ["oeuf_chance", "piece_rune", "chroma"]

def get_special_item_cost(user_data, item):
    if item in SPECIAL_SCALING_ITEMS:
        owned = user_data.get("items", {}).get(item, 0)
        return 100_000 * (owned + 1)
    return ITEM_COSTS.get(item) or GENERAL_ITEMS.get(item, {}).get("cost", 0)

def buy_item(user_data, item, quantity):
    is_ball = item in BALL_COSTS

    if item in SPECIAL_SCALING_ITEMS:
        for _ in range(quantity):
            price = get_special_item_cost(user_data, item)
            if user_data["money"] < price:
                return False
            user_data["money"] -= price
            if is_ball:
                user_data.setdefault("pokeballs", {})
                user_data["pokeballs"][item] = user_data["pokeballs"].get(item, 0) + 1
            else:
                user_data.setdefault("items", {})
                user_data["items"][item] = user_data["items"].get(item, 0) + 1
        return True
    else:
        price = BALL_COSTS.get(item) or ITEM_COSTS.get(item) or GENERAL_ITEMS.get(item, {}).get("cost", 0)
        if user_data["money"] < price * quantity:
            return False
        user_data["money"] -= price * quantity
        if is_ball:
            user_data.setdefault("pokeballs", {})
            user_data["pokeballs"][item] = user_data["pokeballs"].get(item, 0) + quantity
        else:
            user_data.setdefault("items", {})
            user_data["items"][item] = user_data["items"].get(item, 0) + quantity
        return True

# === Objets de soins ===
HEALING_ITEMS = {
    "potion": {"cost": 300, "effect": "heal", "value": 20},
    "super_potion": {"cost": 700, "effect": "heal", "value": 50},
    "lemonade": {"cost": 900, "effect": "heal", "value": 70},
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

# === Objets d'entraînement et EV ===
TRAINING_ITEMS = {
    "rare_candy": {"cost": 10000, "effect": "gain_level"},
    "pp_up": {"cost": 10000, "effect": "increase_pp"},
    "hp_up": {"cost": 10000, "effect": "ev_boost", "stat": "hp"},
    "protein": {"cost": 10000, "effect": "ev_boost", "stat": "atk"},
    "iron": {"cost": 10000, "effect": "ev_boost", "stat": "def"},
    "calcium": {"cost": 10000, "effect": "ev_boost", "stat": "spa"},
    "zinc": {"cost": 10000, "effect": "ev_boost", "stat": "spd"},
    "carbos": {"cost": 10000, "effect": "ev_boost", "stat": "spe"},
    "reset_bag": {"cost": 20000, "effect": "ev_reset"}, #reset un EV au choix
    "vitamin_max": {"cost": 200000, "effect": "ev_max", "value": 510},  # max un EV au choix
}

# === Objets de tenue en combat ===
HELD_ITEMS = {
    "focus_band": {"cost": 300000, "effect": "survive_ko_chance", "value": 0.1},
    "casque_brut": {"cost": 1000000, "effect": "damage_on_contact", "value": 0.16},
    "restes": {"cost": 1500000, "effect": "heal_each_turn", "value": 0.0625},
    "bandeau_choix": {"cost": 1800000, "effect": "boost_stat", "stat": "atk", "value": 1.5, "restriction": "one_move_only"},
    "lunettes_choix": {"cost": 1800000, "effect": "boost_stat", "stat": "spa", "value": 1.5, "restriction": "one_move_only"},
    "mouchoir_choix": {"cost": 1800000, "effect": "boost_stat", "stat": "spe", "value": 1.5, "restriction": "one_move_only"},
    "orbe_vie": {"cost": 2000000, "effect": "boost_all_damage", "value": 1.3, "recoil": 0.1},
    "ceinture_force": {"cost": 1200000, "effect": "survive_one_hit"},
    "lentilscope": {"cost": 900000, "effect": "boost_crit_ratio"},
    "balle_lumiere": {"cost": 1000000, "effect": "double_stat", "target": "pikachu", "stats": ["atk", "spa"]},
    "graines_psy": {"cost": 800000, "effect": "terrain_boost", "condition": "psychic"},
    "graines_brume": {"cost": 800000, "effect": "terrain_boost", "condition": "misty"},
    "graines_electr": {"cost": 800000, "effect": "terrain_boost", "condition": "electric"},
    "graines_herbe": {"cost": 800000, "effect": "terrain_boost", "condition": "grassy"},
    "air_balloon": {"cost": 500000, "effect": "levitate_temporary"},
    "mental_herb": {"cost": 350000, "effect": "cure_infatuation"},
    "smooth_rock": {"cost": 400000, "effect": "extend_weather", "type": "sandstorm"},
    "white_herb": {"cost": 400000, "effect": "restore_lowered_stats"},
    "power_herb": {"cost": 400000, "effect": "instant_charging"},
    "eject_button": {"cost": 450000, "effect": "switch_out_when_hit"},
    "red_card": {"cost": 450000, "effect": "force_switch_attacker"},
    "room_service": {"cost": 300000, "effect": "lower_speed_in_trick_room"},
    "throat_spray": {"cost": 350000, "effect": "boost_spa_on_sound_move"},
    "blunder_policy": {"cost": 350000, "effect": "boost_speed_on_miss"},
    "absorbing_bulb": {"cost": 300000, "effect": "boost_spa_when_hit_water"},
    "cell_battery": {"cost": 300000, "effect": "boost_atk_when_hit_electric"},
    "luminous_moss": {"cost": 300000, "effect": "boost_spd_when_hit_water"},
    "snowball": {"cost": 300000, "effect": "boost_atk_when_hit_ice"},
    "weakness_policy": {"cost": 800000, "effect": "boost_atk_spa_when_hit_super"},
    "policy_armor": {"cost": 600000, "effect": "boost_def_when_hit_physical"},
    "iron_ball": {"cost": 200000, "effect": "halve_speed_and_cancel_flying"},
    "lagging_tail": {"cost": 200000, "effect": "move_last"},
    "full_incense": {"cost": 200000, "effect": "move_last_variant"},
    "quick_powder": {"cost": 200000, "effect": "boost_speed_only_ditto"},
    "grip_claw": {"cost": 300000, "effect": "trap_opponent_longer"},
    "binding_band": {"cost": 300000, "effect": "boost_trap_damage"},
    "shed_shell": {"cost": 400000, "effect": "switch_out_even_trapped"},
    "sticky_barb": {"cost": 100000, "effect": "damage_holder_and_can_transfer"}
}


# === Méga-Gemmes ===
MEGA_ITEMS = {
    "abomasite": {"cost": 1000000, "effect": "mega_evolve", "target": "abomasnow"},
    "absolite": {"cost": 1000000, "effect": "mega_evolve", "target": "absol"},
    "aerodactylite": {"cost": 1000000, "effect": "mega_evolve", "target": "aerodactyl"},
    "aggronite": {"cost": 1000000, "effect": "mega_evolve", "target": "aggron"},
    "alakazite": {"cost": 1000000, "effect": "mega_evolve", "target": "alakazam"},
    "altarianite": {"cost": 1000000, "effect": "mega_evolve", "target": "altaria"},
    "ampharosite": {"cost": 1000000, "effect": "mega_evolve", "target": "ampharos"},
    "audinite": {"cost": 1000000, "effect": "mega_evolve", "target": "audino"},
    "banettite": {"cost": 1000000, "effect": "mega_evolve", "target": "banette"},
    "beedrillite": {"cost": 1000000, "effect": "mega_evolve", "target": "beedrill"},
    "blastoisinite": {"cost": 1000000, "effect": "mega_evolve", "target": "blastoise"},
    "blazikenite": {"cost": 1000000, "effect": "mega_evolve", "target": "blaziken"},
    "cameruptite": {"cost": 1000000, "effect": "mega_evolve", "target": "camerupt"},
    "charizardite_x": {"cost": 1000000, "effect": "mega_evolve", "target": "charizard_x"},
    "charizardite_y": {"cost": 1000000, "effect": "mega_evolve", "target": "charizard_y"},
    "diancite": {"cost": 1000000, "effect": "mega_evolve", "target": "diancie"},
    "galladite": {"cost": 1000000, "effect": "mega_evolve", "target": "gallade"},
    "garchompite": {"cost": 1000000, "effect": "mega_evolve", "target": "garchomp"},
    "gardevoirite": {"cost": 1000000, "effect": "mega_evolve", "target": "gardevoir"},
    "gengarite": {"cost": 1000000, "effect": "mega_evolve", "target": "gengar"},
    "glalitite": {"cost": 1000000, "effect": "mega_evolve", "target": "glalie"},
    "gyaradosite": {"cost": 1000000, "effect": "mega_evolve", "target": "gyarados"},
    "heracronite": {"cost": 1000000, "effect": "mega_evolve", "target": "heracross"},
    "houndoominite": {"cost": 1000000, "effect": "mega_evolve", "target": "houndoom"},
    "kangaskhanite": {"cost": 1000000, "effect": "mega_evolve", "target": "kangaskhan"},
    "latiasite": {"cost": 1000000, "effect": "mega_evolve", "target": "latias"},
    "latiosite": {"cost": 1000000, "effect": "mega_evolve", "target": "latios"},
    "lopunnite": {"cost": 1000000, "effect": "mega_evolve", "target": "lopunny"},
    "lucarionite": {"cost": 1000000, "effect": "mega_evolve", "target": "lucario"},
    "manectite": {"cost": 1000000, "effect": "mega_evolve", "target": "manectric"},
    "mawilite": {"cost": 1000000, "effect": "mega_evolve", "target": "mawile"},
    "medichamite": {"cost": 1000000, "effect": "mega_evolve", "target": "medicham"},
    "metagrossite": {"cost": 1000000, "effect": "mega_evolve", "target": "metagross"},
    "mewtwonite_x": {"cost": 1000000, "effect": "mega_evolve", "target": "mewtwo_x"},
    "mewtwonite_y": {"cost": 1000000, "effect": "mega_evolve", "target": "mewtwo_y"},
    "pidgeotite": {"cost": 1000000, "effect": "mega_evolve", "target": "pidgeot"},
    "pinsirite": {"cost": 1000000, "effect": "mega_evolve", "target": "pinsir"},
    "sablenite": {"cost": 1000000, "effect": "mega_evolve", "target": "sableye"},
    "salamencite": {"cost": 1000000, "effect": "mega_evolve", "target": "salamence"},
    "sceptilite": {"cost": 1000000, "effect": "mega_evolve", "target": "sceptile"},
    "scizorite": {"cost": 1000000, "effect": "mega_evolve", "target": "scizor"},
    "sharpedonite": {"cost": 1000000, "effect": "mega_evolve", "target": "sharpedo"},
    "slowbronite": {"cost": 1000000, "effect": "mega_evolve", "target": "slowbro"},
    "steelixite": {"cost": 1000000, "effect": "mega_evolve", "target": "steelix"},
    "swampertite": {"cost": 1000000, "effect": "mega_evolve", "target": "swampert"},
    "tyranitarite": {"cost": 1000000, "effect": "mega_evolve", "target": "tyranitar"},
    "venusaurite": {"cost": 1000000, "effect": "mega_evolve", "target": "venusaur"}
}

# === Baies ===
BERRIES = {
    "oran_berry": {"cost": 300, "effect": "heal", "value": 10},
    "sitrus_berry": {"cost": 800, "effect": "heal", "value": 25},
    "chesto_berry": {"cost": 400, "effect": "cure", "status": "sleep"},
    "pecha_berry": {"cost": 400, "effect": "cure", "status": "poison"},
    "rawst_berry": {"cost": 400, "effect": "cure", "status": "burn"},
    "aspear_berry": {"cost": 400, "effect": "cure", "status": "freeze"},
    "leppa_berry": {"cost": 600, "effect": "pp_restore", "value": 10},
    "lum_berry": {"cost": 1000, "effect": "cure", "status": "all"},
    "persim_berry": {"cost": 400, "effect": "cure", "status": "confusion"},
    "figy_berry": {"cost": 500, "effect": "heal_percent", "value": 0.33},
    "wiki_berry": {"cost": 500, "effect": "heal_percent", "value": 0.33},
    "mago_berry": {"cost": 500, "effect": "heal_percent", "value": 0.33},
    "aguav_berry": {"cost": 500, "effect": "heal_percent", "value": 0.33},
    "iapapa_berry": {"cost": 500, "effect": "heal_percent", "value": 0.33},
    "liechi_berry": {"cost": 2000, "effect": "boost_stat_on_low_hp", "stat": "atk"},
    "ganlon_berry": {"cost": 2000, "effect": "boost_stat_on_low_hp", "stat": "def"},
    "salac_berry": {"cost": 2000, "effect": "boost_stat_on_low_hp", "stat": "spe"},
    "petaya_berry": {"cost": 2000, "effect": "boost_stat_on_low_hp", "stat": "spa"},
    "apicot_berry": {"cost": 2000, "effect": "boost_stat_on_low_hp", "stat": "spd"},
    "lansat_berry": {"cost": 2500, "effect": "increase_crit_ratio"},
    "starf_berry": {"cost": 3000, "effect": "random_stat_boost_on_low_hp"},
    "enigma_berry": {"cost": 2000, "effect": "heal_when_hit_super_effective"},
    "custap_berry": {"cost": 2000, "effect": "move_first_on_low_hp"},
    "jaboca_berry": {"cost": 2000, "effect": "damage_contact_physical"},
    "rowap_berry": {"cost": 2000, "effect": "damage_contact_special"},
    "kee_berry": {"cost": 2000, "effect": "boost_def_when_hit_physically"},
    "maranga_berry": {"cost": 2000, "effect": "boost_spd_when_hit_special"}
}

# === Plaques d’Arceus ===
ARCEUS_PLATES = {
    "flame_plate": {"cost": 200000, "effect": "change_type", "type": "Fire"},
    "splash_plate": {"cost": 200000, "effect": "change_type", "type": "Water"},
    "zap_plate": {"cost": 200000, "effect": "change_type", "type": "Electric"},
    "meadow_plate": {"cost": 200000, "effect": "change_type", "type": "Grass"},
    "icicle_plate": {"cost": 200000, "effect": "change_type", "type": "Ice"},
    "fist_plate": {"cost": 200000, "effect": "change_type", "type": "Fighting"},
    "toxic_plate": {"cost": 200000, "effect": "change_type", "type": "Poison"},
    "earth_plate": {"cost": 200000, "effect": "change_type", "type": "Ground"},
    "sky_plate": {"cost": 200000, "effect": "change_type", "type": "Flying"},
    "mind_plate": {"cost": 200000, "effect": "change_type", "type": "Psychic"},
    "insect_plate": {"cost": 200000, "effect": "change_type", "type": "Bug"},
    "stone_plate": {"cost": 200000, "effect": "change_type", "type": "Rock"},
    "spooky_plate": {"cost": 200000, "effect": "change_type", "type": "Ghost"},
    "draco_plate": {"cost": 200000, "effect": "change_type", "type": "Dragon"},
    "dread_plate": {"cost": 200000, "effect": "change_type", "type": "Dark"},
    "iron_plate": {"cost": 200000, "effect": "change_type", "type": "Steel"},
    "pixie_plate": {"cost": 200000, "effect": "change_type", "type": "Fairy"}
}

TYPE_BOOST_ITEMS = {
    "charcoal": {"cost": 200000, "effect": "boost_type_damage", "type": "Fire"},
    "mystic_water": {"cost": 200000, "effect": "boost_type_damage", "type": "Water"},
    "magnet": {"cost": 200000, "effect": "boost_type_damage", "type": "Electric"},
    "miracle_seed": {"cost": 200000, "effect": "boost_type_damage", "type": "Grass"},
    "never_melt_ice": {"cost": 200000, "effect": "boost_type_damage", "type": "Ice"},
    "black_belt": {"cost": 200000, "effect": "boost_type_damage", "type": "Fighting"},
    "poison_barb": {"cost": 200000, "effect": "boost_type_damage", "type": "Poison"},
    "soft_sand": {"cost": 200000, "effect": "boost_type_damage", "type": "Ground"},
    "sharp_beak": {"cost": 200000, "effect": "boost_type_damage", "type": "Flying"},
    "twisted_spoon": {"cost": 200000, "effect": "boost_type_damage", "type": "Psychic"},
    "silver_powder": {"cost": 200000, "effect": "boost_type_damage", "type": "Bug"},
    "hard_stone": {"cost": 200000, "effect": "boost_type_damage", "type": "Rock"},
    "spell_tag": {"cost": 200000, "effect": "boost_type_damage", "type": "Ghost"},
    "dragon_fang": {"cost": 200000, "effect": "boost_type_damage", "type": "Dragon"},
    "black_glasses": {"cost": 200000, "effect": "boost_type_damage", "type": "Dark"},
    "metal_coat": {"cost": 200000, "effect": "boost_type_damage", "type": "Steel"},
    "pixie_dust": {"cost": 200000, "effect": "boost_type_damage", "type": "Fairy"}  # non-officiel mais blc c'est logique
}


# === Fusion de tout (pour accès global) ===
GENERAL_ITEMS = {}
for group in [HEALING_ITEMS, STATUS_ITEMS, PP_ITEMS, X_ITEMS, TRAINING_ITEMS, HELD_ITEMS, MEGA_ITEMS, BERRIES, ARCEUS_PLATES, TYPE_BOOST_ITEMS]:
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
    "PP": list(PP_ITEMS.keys()),
    "Boosts de combat": list(X_ITEMS.keys()),
    "Entraînement / EV": list(TRAINING_ITEMS.keys()),
    "Baies": list(BERRIES.keys()),
    "Objets boost de type" : list(TYPE_BOOST_ITEMS.keys()),
    "Objets tenus": list(HELD_ITEMS.keys()),
    "Méga-Gemmes" : list(MEGA_ITEMS.keys()),  
    "Plaques d'Arceus" : list(ARCEUS_PLATES.keys())
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
    "piece_rune": {"fr": "Pièce Rune", "en": "Amulet Coin"},
    "abomasite": {"fr": "Abomagonite", "en": "Abomasite"},
    "absolite": {"fr": "Absolite", "en": "Absolite"},
    "aerodactylite": {"fr": "Ptéraïte", "en": "Aerodactylite"},
    "aggronite": {"fr": "Galébronite", "en": "Aggronite"},
    "alakazite": {"fr": "Alakazamite", "en": "Alakazite"},
    "altarianite": {"fr": "Altarianite", "en": "Altarianite"},
    "ampharosite": {"fr": "Pharampite", "en": "Ampharosite"},
    "audinite": {"fr": "Nanméouïte", "en": "Audinite"},
    "banettite": {"fr": "Branettite", "en": "Banettite"},
    "beedrillite": {"fr": "Dardargnite", "en": "Beedrillite"},
    "blastoisinite": {"fr": "Tortankite", "en": "Blastoisinite"},
    "blazikenite": {"fr": "Braségalite", "en": "Blazikenite"},
    "cameruptite": {"fr": "Caméruptite", "en": "Cameruptite"},
    "charizardite_x": {"fr": "Dracaufite X", "en": "Charizardite X"},
    "charizardite_y": {"fr": "Dracaufite Y", "en": "Charizardite Y"},
    "diancite": {"fr": "Diancite", "en": "Diancite"},
    "galladite": {"fr": "Gallamite", "en": "Galladite"},
    "garchompite": {"fr": "Carchacrokite", "en": "Garchompite"},
    "gardevoirite": {"fr": "Gardevoirite", "en": "Gardevoirite"},
    "gengarite": {"fr": "Ectoplasmite", "en": "Gengarite"},
    "glalitite": {"fr": "Oniglalite", "en": "Glalitite"},
    "gyaradosite": {"fr": "Léviatorite", "en": "Gyaradosite"},
    "heracronite": {"fr": "Scarhinoïte", "en": "Heracronite"},
    "houndoominite": {"fr": "Démolossite", "en": "Houndoominite"},
    "kangaskhanite": {"fr": "Kangourexite", "en": "Kangaskhanite"},
    "latiasite": {"fr": "Latiasite", "en": "Latiasite"},
    "latiosite": {"fr": "Latiosite", "en": "Latiosite"},
    "lopunnite": {"fr": "Lockpinite", "en": "Lopunnite"},
    "lucarionite": {"fr": "Lucarite", "en": "Lucarionite"},
    "manectite": {"fr": "Élecsprintite", "en": "Manectite"},
    "mawilite": {"fr": "Mysdibulite", "en": "Mawilite"},
    "medichamite": {"fr": "Charminite", "en": "Medichamite"},
    "metagrossite": {"fr": "Métalossite", "en": "Metagrossite"},
    "mewtwonite_x": {"fr": "Mewtwoïte X", "en": "Mewtwonite X"},
    "mewtwonite_y": {"fr": "Mewtwoïte Y", "en": "Mewtwonite Y"},
    "pidgeotite": {"fr": "Roucarnagite", "en": "Pidgeotite"},
    "pinsirite": {"fr": "Scarabrutite", "en": "Pinsirite"},
    "sablenite": {"fr": "Ténéfixite", "en": "Sablenite"},  
    "salamencite": {"fr": "Drattakite", "en": "Salamencite"},
    "sceptilite": {"fr": "Jungkoïte", "en": "Sceptilite"},
    "scizorite": {"fr": "Cizayoxite", "en": "Scizorite"},
    "sharpedonite": {"fr": "Sharpedite", "en": "Sharpedonite"},
    "slowbronite": {"fr": "Flagadossite", "en": "Slowbronite"},
    "steelixite": {"fr": "Steelixite", "en": "Steelixite"},
    "swampertite": {"fr": "Laggronite", "en": "Swampertite"},
    "tyranitarite": {"fr": "Tyranocivite", "en": "Tyranitarite"},
    "venusaurite": {"fr": "Florizarreite", "en": "Venusaurite"},
    "oran_berry": {"fr": "Baie Oran", "en": "Oran Berry"},
    "sitrus_berry": {"fr": "Baie Sitrus", "en": "Sitrus Berry"},
    "chesto_berry": {"fr": "Baie Chesto", "en": "Chesto Berry"},
    "pecha_berry": {"fr": "Baie Pêcha", "en": "Pecha Berry"},
    "rawst_berry": {"fr": "Baie Fraive", "en": "Rawst Berry"},
    "aspear_berry": {"fr": "Baie Willia", "en": "Aspear Berry"},
    "leppa_berry": {"fr": "Baie Mepo", "en": "Leppa Berry"},
    "lum_berry": {"fr": "Baie Prine", "en": "Lum Berry"},
    "persim_berry": {"fr": "Baie Kika", "en": "Persim Berry"},
    "figy_berry": {"fr": "Baie Figuy", "en": "Figy Berry"},
    "wiki_berry": {"fr": "Baie Wiki", "en": "Wiki Berry"},
    "mago_berry": {"fr": "Baie Mago", "en": "Mago Berry"},
    "aguav_berry": {"fr": "Baie Gowav", "en": "Aguav Berry"},
    "iapapa_berry": {"fr": "Baie Papaya", "en": "Iapapa Berry"},
    "liechi_berry": {"fr": "Baie Litchi", "en": "Liechi Berry"},
    "ganlon_berry": {"fr": "Baie Gonlan", "en": "Ganlon Berry"},
    "salac_berry": {"fr": "Baie Salac", "en": "Salac Berry"},
    "petaya_berry": {"fr": "Baie Pitaya", "en": "Petaya Berry"},
    "apicot_berry": {"fr": "Baie Abriko", "en": "Apicot Berry"},
    "lansat_berry": {"fr": "Baie Lansat", "en": "Lansat Berry"},
    "starf_berry": {"fr": "Baie Frista", "en": "Starf Berry"},
    "enigma_berry": {"fr": "Baie Enigma", "en": "Enigma Berry"},
    "custap_berry": {"fr": "Baie Chérim", "en": "Custap Berry"},
    "jaboca_berry": {"fr": "Baie Jaboca", "en": "Jaboca Berry"},
    "rowap_berry": {"fr": "Baie Rudika", "en": "Rowap Berry"},
    "kee_berry": {"fr": "Baie Pomroz", "en": "Kee Berry"},
    "maranga_berry": {"fr": "Baie Maron", "en": "Maranga Berry"},
    "air_balloon": {"fr": "Ballon", "en": "Air Balloon"},
    "mental_herb": {"fr": "Herbe Mentale", "en": "Mental Herb"},
    "white_herb": {"fr": "Herbe Blanche", "en": "White Herb"},
    "power_herb": {"fr": "Herbe Pouvoir", "en": "Power Herb"},
    "eject_button": {"fr": "Bouton Fuite", "en": "Eject Button"},
    "red_card": {"fr": "Carton Rouge", "en": "Red Card"},
    "room_service": {"fr": "Room Service", "en": "Room Service"},
    "throat_spray": {"fr": "Bouchon d’Oreilles", "en": "Throat Spray"},
    "blunder_policy": {"fr": "Assurance Raté", "en": "Blunder Policy"},
    "absorbing_bulb": {"fr": "Ampoule", "en": "Absorb Bulb"},
    "cell_battery": {"fr": "Pile", "en": "Cell Battery"},
    "luminous_moss": {"fr": "Mousse Ténue", "en": "Luminous Moss"},
    "snowball": {"fr": "Boule de Neige", "en": "Snowball"},
    "weakness_policy": {"fr": "Vulné-Assurance", "en": "Weakness Policy"},
    "policy_armor": {"fr": "Armure Résistance", "en": "Policy Armor"},
    "iron_ball": {"fr": "Balle Fer", "en": "Iron Ball"},
    "lagging_tail": {"fr": "Ralentiqueue", "en": "Lagging Tail"},
    "full_incense": {"fr": "Encens Pur", "en": "Full Incense"},
    "quick_powder": {"fr": "Poudre Vite", "en": "Quick Powder"},
    "grip_claw": {"fr": "Griffes Ténacité", "en": "Grip Claw"},
    "binding_band": {"fr": "Bande Étreinte", "en": "Binding Band"},
    "shed_shell": {"fr": "Exuvie", "en": "Shed Shell"},
    "sticky_barb": {"fr": "Pointe Ferreuse", "en": "Sticky Barb"},
    "flame_plate": {"fr": "Plaque Flamme", "en": "Flame Plate"},
    "splash_plate": {"fr": "Plaque Hydro", "en": "Splash Plate"},
    "zap_plate": {"fr": "Plaque Volt", "en": "Zap Plate"},
    "meadow_plate": {"fr": "Plaque Herbe", "en": "Meadow Plate"},
    "icicle_plate": {"fr": "Plaque Glace", "en": "Icicle Plate"},
    "fist_plate": {"fr": "Plaque Poing", "en": "Fist Plate"},
    "toxic_plate": {"fr": "Plaque Toxik", "en": "Toxic Plate"},
    "earth_plate": {"fr": "Plaque Terre", "en": "Earth Plate"},
    "sky_plate": {"fr": "Plaque Ciel", "en": "Sky Plate"},
    "mind_plate": {"fr": "Plaque Esprit", "en": "Mind Plate"},
    "insect_plate": {"fr": "Plaque Insecte", "en": "Insect Plate"},
    "stone_plate": {"fr": "Plaque Roc", "en": "Stone Plate"},
    "spooky_plate": {"fr": "Plaque Fantôme", "en": "Spooky Plate"},
    "draco_plate": {"fr": "Plaque Draco", "en": "Draco Plate"},
    "dread_plate": {"fr": "Plaque Ombre", "en": "Dread Plate"},
    "iron_plate": {"fr": "Plaque Fer", "en": "Iron Plate"},
    "pixie_plate": {"fr": "Plaque Pixie", "en": "Pixie Plate"},
    "focus_band": {"fr": "Bandeau", "en": "Focus Band"},
    "lentilscope": {"fr": "Lentilscope", "en": "Scope Lens"},
    "balle_lumiere": {"fr": "Balle Lumière", "en": "Light Ball"},
    "graines_psy": {"fr": "Graine Psychique", "en": "Psychic Seed"},
    "graines_brume": {"fr": "Graine Brume", "en": "Misty Seed"},
    "graines_electr": {"fr": "Graine Électrifiée", "en": "Electric Seed"},
    "graines_herbe": {"fr": "Graine Herbe", "en": "Grassy Seed"},
    "vitamin_max": {"fr": "Vitamine Max", "en": "Max Vitamin"},
    "reset_bag": {"fr": "Sac Réinitialisation", "en": "Reset Bag"}
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
    "Baies": {"fr": "Baies", "en": "Berries"},
    "Objets boost de type": {"fr": "Objets boost de type", "en": "Type Boost Items"},
    "Méga-Gemmes": {"fr": "Méga-Gemmes", "en": "Mega Stones"},
    "Plaques d'Arceus": {"fr": "Plaques d’Arceus", "en": "Arceus Plates"}
}

# ✅ Ajout pour éviter erreur d'import
SHOP_CATEGORY_PREFIX = "🛒"
