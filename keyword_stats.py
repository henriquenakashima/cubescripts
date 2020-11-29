import json

def get_keywords(card):
    if 'keywords' in card.keys():
        return card['keywords']
    elif 'card_faces' in card:
        keywords = []
        for face in card['card_faces']:
            if 'keywords' in face:
                keywords += face['keywords']
        return keywords
    else:
        return []


def keyword_count(filename):
    # json file must contain a list of Scryfall card objects
    f = open(filename, encoding='utf8')
    d = json.load(f)
    keywords = []
    for card in d:
        keywords += get_keywords(card)
    f.close()
    k_unique = set(keywords)
    k_dict = {}
    for keyword in k_unique:
        k_dict[keyword] = keywords.count(keyword)
    return k_dict


def keyword_report(k_dict):
    k_lists = []
    for keyword in k_dict:
        k_lists += [[k_dict[keyword], keyword]]
    k_lists = sorted(k_lists, reverse=True)
    for n, keyword in k_lists:
        print(keyword, n)
    print(f'\nTotal unique keywords: {len(k_dict)}')
