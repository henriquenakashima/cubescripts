# Generate a draft pool for dr4ft.info

import random

import cube_json
import cube_pool


OUTPUT_POOL_SIZE = 360
CARDS_FROM_OCCASIONAL = 48
CARDS_FROM_CORE = OUTPUT_POOL_SIZE - CARDS_FROM_OCCASIONAL


CUBE_NAME = 'TheElegantCube_fetched'

OUTPUT_FILENAME = 'cards_in_draft.txt'


def main():
    csv_path = cube_json.request_cube_csv('TheElegantCube_fetched', 'elegant')

    pools = cube_pool.load_pools(csv_path, {'core', 'occasional'})

    main_pool = (pools['core'].wide_sample(CARDS_FROM_CORE) +
                 pools['occasional'].wide_sample(CARDS_FROM_OCCASIONAL))
    main_pool_names = [card.name for card in main_pool]

    with open(OUTPUT_FILENAME, 'w') as f:
        f.write('\n'.join(main_pool_names))


if __name__ == '__main__':
    main()
