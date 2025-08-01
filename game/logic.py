from models.orc import random_orc


def generate_orcs():
    return [random_orc() for _ in range(3)]


def player_attack(player, orc, card):
    if player.mana >= card.mana_cost:
        player.mana -= card.mana_cost
        orc.life -= card.damage
        if orc.life <= 0:
            return "orc_defeated"
        return "attack_successful"
    return "not_enough_mana"
