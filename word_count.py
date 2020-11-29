import json

from collections import defaultdict

import cube_json


def load_cube_from_txt(filename):
    f_cube_list = open(filename)
    cards = []
    for line in f_cube_list:
        cards += [line.strip()]
    return cards


TEMP_JSON = 'cube_temp.json'
ALL_CARDS_CLEAN_JSON = 'oracle_cards_clean.json'


EXPECTED_HEADER = [
    'Name',
    'CMC',
    'Type',
    'Color',
    'Set',
    'Collector Number',
    'Rarity',
    'Color Category',
    'Status',
    'Finish',
    'Maybeboard',
    'Image URL',
    'Image Back URL',
    'Tags',
    'Notes',
    'MTGO ID'
]
COLUMNS = {column_name: i for i, column_name in enumerate(EXPECTED_HEADER)}


def is_actual_mtg_card(card_dict):
    return card_dict['set_type'] not in {'memorabilia', 'funny', 'token'}


def create_all_cards_json():
    with open('oracle_cards.json', encoding='utf8') as f_oracle_cards:
        d = json.load(f_oracle_cards)
    output_filename = ALL_CARDS_CLEAN_JSON
    f_cube_json = open(output_filename, 'w+', encoding='utf8')
    cube_data = []
    for card in d:
        if is_actual_mtg_card(card):
            cube_data += [card]
    string_data = json.dumps(cube_data)
    f_cube_json.write(string_data)
    f_cube_json.close()
    return ALL_CARDS_CLEAN_JSON


def wc_fo(text):
    # full oracle text word count
    return len(text.split())


def wc_o(text):
    # word count of oracle text without keyword explanation text
    if "(" in text and ")" in text:
        p1 = text.find("(")
        p2 = text.find(")")
        o = text[:p1] + text[p2 + 1:]
        return wc_o(o)
    else:
        return len(text.split())


def word_count(card, *, full_oracle):
    if full_oracle:
        wc = wc_fo
    else:
        wc = wc_o
    if 'card_faces' in card.keys():
        total_count = 0
        for face in card['card_faces']:
            text = face['oracle_text']
            total_count += wc(text)
        return total_count
    else:
        text = card['oracle_text']
        return wc(text)


def cube_word_count(filename, *, full_oracle):
    with open(filename, encoding='utf8') as f:
        d = json.load(f)
    wc = []
    for card in d:
        words = word_count(card, full_oracle=full_oracle)
        wc += [words]
    mean = sum(wc) / len(wc)
    if full_oracle:
        metric = 'Avg Words/Card (full text)'
    else:
        metric = 'Avg Words/Card (no reminders)'
    print(f"{metric}: {mean:.1f}")
    return mean


def duplicate_count(filename):
    with open(filename, encoding='utf8') as f:
        d = json.load(f)
    unique = []
    for card in d:
        if card['name'] not in unique:
            unique += [card['name']]
    print(f"{len(unique)} unique of {len(d)} total cards")


WHEEL = str.maketrans('WUBRG', '01234')


def wheel_order(colors):
    return colors.translate(WHEEL)


def print_by_color(filename, *, rank_cards, full_oracle):
    cards_by_color_identity = defaultdict(list)
    with open(filename, encoding='utf8') as f:
        d = json.load(f)
    for card in d:
        words = word_count(card, full_oracle=full_oracle)
        if 'Land' in card['type_line'].split('//')[0]:
            identity = 'Non-basic land'
        elif len(card['color_identity']) > 1:
            identity = 'Multicolor'
        else:
            identity = ''.join(card['color_identity'])
        cards_by_color_identity[identity].append((card['name'], words))
    # pp(cards_by_color_identity)
    # sort first by fewest colors in identity, then by WUBRG order
    for identity, card_tuples in sorted(cards_by_color_identity.items(), key=lambda t:(len(t[0]), wheel_order(t[0]))):
        total_words = sum(words for _, words in card_tuples)
        card_count = len(card_tuples)
        average_words = total_words / card_count
        identity_name = 'Non-land colorless' if not identity else identity
        print(f"{identity_name }: average {average_words:.2f} [of {card_count} cards]")
        if rank_cards:
            for card_name, card_words in sorted(card_tuples, key=lambda t: t[1], reverse=True):
                print(f'{card_name}: {card_words}')
            print()
    print()


def get_text(card):
    if 'oracle_text' in card.keys():
        return card['oracle_text']
    elif 'card_faces' in card.keys():
        text = ""
        for face in card['card_faces']:
            text += face['oracle_text'] + ' '
        return text

if __name__ == '__main__':
    ################################################################################

    full_oracle = False

    ################################################################################
    # Use either line:

    # 1. If you have a .txt of your cube
    # cube_list = cube_json.load_cube_from_txt('YourCubeHere.txt')

    # 2. If you have a .csv of your cube
    # cube_list = cube_json.load_cube_from_csv('YourCubeHere.csv')

    # 3. If you have a .csv of your cube and want to consider only cards with a certain tag
    cube_list = cube_json.load_cube_from_csv('cube_csvs/TheElegantCube_2020-11-17_5.0.4.csv', {'core'})

    ################################################################################
    # Calculate average of a cube
    cube_json_handle = cube_json.create_cube_json(cube_list)

    # Summary of average words by color
    print_by_color(cube_json_handle, rank_cards=False, full_oracle=full_oracle)

    # Individual cards by color, ranked by word count
    print_by_color(cube_json_handle, rank_cards=True, full_oracle=full_oracle)

    # Average words excluding reminder text
    cube_word_count(cube_json_handle, full_oracle=False)

    # Average words in full oracle text
    cube_word_count(cube_json_handle, full_oracle=True)

    ################################################################################
    # Calculate average of all Magic cards

    # card_db_json_handle = create_all_cards_json()
    # print_by_color(card_db_json_handle, rank_cards=True, full_oracle=full_oracle)
    # cube_word_count(card_db_json_handle, full_oracle=full_oracle)

    ################################################################################

    pass