# Generate a report of how many archetype cards are in each color category

import argparse
from collections import defaultdict

import cubecobra_csv

CUBE_NAME = 'TheElegantCube_fetched'

ARCHETYPE_TAGS = [
    'counters',
    'artifacts',
    'tokens',
    'sacrifice',
    'graveyard',
    'reanimator',

    'humans',
    'wizards',
    'zombies',
    'goblins',
    'elves',
    'burn',
    'ramp',

    'tappers',
    'lifegain',
    'flash',
    'flash',
    'spells',

    'blink',
    'heroic',
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--archetype')
    arguments = parser.parse_args()

    csv_path = cubecobra_csv.request_cube_csv('TheElegantCube_fetched', 'elegant')

    cube_cards = cubecobra_csv.load_cube(csv_path)
    archetype_counts_per_category = defaultdict(lambda: defaultdict(list))
    for cube_card in cube_cards:
        if 'core' not in cube_card.tags:
            continue
        for tag in cube_card.tags:
            if tag in ARCHETYPE_TAGS:
                archetype_counts_per_category[tag][cube_card.color_category].append(cube_card)

    if not arguments.archetype:
        for tag in ARCHETYPE_TAGS:
            print(f'Archetype: {tag}')
            cards_per_category = archetype_counts_per_category[tag]
            for category, cards in cards_per_category.items():
                print(f'{category} {len(cards)}')
            print()
    else:
        cards_per_category = archetype_counts_per_category[arguments.archetype]

        for category, cards in cards_per_category.items():
            print(f'Category: {category} - {len(cards)} card{"s" if len(cards) != 1 else ""}')
            for i, card in enumerate(cards, 1):
                print(f'{i:2d} {card.name}')
            print()

        print()
        for category, cards in cards_per_category.items():
            print(f'{category} {len(cards)}')


if __name__ == '__main__':
    main()
