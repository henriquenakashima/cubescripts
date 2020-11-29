import json
import statistics

# Counts words on each card from each set using MTGJSON data.
# I downloaded "all set files" from https://mtgjson.com/downloads/all-files/

def load_set(code):
    with open(f'mtgjson/sets/{code}.json', encoding='utf8') as f:
        data = json.load(f)
        return data
    baseSetSize = data['baseSetSize']
    cards = data['cards']


def analyze_set(code):
    d = load_set(code)
    if 'data' in d:
        d = d['data']
    if 'cards' in d:
        cards = d['cards']
    else:
        print(f'No card data found in {code}.json')
        return
    faces = {}
    #list text for all cards
    for card in cards:
        if 'text' in card:
            faces[card['uuid']] = card['text']
        else:
            faces[card['uuid']] = ""
    #update text for double faced
    for card in cards:
        if 'side' in card:
            if card['side'] == 'a':
                if 'text' not in card:
                    card['text'] = ""
                elif card['otherFaceIds']:
                    card['text'] += " " + faces[card['otherFaceIds'][0]]

        # make card number an int
        if 'number' in card:
            try:
                card['number'] = int(card['number'])
            except ValueError:
                numstring = ""
                for c in card['number']:
                    if c.isdigit():
                        numstring += c
                if len(numstring) == 0:
                    card['number'] = 999999
                else:
                    card['number'] = int(numstring)
    # Generate a list of cards in the set
    set_cards = []
    for card in cards:
        if card['name'] in ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']:
            continue
        if 'side' in card and card['side'] != 'a':
            continue
        if card['number'] > d['baseSetSize']:
            continue
        set_cards += [card]
    # Create a list of word counts by rarity
    rarities = {'common': [], 'uncommon': [], 'rare': [], 'mythic': []}
    for card in set_cards:
        if 'text' not in card:
            words = 0
        else:
            words = len(card['text'].split())
        rarities[card['rarity']] += [words]
    line = [d['code']]
    for r in ['common', 'uncommon', 'rare', 'mythic']:
        if len(rarities[r]) > 0:
            mean = round(sum(rarities[r]) / len(rarities[r]), 1)
            median = statistics.median(rarities[r])
        else:
            mean = 0
            median = 0
        line += [mean, median]
        line = [str(x) for x in line]
        textline = ",".join(line)
    print(textline)
    return textline


codes = []
codes += ['LEA','3ED','4ED','5ED','6ED','7ED','8ED','9ED','10E','M10','M11','M12','M13','M14','M15','ORI','M19','M20',
         'M21']
codes += ['POR','P02','PTK','S99']
codes += ['ARN','ATQ','LEG','DRK','FEM','HML']
codes += ['ICE','ALL','MIR','VIS','WTH','TMP','STH','EXO','USG','ULG','UDS','MMQ','NEM','PCY','INV','PLS','APC',
          'ODY','TOR','JUD','ONS','LGN','SCG','MRD','DST','5DN','CHK','BOK','SOK','RAV','GPT','DIS','CSP',
          'TSP','PLC','FUT','LRW','MOR','SHM','EVE','ALA','CON_','ARB','ZEN','WWK','ROE','SOM','MBS','NPH',
          'ISD','DKA','AVR','RTR','GTC','DGM','THS','BNG','JOU','KTK','FRF','DTK','BFZ','OGW','SOI','EMN','KLD','AER',
          'AKH','HOU','XLN','RIX','DOM','GRN','RNA','WAR','ELD','THB','IKO','ZNR']
codes += ['MMA','MM2','EMA','MM3','IMA','A25','UMA','2XM']
codes += ['MH1','CMR','JMP']

output = open('retail_set_words.csv', 'w+')
output.write('Set,c (mean),c (med),u (mean),u (med),r (mean),r (med),m (mean),m (med)\n')
for code in codes:
    line = analyze_set(code)
    output.write(line + '\n')
output.close()

