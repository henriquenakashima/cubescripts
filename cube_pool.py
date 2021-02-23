# Loads disjoint pools from a cube CSV

import csv
import itertools
import random
from collections import defaultdict
from typing import Dict, Set

import cubecobra_csv


class CubePool:
    def __init__(self):
        self._categories = defaultdict(list)

    def add_card(self, card_name: str, color_category: str):
        assert color_category in 'wubrgchml', f'{card_name}: {color_category}'
        self._categories[color_category].append(card_name)

    def wide_sample(self, n: int):
        wide_iterator = list(itertools.chain.from_iterable(self._categories.values()))
        return random.sample(wide_iterator, n)


def load_pools(csv_path: str, pool_tags: Set[str]) -> Dict[str, CubePool]:
    pools = defaultdict(CubePool)
    with open(csv_path) as f:
        reader = csv.reader(f)
        header_line = next(reader)
        cubecobra_csv.assert_header(header_line)
        for line in reader:
            card = cubecobra_csv.get_name(line)
            tags = cubecobra_csv.get_tags(line)
            # print(f'{card} {tags}')
            pool_tags_for_card = pool_tags.intersection(tags)
            if len(pool_tags_for_card) == 0:
                print(f'{card} does not have any of the tags: {pool_tags}')
            elif len(pool_tags_for_card) > 1:
                print(f'{card} should only be tagged as one in {pool_tags} '
                      'but is tagged as {pool_tags_for_card}')
            else:
                (pool_tag,) = pool_tags_for_card
                color_category = cubecobra_csv.get_color_category(line)
                # print(f'{card} {color_category}')
                pools[pool_tag].add_card(card, color_category)
    return pools

