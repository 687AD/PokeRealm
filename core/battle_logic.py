def calculate_damage(attacker, defender):
    base_power = attacker["move"]["power"]
    attack = attacker["stats"]["attack"]
    defense = defender["stats"]["defense"]
    return max(1, int((base_power * attack / defense) * 0.5))  # formule simplifiée
