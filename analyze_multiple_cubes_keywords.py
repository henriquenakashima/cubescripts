"""Count keywords in a list of cube.json files.
"""
import json
import os

import keyword_stats


if __name__ == '__main__':
    output = open('cube_keyword_frequency.csv', 'w+')
    all_cube_files = os.listdir('cubes')
    output_file = open('cube_keyword_frequency.csv', 'w+')
    output_file.write('Cube,Keywords\n')
    for filename in all_cube_files:
        if filename.endswith('json'):
            k_dict = keyword_stats.keyword_count('cubes/' + filename)
            output_file.write(f"{filename.strip('json')},{len(k_dict)}\n")
            print(filename, len(k_dict))
    output_file.close()

