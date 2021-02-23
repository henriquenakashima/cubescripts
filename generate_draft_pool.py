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

    main_pool = (random.sample(pools['core'], CARDS_FROM_CORE) +
                 random.sample(pools['occasional'], CARDS_FROM_OCCASIONAL))
    with open(OUTPUT_FILENAME, 'w') as f:
        f.write('\n'.join(main_pool))


if __name__ == '__main__':
    main()
