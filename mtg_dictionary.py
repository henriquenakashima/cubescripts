import json

# Generates a list of every word (with frequencies) used in MTG cards.

# The 'oracle_cards.json' file is Scryfall's "Oracle Cards" file.
# "A JSON file containing one Scryfall card object for each Oracle ID on Scryfall."
# https://scryfall.com/docs/api/bulk-data
with open('oracle_cards.json', encoding='utf8') as f_oracle_cards:
    data = json.load(f_oracle_cards)


def word_list(card):
    if 'booster' not in card or card['booster'] is False:
        return []
    if 'type_line' not in card:
        return []
    if card['set_type'] in ['funny', 'vanguard', 'memorabilia']:
        return []
    if 'oracle_text' not in card:
        return []
    name = card['name']
    text = card['oracle_text']
    # remove the name; eliminates misleading occurrences of some words
    text = text.replace(name, '')
    text = text.replace("—", " ")
    remove_these = "®½π—•−∞☐"
    for char in remove_these:
        text = text.replace(char, " ")
    words = text.split()
    words = [word.strip(' ,.()[]!@#$%^&*=;:"\'?<>\n\t').lower() for word in words if word.islower()]
    return words


d = {}
for card in data:
    if 'oracle_text' in card:
        card_words = word_list(card)
        for word in card_words:
            if word not in d:
                d[word] = 1
            else:
                d[word] += 1

f_oracle_cards.close()

output = open('mtgdict.csv', "w+", encoding='utf8')
for word in d:
    output.write(f"{word},{d[word]}\n")
output.close()

