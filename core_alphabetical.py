# Generate a draft pool for dr4ft.info

import csv

import cubecobra_csv

CUBE_NAME = 'TheElegantCube_fetched'


def main():
    csv_path = cubecobra_csv.request_cube_csv('TheElegantCube_fetched', 'elegant')
    core_cards = cubecobra_csv.load_cube_names(csv_path, {'core'})
    core_cards.sort()
    for card in core_cards:
        print(card)


if __name__ == '__main__':
    main()
