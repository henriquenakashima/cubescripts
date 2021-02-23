# Loads disjoint pools from a cube CSV

import csv
from collections import defaultdict
from typing import Dict, List, Set

import cubecobra_csv


def load_pools(csv_path: str, pool_tags: Set[str]) -> Dict[str, List[str]]:
    pools = defaultdict(list)
    with open(csv_path) as f:
        reader = csv.reader(f)
        header_line = next(reader)
        cubecobra_csv.assert_header(header_line)
        for line in reader:
            card = line[cubecobra_csv.COLUMNS['Name']]
            tags = set(line[cubecobra_csv.COLUMNS['Tags']].split(', '))
            # print(f'{card} {tags}')
            pool_tags_for_card = pool_tags.intersection(tags)
            if len(pool_tags_for_card) == 0:
                print(f'{card} does not have any of the tags: {pool_tags}')
            elif len(pool_tags_for_card) == 1:
                (pool_tag,) = pool_tags_for_card
                pools[pool_tag].append(card)
            else:
                print(f'{card} should only be tagged as one in {pool_tags} '
                      'but is tagged as {pool_tags_for_card}')
    return pools
