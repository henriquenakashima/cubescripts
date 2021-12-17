# Generate a draft pool for mtgadraft.tk or dr4ft.info

import cube_pool
import cubecobra_csv

ROUNDS = 3
SEATS = 8
PACKS = ROUNDS * SEATS
CARDS_PER_PACK = 15
OUTPUT_POOL_SIZE = PACKS * CARDS_PER_PACK
OCCASIONALS_SLOTS_PER_ROUND = [2, 1, 0]
CARDS_FROM_OCCASIONAL = sum(OCCASIONALS_SLOTS_PER_ROUND) * SEATS
CARDS_FROM_CORE = OUTPUT_POOL_SIZE - CARDS_FROM_OCCASIONAL


CUBE_NAME = 'TheElegantCube_fetched'

OUTPUT_FILENAME = 'cards_in_draft.txt'


def main():
    csv_path = cubecobra_csv.request_cube_csv('TheElegantCube_fetched', 'elegant')

    pools = cube_pool.load_pools(csv_path, {'core', 'occasional'})

    core_pool = pools['core'].wide_sample(CARDS_FROM_CORE)
    core_pool_names = [card.name for card in core_pool]
    occasional_pool = pools['occasional'].wide_sample(CARDS_FROM_OCCASIONAL)
    occasional_pool_names = [card.name for card in occasional_pool]
    boosters = []
    for r in range(ROUNDS):
        for s in range(SEATS):
            occasionals_per_booster = OCCASIONALS_SLOTS_PER_ROUND[r]
            core_per_booster = CARDS_PER_PACK - occasionals_per_booster

            booster = occasional_pool_names[-occasionals_per_booster:]
            del occasional_pool_names[-occasionals_per_booster:]
            assert len(booster) == occasionals_per_booster, str(booster)

            booster += core_pool_names[-core_per_booster:]
            del core_pool_names[-core_per_booster:]
            assert len(booster) == CARDS_PER_PACK, str(booster)

            boosters.append(booster)

    with open(OUTPUT_FILENAME, 'wb') as f:
        for booster in boosters:
            booster_contents = '\n'.join(booster).encode('utf-8')
            f.write(booster_contents)
            f.write(b'\n\n')
        print(f'Wrote {len(boosters)} boosters of {CARDS_PER_PACK} cards to {OUTPUT_FILENAME}')


if __name__ == '__main__':
    main()
