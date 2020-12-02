# Generate a draft pool for dr4ft.info

import csv

import cube_json
import cubecobra_csv

CUBE_NAME = 'TheElegantCube_fetched'


def main():
    csv_path = cube_json.request_cube_csv('TheElegantCube_fetched', 'elegant')

    core_cards = []
    with open(csv_path) as f:
        reader = csv.reader(f)
        header_line = next(reader)
        cubecobra_csv.assert_header(header_line)
        for line in reader:
            card = line[cubecobra_csv.COLUMNS['Name']]
            tags = line[cubecobra_csv.COLUMNS['Tags']].split(', ')
            if 'core' in tags:
                core_cards.append(card)

    core_cards.sort()
    for card in core_cards:
        print(card)


if __name__ == '__main__':
    main()
