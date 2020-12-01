# Generate a draft pool for dr4ft.info

import csv
import random

import cube_json


OUTPUT_POOL_SIZE = 360
CARDS_FROM_OCCASIONAL = 48
CARDS_FROM_CORE = OUTPUT_POOL_SIZE - CARDS_FROM_OCCASIONAL
CUBE_NAME = 'TheElegantCube_fetched'

OUTPUT_FILENAME = 'cards_in_draft.txt'
EXPECTED_HEADER = [
    'Name',
    'CMC',
    'Type',
    'Color',
    'Set',
    'Collector Number',
    'Rarity',
    'Color Category',
    'Status',
    'Finish',
    'Maybeboard',
    'Image URL',
    'Image Back URL',
    'Tags',
    'Notes',
    'MTGO ID'
]
COLUMNS = {column_name: i for i, column_name in enumerate(EXPECTED_HEADER)}


def main():
    csv_path = cube_json.request_cube_csv('TheElegantCube_fetched', 'elegant')

    core_pool = []
    occasional_pool = []
    with open(csv_path) as f:
        reader = csv.reader(f)
        header_line = next(reader)
        assert header_line == EXPECTED_HEADER
        for line in reader:
            card = line[COLUMNS['Name']]
            tags = line[COLUMNS['Tags']].split(', ')
            # print(f'{card} {tags}')
            if 'occasional' in tags:
                occasional_pool.append(card)
            elif 'core' in tags:
                core_pool.append(card)
            else:
                print('{card} is tagged as neither "core" nor "occasional"')

    main_pool = random.sample(core_pool, CARDS_FROM_CORE) + random.sample(occasional_pool, CARDS_FROM_OCCASIONAL)
    with open(OUTPUT_FILENAME, 'w') as f:
        f.write('\n'.join(main_pool))


if __name__ == '__main__':
    main()
