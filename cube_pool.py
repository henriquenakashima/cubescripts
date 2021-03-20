# Loads disjoint pools from a cube CSV

import csv
import dataclasses
import itertools
import random
from collections import defaultdict
from typing import Dict, List, Set

import cubecobra_csv
from cubecobra_csv import CubeCard


class CubePool:
    def __init__(self):
        self._categories: List[CubeCard] = defaultdict(list)

    def add_card(self, card: CubeCard):
        self._categories[card.color_category].append(card)

    def wide_sample(self, n: int) -> List[CubeCard]:
        wide_iterator = list(itertools.chain.from_iterable(self._categories.values()))
        sample = random.sample(wide_iterator, n)
        return sample

    def category_sample(self, color_category: str, n: int) -> List[CubeCard]:
        return random.sample(self._categories[color_category], n)

    def draw_from_category(self, color_category: str, n: int) -> List[CubeCard]:
        drawn = self.category_sample(color_category, n)
        self.remove_cards(drawn, color_category)
        return drawn

    def remove_cards(self, removed: List[CubeCard], color_category: str):
        existing = self._categories[color_category]
        self._categories[color_category] = [c for c in existing if not c in removed]

    def fetch(self, card_name: str, color_category: str) -> CubeCard:
        found: List[CubeCard] = list(filter(lambda c: c.name == card_name, self._categories[color_category]))
        assert len(found) >= 1
        card_taken: CubeCard = found[0]
        self.remove_cards([card_taken], color_category)
        return card_taken

    def get_category(self, color_category: str) -> List[CubeCard]:
        return self._categories[color_category]


def load_pools(csv_path: str, pool_tags: Set[str]) -> Dict[str, CubePool]:
    pools = defaultdict(CubePool)
    cube: List[CubeCard] = cubecobra_csv.load_cube(csv_path)

    for cube_card in cube:
        pool_tags_for_card = pool_tags.intersection(cube_card.tags)
        if len(pool_tags_for_card) == 0:
            print(f'{cube_card.name} does not have any of the tags: {pool_tags}')
        elif len(pool_tags_for_card) > 1:
            print(f'{cube_card.name} should only be tagged as one in {pool_tags} '
                  'but is tagged as {pool_tags_for_card}')
        else:
            (pool_tag,) = pool_tags_for_card
            pools[pool_tag].add_card(cube_card)

    return pools

