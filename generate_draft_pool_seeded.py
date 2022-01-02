# Generate a draft pool for mtgadraft.tk or dr4ft.info
# Seeds color categories.
import collections
import itertools
import math
import random

import cube_pool
import cubecobra_csv

from cubecobra_csv import CubeCard

DEBUG_PRINT = False

SEATS = 5
SEEDING = [
    'oowubrgcfxxxx',
    'owubrgcfxxxxx',
    'wubrgcfxxxxxx',
    'wubrgcfxxxxxx'
]
ROUNDS = len(SEEDING)
PACKS = ROUNDS * SEATS

FIXING_TAG = 'gold_land'
CATEGORIES_TO_INCLUDE_ALL = ['f']

CUBE_NAME = 'TheElegantCube_fetched'

OUTPUT_FILENAME = 'cards_in_draft.txt'


def main():
    csv_path = cubecobra_csv.request_cube_csv('TheElegantCube_fetched', 'elegant')

    pools = cube_pool.load_pools(csv_path, {'core', 'occasional'})
    pools['core'].split_category_by_tag('l', FIXING_TAG, 'f', 'l')
    pools['core'].join_categories(['m', 'h'], 'm')

    seeded_slots_per_category = collections.Counter(itertools.chain.from_iterable(SEEDING))
    seeded_size_per_category = {}
    for category in 'owubrgcflmx':
        seeded_category_size = seeded_slots_per_category[category] * SEATS
        print(f'seeded_category_size of cat {category} is {seeded_category_size}')
        seeded_size_per_category[category] = seeded_category_size

    total_core_pool_to_use = sum(seeded_size_per_category.values()) - seeded_size_per_category['o']
    for category in CATEGORIES_TO_INCLUDE_ALL:
        total_core_pool_to_use -= seeded_size_per_category[category]
    print('total_core_pool_to_use %d' % total_core_pool_to_use)

    core_size_per_category = {}
    core_size_to_split = 0
    for category in 'wubrgcflm':
        core_category_size = len(pools['core'].get_category(category))
        print(f'core size of cat {category} is {core_category_size}')
        core_size_per_category[category] = core_category_size
        if category not in CATEGORIES_TO_INCLUDE_ALL:
            core_size_to_split += core_category_size

    print(f'total_core_pool_to_use: {total_core_pool_to_use}')
    print(f'core_size_to_split: {core_size_to_split}')
    percentage_of_core = total_core_pool_to_use / core_size_to_split
    print(f'percentage of core to use: {percentage_of_core}')

    desired_size_per_category = {}
    for category in 'wubrgcflm':
        if category in CATEGORIES_TO_INCLUDE_ALL:
            desired_category_size = core_size_per_category[category]
        else:
            desired_category_size = math.ceil(percentage_of_core * core_size_per_category[category])
        print(f'desired size of cat {category} is {desired_category_size}')
        desired_size_per_category[category] = desired_category_size

    leftover_pool = []
    for category in 'wubrgcflm':
        assert(seeded_size_per_category[category] <= desired_size_per_category[category]), \
               (f'Cannot seed {seeded_size_per_category[category]} cards from category {category} from desired size '
                f'{desired_size_per_category[category]}')
        leftover_category_size = desired_size_per_category[category] - seeded_size_per_category[category]
        leftovers = pools['core'].draw_from_category(category, leftover_category_size)
        leftover_pool.extend(leftovers)
    random.shuffle(leftover_pool)

    position_pools_per_round = []
    for round_seeding in SEEDING:
        position_pools = []
        for pos, category in enumerate(round_seeding):
            if category in 'wubrgcflm':
                drawn = pools['core'].draw_from_category(category, SEATS)
            elif category in 'x':
                drawn = None
            elif category in 'o':
                drawn = pools['occasional'].wide_sample(SEATS)
            else:
                raise ValueError(f'Category cannot be {category}')
            position_pools.append(drawn)
        position_pools_per_round.append(position_pools)


    boosters = []
    for round_seeding, position_pools in zip(SEEDING, position_pools_per_round):
        for s in range(SEATS):
            booster = []
            for category, position_pool in zip(round_seeding, position_pools):
                if category in 'owubrgcflm':
                    card = position_pool.pop()
                elif category in 'x':
                    card = leftover_pool.pop()
                booster.append(card)

            boosters.append(booster)

    with open(OUTPUT_FILENAME, 'wb') as f:
        for booster in boosters:
            def render_card_line(card: CubeCard) -> str:
                if DEBUG_PRINT:
                    return f'{card.name} ({card.color_category})'
                else:
                    return card.name
            booster_names = [render_card_line(card) for card in booster]
            booster_contents = '\n'.join(booster_names).encode('utf-8')
            f.write(booster_contents)
            f.write(b'\n\n')
        print(f'Wrote {len(boosters)} boosters to {OUTPUT_FILENAME}')


if __name__ == '__main__':
    main()
