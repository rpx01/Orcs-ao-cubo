


def player_attack(player, orc, card):
    if player.mana >= card.mana_cost:
        player.mana -= card.mana_cost
        orc.life -= card.damage
        if orc.life <= 0:
            return "orc_defeated"
        return "attack_successful"
    return "not_enough_mana"


def advance_orcs(game_map):
    """Move todos os orcs no mapa uma posição para a frente."""
    orcs_at_gate = []
    for lane in game_map.values():
        if lane[2]:
            orcs_at_gate.extend(lane[2])
            lane[2] = []
        if lane[1]:
            lane[2].extend(lane[1])
            lane[1] = []
        if lane[0]:
            lane[1].extend(lane[0])
            lane[0] = []
    return orcs_at_gate
