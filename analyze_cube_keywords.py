"""Print a keyword report for a cards.json file
"""

import cube_json
import keyword_stats

if __name__ == '__main__':
    cube_list = cube_json.load_cube_from_csv('cube_csvs/TheElegantCube_2020-11-17_5.0.4.csv', {'core'})
    cube_json_filename = cube_json.create_cube_json(cube_list, 'cubes/TheElegantCube_2020-11-17_5.0.4.json')
    keyword_dict = keyword_stats.keyword_count(cube_json_filename)
    keyword_stats.keyword_report(keyword_dict)
