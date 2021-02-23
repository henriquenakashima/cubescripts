# Loads disjoint pools from a cube CSV

import csv
import dataclasses
import itertools
import random
from collections import defaultdict
from typing import Dict, List, Set

import cubecobra_csv


@dataclasses.dataclass
class Card:
    name: str
    color_category: str
    colors: List[str]
    tags: List[str]

    def __post_init__(self):
        assert self.color_category in 'wubrgchml0', f'{self}'

    def __repr__(self):
        return self.name


class CubePool:
    def __init__(self):
        self._categories: List[Card] = defaultdict(list)

    def add_card(self, card: Card):
        self._categories[card.color_category].append(card)

    def wide_sample(self, n: int) -> List[Card]:
        wide_iterator = list(itertools.chain.from_iterable(self._categories.values()))
        sample = random.sample(wide_iterator, n)
        return sample

    def category_sample(self, color_category: str, n: int) -> List[Card]:
        return random.sample(self._categories[color_category], n)

    def draw_from_category(self, color_category: str, n: int) -> List[Card]:
        drawn = self.category_sample(color_category, n)
        self.remove_cards(drawn, color_category)
        return drawn

    def remove_cards(self, removed: List[Card], color_category: str):
        existing = self._categories[color_category]
        self._categories[color_category] = [c for c in existing if not c in removed]

    def fetch(self, card_name: str, color_category: str) -> Card:
        found: List[Card] = list(filter(lambda c: c.name == card_name, self._categories[color_category]))
        assert len(found) >= 1
        card_taken: Card = found[0]
        self.remove_cards([card_taken], color_category)
        return card_taken

    def get_category(self, color_category: str) -> List[Card]:
        return self._categories[color_category]


def load_pools(csv_path: str, pool_tags: Set[str]) -> Dict[str, CubePool]:
    pools = defaultdict(CubePool)
    with open(csv_path) as f:
        reader = csv.reader(f)
        header_line = next(reader)
        cubecobra_csv.assert_header(header_line)
        for line in reader:
            card_name = cubecobra_csv.get_name(line)
            tags = cubecobra_csv.get_tags(line)
            # print(f'{card_name} {tags}')
            pool_tags_for_card = pool_tags.intersection(tags)
            if len(pool_tags_for_card) == 0:
                print(f'{card_name} does not have any of the tags: {pool_tags}')
            elif len(pool_tags_for_card) > 1:
                print(f'{card_name} should only be tagged as one in {pool_tags} '
                      'but is tagged as {pool_tags_for_card}')
            else:
                (pool_tag,) = pool_tags_for_card
                color_category = cubecobra_csv.get_color_category(line)
                # print(f'{card_name} {color_category}')
                colors = cubecobra_csv.get_colors(line)
                print(f'{card_name} {colors}')
                card = Card(card_name, color_category, colors, tags)
                pools[pool_tag].add_card(card)
    return pools

