# core/items.py

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
    "mythic" : 0.01
}

BALL_COSTS = {
    "pokeball": 100,
    "superball": 300,
    "hyperball": 1000,
    "masterball": 10000
}

ITEM_COSTS = {
    "chroma": 10000,
    "multi_exp": 20000
}

def get_capture_chance(ball_type, rarity):
    return BALL_RATES.get(ball_type, 0) * RARITY_RATES.get(rarity, 0)

def can_afford(user_data, item, quantity=1):
    price = BALL_COSTS.get(item) or ITEM_COSTS.get(item)
    return user_data["money"] >= price * quantity

def buy_item(user_data, item, quantity):
    price = BALL_COSTS.get(item) if item in BALL_COSTS else ITEM_COSTS.get(item)
    total = price * quantity
    if user_data["money"] >= total:
        user_data["money"] -= total
        if item in user_data["pokeballs"]:
            user_data["pokeballs"][item] += quantity
        elif item in user_data["items"]:
            user_data["items"][item] += quantity
        return True
    return False
