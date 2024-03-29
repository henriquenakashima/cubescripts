# Play Rogue Duel, a 2-player format in which players duel multiple times,
# improving their decks between games.

import random
from collections import Counter
from pathlib import Path
from typing import Dict, List

import cube_pool
import cubecobra_csv
from cubecobra_csv import CubeCard

CUBE_NAME = 'TheElegantCube_fetched'


class RogueDuelPlayerState:
    def __init__(self):
        self.colors: List[str] = []
        self.deck: List[CubeCard] = []


class RogueDuelState:
    def __init__(self):
        self.player1 = RogueDuelPlayerState()
        self.player2 = RogueDuelPlayerState()
        self.player_states = (self.player1, self.player2)

        csv_path = cubecobra_csv.request_cube_csv('TheElegantCube_fetched', 'elegant')
        self.pools: Dict[str, cube_pool.CubePool] = cube_pool.load_pools(csv_path, {'core', 'occasional'})
        self.discard_pile: List[CubeCard] = []


def main():
    state = RogueDuelState()
    _decide_colors(state)
    _pick_artifacts(state)
    _fill_with_lands(state)
    print(state.player1.deck)
    print(state.player2.deck)
    _export_decks(state)


def _decide_colors(state: RogueDuelState):
    sealed_pools: Dict[str, List[CubeCard]] = {}
    for color_category in 'wubrg':
        sealed_pools[color_category] = (state.pools['core'].draw_from_category(color_category, 6) +
                                        state.pools['occasional'].draw_from_category(color_category, 2))
    print(sealed_pools)

    colors_available = list('wubrg')
    color = random.choice('wubrg')
    colors_available.remove(color)
    print(f'Player 1 assigned color: {color}')
    state.player1.colors.append(color)
    state.player1.deck.extend(sealed_pools[color])

    color = _pick_a_color(colors_available, 'Player 2, choose your first color from:')
    state.player2.colors.append(color)
    state.player2.deck.extend(sealed_pools[color])

    color = _pick_a_color(colors_available, 'Player 1, choose your second color from:')
    state.player1.colors.append(color)
    state.player1.deck.extend(sealed_pools[color])

    color = _pick_a_color(colors_available, 'Player 2, choose your second color from:')
    state.player2.colors.append(color)
    state.player2.deck.extend(sealed_pools[color])

    state.discard_pile.extend(sealed_pools[colors_available[0]])


def _pick_a_color(colors_available: List[str], prompt: str) -> str:
    color = ''
    while color not in colors_available:
        color = input(f'{prompt} {colors_available}')
    colors_available.remove(color)
    return color


def _pick_artifacts(state: RogueDuelState):
    artifact_pool: List[CubeCard] = (state.pools['core'].draw_from_category('c', 4) +
                                           state.pools['occasional'].draw_from_category('c', 1))
    print(artifact_pool)
    card = _pick_a_card(artifact_pool, 'Player 1, choose an artifact:')
    state.player1.deck.append(card)
    card = _pick_a_card(artifact_pool, 'Player 2, choose an artifact:')
    state.player2.deck.append(card)
    state.discard_pile.extend(artifact_pool)


def _pick_a_card(cards_available: List[CubeCard], prompt: str) -> CubeCard:
    for i, card in enumerate(cards_available, 1):
        print(f'[{i:>2}] {card.name}')
    index_chosen = -1
    while index_chosen < 0 or index_chosen >= len(cards_available):
        index_chosen = int(input(prompt)) - 1
    card_chosen = cards_available[index_chosen]
    cards_available.remove(card_chosen)
    return card_chosen


def _fill_with_lands(state: RogueDuelState):
    RAINBOW_DUALS = [state.pools['core'].fetch('Terramorphic Expanse', 'l'),
                     state.pools['core'].fetch('Evolving Wilds', 'l')]
    state.pools['core'].remove_cards(RAINBOW_DUALS, 'l')
    for player_state, rainbow_land in zip(state.player_states, RAINBOW_DUALS):
        for color in player_state.colors:
            player_state.deck.extend([_basic_for_color(color) for _ in range(5)])
        player_state.deck.append(rainbow_land)
        # Add two duals
        duals = _fetch_duals(state, player_state.colors)
        assert len(duals) == 2, f'Found duals {duals} for colors {player_state.colors}'
        player_state.deck.extend(duals)


def _basic_for_color(color: str) -> str:
    name = {'w': 'Plains', 'u': 'Island', 'b': 'Swamp', 'r': 'Mountain', 'g': 'Forest'}[color]
    return CubeCard(name, '0', [color], [])


def _fetch_duals(state: RogueDuelState, colors: List[str]) -> List[CubeCard]:
    colors = sorted(colors)
    duals = []
    # Get duals
    core_lands: List[CubeCard] = state.pools['core'].get_category('l')
    for land in core_lands:
        if land.colors == colors:
            duals.append(land)
    state.pools['core'].remove_cards(duals, 'l')
    return duals


def _export_decks(state: RogueDuelState):
    decks_path = Path('decks')
    decks_path.mkdir(exist_ok=True)
    for i, player_state in enumerate(state.player_states):
        filepath = decks_path / f'player{i + 1}_deck.txt'
        _export_deck(player_state.deck, filepath)


def _export_deck(deck: List[CubeCard], filepath: Path):
    deck_counter = Counter([card.name for card in deck])
    with open(filepath, 'w') as f:
        for card_name, quantity in deck_counter.most_common():
            f.write(f'{quantity} {card_name}\n')


if __name__ == '__main__':
    main()
