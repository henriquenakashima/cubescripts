"""Find keyword count in each set.
"""

import keyword_stats

if __name__ == '__main__':
    f = open('set_codes.txt')
    codes = [line.strip() for line in f.readlines()]
    output_file = open('set_keyword_frequency.csv', 'w+')
    output_file.write('Set,Keywords\n')
    for code in codes:
        if code == 'CON':
            code = 'CON_'
        filename = f'scryfall/sets/{code}.json'
        k_dict = keyword_stats.keyword_count(filename)
        print(f'{code}: {len(k_dict)}')
        output_file.write(f'{code},{len(k_dict)}\n')
    output_file.close()
    f.close()
