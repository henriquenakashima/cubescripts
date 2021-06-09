# Fill a cube with single copies of cards based on rarity tags.

# Paste the output file's contents in plain text to add the extra copies.
# To clean up the CubeCobra cube, filter all cards without tags and mass remove them.

from typing import List

import cubecobra_csv

from cubecobra_csv import CubeCard


CUBE_NAME = 'TotalWar_fetched'
CUBE_ID = 'total-war'

OUTPUT_FILENAME = 'cards_to_add.txt'


def get_copies_to_add(card):
    print(f'{card} {card.tags}')
    for tag in card.tags:
        if tag == 'abundant':
            return [card] * (32 - 1)
        if tag == 'mundane':
            return [card] * (16 - 1)
        if tag == 'common':
            return [card] * (4 - 1)
        if tag == 'uncommon':
            return [card] * (2 - 1)
        if tag == 'dual':
            return [card] * (7 - 1)
    return []


def main():
    csv_path = cubecobra_csv.request_cube_csv(CUBE_NAME, CUBE_ID)

    cube: List[CubeCard] = cubecobra_csv.load_cube(csv_path)
    names_to_add = []
    for card in cube:
        copies_to_add = get_copies_to_add(card)
        names_to_add.extend([card.name for card in copies_to_add])

    with open(OUTPUT_FILENAME, 'wb') as f:
        full_pool_contents = '\n'.join(names_to_add).encode('utf-8')
        f.write(full_pool_contents)
        print(f'Wrote {len(names_to_add)} cards to {OUTPUT_FILENAME}')


if __name__ == '__main__':
    main()
