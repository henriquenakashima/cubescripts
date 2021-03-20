import json

from word_count import TEMP_JSON, is_actual_mtg_card


def create_cube_json(cards, output_filename=TEMP_JSON) -> str:
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
