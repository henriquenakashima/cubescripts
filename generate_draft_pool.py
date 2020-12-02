# Generate a draft pool for dr4ft.info

import csv
import random

import cube_json
import cubecobra_csv


OUTPUT_POOL_SIZE = 360
CARDS_FROM_OCCASIONAL = 48
CARDS_FROM_CORE = OUTPUT_POOL_SIZE - CARDS_FROM_OCCASIONAL
CUBE_NAME = 'TheElegantCube_fetched'

OUTPUT_FILENAME = 'cards_in_draft.txt'


def main():
    csv_path = cube_json.request_cube_csv('TheElegantCube_fetched', 'elegant')

    core_pool = []
    occasional_pool = []
    with open(csv_path) as f:
        reader = csv.reader(f)
        header_line = next(reader)
        cubecobra_csv.assert_header(header_line)
        for line in reader:
            card = line[cubecobra_csv.COLUMNS['Name']]
            tags = line[cubecobra_csv.COLUMNS['Tags']].split(', ')
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
