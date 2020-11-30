import os
import requests
import json
import time


# Requests card objects from each set from Scryfall.com
# Takes a few seconds and creates a ~1 MB json file per set
# Reads set codes on separate lines in set_codes.txt

def request_set(code):
    time.sleep(0.1)  # Scryfall asks for 50-100 ms delay between requests
    # Scryfall query is "set:code in:booster"
    url = f'https://api.scryfall.com/cards/search?q=set%3A{code}+in%3Dbooster'
    print(f'Requesting {code}')
    response = requests.get(url)
    d = response.json()
    cards = []
    cards += d['data']
    while d['has_more']:
        time.sleep(0.1)
        print(f'Requesting {code} next page')
        response = requests.get(d['next_page'])
        d = response.json()
        cards += d['data']
    output_cards = json.dumps(cards)
    if code == 'CON':
        code = 'CON_'
    f = open(f'scryfall/sets/{code}.json', 'w+')
    f.write(output_cards)
    f.close()


if __name__ == '__main__':
    sets = []
    with open('set_codes.csv') as set_file:
        sets = [line.strip() for line in set_file.readlines()]

    os.makedirs(os.path.join('scryfall', 'sets'), exist_ok=True)
    for code in sets:
        request_set(code)
