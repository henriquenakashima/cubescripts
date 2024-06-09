"""Print a keyword report for a cards.json file
"""

import cube_json
import cubecobra_csv
import keyword_stats

if __name__ == '__main__':
    cube_id = 'jeskaicube'
    csv_path = cubecobra_csv.request_cube_csv(cube_id, cube_id)
    cube_list = cubecobra_csv.load_cube_names(f'cube_csvs/{cube_id}.csv')
    cube_json_filename = cube_json.create_cube_json(cube_list, f'cubes/{cube_id}.json')
    keyword_dict = keyword_stats.keyword_count(cube_json_filename)

    # keyword_stats.keyword_report(keyword_dict)
    keyword_stats.keyword_report_full(keyword_dict)
