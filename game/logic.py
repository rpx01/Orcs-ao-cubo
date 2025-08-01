from models.orc import random_orc


def generate_orcs(round_number):
    """Gera uma lista de orcs para a rodada informada."""
    # A cada rodada, os orcs terão mais vida e darão mais pontos
    return [random_orc(round_number) for _ in range(3)]


def player_attack(player, orc, card):
    if player.mana >= card.mana_cost:
        player.mana -= card.mana_cost
        orc.life -= card.damage
        if orc.life <= 0:
            return "orc_defeated"
        return "attack_successful"
    return "not_enough_mana"
