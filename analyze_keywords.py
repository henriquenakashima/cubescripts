import json
import os


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


# ### Example use: print a keyword report for a cards.json file ###
# filename = f'cubes/CoreTheElegantCube.json'
# k_dict = keyword_count(filename)
# keyword_report(k_dict)


# ### Example use: count keywords in a list of cube.json files ###
# output = open('cube_keyword_frequency.csv', 'w+')
# all_cube_files = os.listdir('cubes')
# output_file = open('cube_keyword_frequency.csv', 'w+')
# output_file.write('Cube,Keywords\n')
# for filename in all_cube_files:
#     if filename.endswith('json'):
#         k_dict = keyword_count('cubes/' + filename)
#         output_file.write(f"{filename.strip('json')},{len(k_dict)}\n")
#         print(filename, len(k_dict))
# output_file.close()


# ### Example use: find keyword count in each set ###
# f = open('set_codes.txt')
# codes = [line.strip() for line in f.readlines()]
# output_file = open('set_keyword_frequency.csv', 'w+')
# output_file.write('Set,Keywords\n')
# for code in codes:
#     if code == 'CON':
#         code = 'CON_'
#     filename = f'scryfall/sets/{code}.json'
#     k_dict = keyword_count(filename)
#     print(f'{code}: {len(k_dict)}')
#     output_file.write(f'{code},{len(k_dict)}\n')
# output_file.close()
# f.close()
