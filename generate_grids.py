# Generate grids for grid drafting

import random
from typing import List

import cubecobra_csv

GRID_COUNT = 3


CUBECOBRA_ID = 'flying'
CUBE_NAME = 'flying_fetched'

OUTPUT_FILENAME = 'cards_in_draft.txt'


def main():
    csv_path = cubecobra_csv.request_cube_csv(CUBE_NAME, CUBECOBRA_ID)

    cube: List[cubecobra_csv.CubeCard] = cubecobra_csv.load_cube(csv_path)
    cube = random.sample(cube, 9 * GRID_COUNT)
    grids = []
    for i in range(GRID_COUNT):
        grid = []
        grids.append(grid)
        for card in cube[9*i : 9*(i+1)]:
            grid.append(card.name)

    print(f'https://cubecobra.com/cube/list/{CUBECOBRA_ID}')
    print()
    for i, grid in enumerate(grids, 1):
        print_grid(grid, i)


def print_grid(grid, i):
    new_line = '\n'

    def print_line(grid_line):
        print(f"""[ci]
{new_line.join(grid_line)}
[/ci]""")
    print(f'[spoiler="Grid {i}"]')
    print_line(grid[0:3])
    print_line(grid[3:6])
    print_line(grid[6:9])
    print(f'[/spoiler]')


if __name__ == '__main__':
    main()
