import csv
import json
import requests

from word_count import EXPECTED_HEADER, COLUMNS, TEMP_JSON, is_actual_mtg_card


def request_cube_csv(cube_name, cube_id):
    url = f'https://cubecobra.com/cube/download/csv/{cube_id}'
    url += '?primary=Color%20Category&secondary=Types-Multicolor&tertiary=CMC2'
    response = requests.get(url)
    open(f'cube_csvs/{cube_name}.csv', 'wb').write(response.content)


def load_cube_from_csv(filename, tag_filter=None):
    cards = []
    with open(filename) as f:
        reader = csv.reader(f)
        header_line = next(reader)
        assert header_line == EXPECTED_HEADER
        for line in reader:
            card = line[COLUMNS['Name']]
            # Export CSV is broken on CubeCobra because Image Back URL is always just one double quotes character.
            tags = [t.strip() for t in line[COLUMNS['Tags']].split(', ')]
            if tag_filter is None or any(t in tag_filter for t in tags):
                cards.append(card)
    return cards


def create_cube_json(cards, output_filename=TEMP_JSON):
    # Call this once to create a smaller JSON file from the full card list
    # Visit https://scryfall.com/docs/api/bulk-data and look for "Oracle Cards" file;
    # Download and rename it to 'oracle_cards.json'
    with open('oracle_cards.json', encoding='utf8') as f_oracle_cards:
        d = json.load(f_oracle_cards)
    f_cube_json = open(output_filename, 'w+', encoding='utf8')
    cube_data = []
    for card in d:
        if card['name'] in cards:
            for i in range(cards.count(card['name'])):
                cube_data += [card]
        elif 'card_faces' in card.keys() and is_actual_mtg_card(card):
            for face in card['card_faces']:
                if face['name'] in cards:
                    cube_data += [card]
    string_data = json.dumps(cube_data)
    f_cube_json.write(string_data)
    f_cube_json.close()
    return output_filename