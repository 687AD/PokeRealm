# core/lang.py

from core.translation_data import POKEMON_NAMES

def resolve_pokemon_internal_name(display_name, lang):
    for internal_name, names in POKEMON_NAMES.items():
        if names.get(lang, "").lower() == display_name.lower():
            return internal_name
    return display_name.lower()  # fallback si pas trouvé

TEXTS = {
    "wild_appears_simple": {
        "fr": "Un Pokémon sauvage apparaît !",
        "en": "A wild Pokémon appeared!"
    },
    "name_label": {
        "fr": "Nom :",
        "en": "Name:"
    },
    "rarity_label": {
        "fr": "Rareté :",
        "en": "Rarity:"
    },
    "status_label": {
        "fr": "Statut :",
        "en": "Status:"
    },
    "already_caught": {
        "fr": "✅ Déjà capturé",
        "en": "✅ Already caught"
    },
    "new_catch": {
        "fr": "❌ Nouveau Pokémon",
        "en": "❌ New Pokémon"
    },
    "common": {"fr": "Commun", "en": "Common"},
    "uncommon": {"fr": "Peu commun", "en": "Uncommon"},
    "rare": {"fr": "Rare", "en": "Rare"},
    "epic": {"fr": "Épique", "en": "Epic"},
    "legendary": {"fr": "Légendaire", "en": "Legendary"},
    "mythic": {"fr": "Mythique", "en": "Mythic"},

    "wait_roulette": {
        "fr": "⏳ Patiente encore {seconds} seconde(s) avant une nouvelle roulette.",
        "en": "⏳ Please wait {seconds} second(s) before spinning again."
    },
    "stats_command_usage": {
    "fr": "📊 Utilisation : /stats <Nom du Pokémon>",
    "en": "📊 Usage: /stats <Pokemon Name>"
    },
    "new_stats": {
        "fr": "📊 Nouvelles stats : PV: {hp} | Att: {atk} | Def: {def_} | Atq Spé: {spa} | Déf Spé: {spd} | Vit: {spe}",
        "en": "📊 New stats: HP: {hp} | Atk: {atk} | Def: {def_} | SpA: {spa} | SpD: {spd} | Spe: {spe}"
    },
    "menu_help": {
        "fr": "📖 Aide",
        "en": "📖 Help"
    },
    "menu_inventory": {
        "fr": "🎒 Sac",
        "en": "🎒 Bag"
    },
    "menu_box": {
        "fr": "📦 Boîte Pokémon",
        "en": "📦 PokéBox"
    },
    "choose_sorting": {
        "fr": "📊 Choisis un type de tri :",
        "en": "📊 Choose a sorting method:"
    },
    "button_sort_box": {
        "fr": "🔽 Trier",
        "en": "🔽 Sort"
    },
    "choose_language": {
        "fr": "🌍 Choisis ta langue :",
        "en": "🌍 Choose your language:"
    },
    "lang_set": {
        "fr": "✅ Langue définie sur Français.",
        "en": "✅ Language set to English."
    },
    "start_welcome": {
        "fr": "👋 Salut {name} ! Bienvenue dans le monde des Pokémon !",
        "en": "👋 Hi {name}! Welcome to the world of Pokémon!"
    },
    "daily_already": {
        "fr": "⏳ Tu as déjà réclamé ta récompense aujourd'hui !",
        "en": "⏳ You've already claimed your daily reward today!"
    },
    "daily_reward": {
        "fr": "🎁 Tu as reçu 1000 pokédollars et 10 Pokéball !",
        "en": "🎁 You received 1000 Pokédollars and 10 Pokéball!"
    },
    "choose_ball": {
        "fr": "Choisis une Pokéball pour tenter une capture :",
        "en": "Choose a Pokéball to attempt a capture:"
    },
    "no_ball": {
        "fr": "❌ Tu n’as plus de {ball} !",
        "en": "❌ You have no more {ball}!"
    },
    "catch_failed": {
        "fr": "💨 Le Pokémon s’est enfui !",
        "en": "💨 The Pokémon ran away!"
    },
    "catch_success": {
        "fr": "✅ Tu as capturé {name} ! +{money}💰",
        "en": "✅ You caught {name}! +{money}💰"
    },
    "not_enough_money": {
        "fr": "❌ Pas assez de pokédollars.",
        "en": "❌ Not enough Pokédollars."
    },
    "item_unknown": {
        "fr": "❌ Objet inconnu.",
        "en": "❌ Unknown item."
    },
    "enter_quantity": {
        "fr": "🧮 Combien veux-tu en acheter ?",
        "en": "🧮 How many do you want to buy?"
    },
    "invalid_number": {
        "fr": "❌ Merci d'entrer un nombre valide.",
        "en": "❌ Please enter a valid number."
    },
    "purchase_confirm": {
        "fr": "✅ {quantity} x {item} achetés pour {price}💰.",
        "en": "✅ {quantity} x {item} bought for {price}💰."
    },
    "no_pokemon_available": {
        "fr": "❌ Aucun Pokémon disponible.",
        "en": "❌ No Pokémon available."
    },
    "back_to_menu": {
        "fr": "⬅️ Retour au menu principal.",
        "en": "⬅️ Back to main menu."
    },
    "shop_intro": {
        "fr": "🛒 BOUTIQUE\n\nTu peux acheter les objets suivants :\n",
        "en": "🛒 SHOP\n\nYou can buy the following items:\n"
    },
    "shop_instruction": {
        "fr": "Clique sur un objet pour l’acheter (quantité au choix).",
        "en": "Click an item to buy (quantity will be asked)."
    },
    "wild_appears": {
        "fr": "🌿 Un Pokémon sauvage apparaît : {name} !",
        "en": "🌿 A wild Pokémon appears: {name}!"
    },
    "choose_another_ball": {
        "fr": "💡 Choisis une autre Pokéball.",
        "en": "💡 Choose another Pokéball."
    },
    "no_more_balls": {
        "fr": "💥 Tu n’as plus aucune Pokéball ! Retour au menu.",
        "en": "💥 You have no Pokéballs left! Returning to menu."
    },
    "menu_roulette": {
        "fr": "🎰 Roulette",
        "en": "🎰 Catch"
    },
    "menu_shop": {
        "fr": "🛒 Boutique",
        "en": "🛒 Shop"
    },
    "menu_money": {
        "fr": "💰 Argent",
        "en": "💰 Money"
    },
    "menu_lang": {
        "fr": "🌍 Langue",
        "en": "🌍 Language"
    },
    "menu_back": {
        "fr": "🔙 Retour",
        "en": "🔙 Back"
    },
    "duplicates_sold": {
        "fr": "✅ Tous les doublons ont été vendus. +{money} pokédollars gagnés.",
        "en": "✅ All duplicates sold. You earned +{money} Pokédollars."
    },
    "button_sell_duplicates": {
        "fr": "🗑 Vendre doublons",
        "en": "🗑 Sell duplicates"
    },
    "no_duplicates": {
        "fr": "❌ Aucun doublon à vendre.",
        "en": "❌ No duplicates to sell."
    },
    "iv_stack_message": {
        "fr": "📈 {count} IV(s) ont été améliorés sur ton Pokémon principal.",
        "en": "📈 {count} IV(s) were improved on your main Pokémon."
    },
    "hidden_ability_stack_message": {
        "fr": "✨ Le talent caché a été ajouté à ton Pokémon principal.",
        "en": "✨ Hidden ability was added to your main Pokémon."
    },
    "nature_command_usage": {
        "fr": "❗ Utilisation : /nature <nom du Pokémon> <nature>",
        "en": "❗ Usage: /nature <pokemon name> <nature>"
    },
    "nature_usage": {
        "fr": "❗ Utilisation : /nature <NomDuPokémon> <Nature>",
        "en": "❗ Usage: /nature <PokemonName> <Nature>"
    },
    "nature_not_known": {
        "fr": "❌ Cette nature n'est pas encore connue pour ce Pokémon.",
        "en": "❌ This nature is not yet known for this Pokémon."
    },
    "pokemon_not_found": {
        "fr": "❌ Aucun Pokémon avec ce nom dans ta box.",
        "en": "❌ No Pokémon with that name in your box."
    },
    "nature_changed": {
        "fr": "✅ Nature changée pour {nature}.",
        "en": "✅ Nature changed to {nature}."
    },
    "nature_stack_message": {
        "fr": "🍃 {count} nouvelle(s) nature(s) ont été apprises par ton Pokémon principal.",
        "en": "🍃 {count} new nature(s) were learned by your main Pokémon."
    },
    "previous_page": {
        "fr": "🔼 Page précédente",
        "en": "🔼 Previous page"
    },
    "next_page": {
        "fr": "🔽 Page suivante",
        "en": "🔽 Next page"
    }
}

def get_text(key, lang="fr", **kwargs):
    text = TEXTS.get(key, {}).get(lang, "")
    return text.format(**kwargs)
