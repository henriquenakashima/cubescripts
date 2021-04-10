import pathlib

import cubecobra_csv

from cubecobra_csv import CubeCard


OUT_FILE = pathlib.Path('forge') /'MyCube.txt'

HEADER = """[metadata]
Code=CUB
Date=2021-04-09
Name=My Cube
MciCode=cub
Type=Expansion
BoosterCovers=1
Booster=10 Common, 1 Rare
Foil=NotSupported

[cards]
"""

if __name__ == '__main__':
    csv_path = cubecobra_csv.request_cube_csv('TheElegantCube_fetched', 'elegant')

    cube_cards = cubecobra_csv.load_cube(csv_path)

    with open(OUT_FILE, 'w') as outfile:
        outfile.write(HEADER)

        i = 1
        card: CubeCard
        for card in cube_cards:
            if 'core' in card.tags:
                rarity = 'C'
            elif 'occasional' in card.tags:
                rarity = 'R'
            else:
                raise Exception(f'{card.name} has no module tags')
            outfile.write('%d %s %s\n' % (i, rarity, card.name))
            i += 1
    print(f'Finished writing {OUT_FILE} with {i - 1} cards')
