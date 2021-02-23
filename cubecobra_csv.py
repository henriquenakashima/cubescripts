# TODO: Make this an actual API

from typing import List, Set


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


def assert_header(header_line):
    assert header_line == EXPECTED_HEADER


_COLOR_CATEGORIES = {
    'w': 'w',
    'u': 'u',
    'b': 'b',
    'r': 'r',
    'g': 'g',
    'm': 'm',
    'h': 'h',
    'c': 'c',
    'l': 'l',
    'White': 'w',
    'Blue': 'u',
    'Black': 'b',
    'Red': 'r',
    'Green': 'g',
    'Multicolor': 'm',
    'Hybrid': 'h',
    'Colorless': 'c',
    'Land': 'land',
}


def get_name(line: List) -> str:
    return line[COLUMNS['Name']]


def get_tags(line: List) -> Set[str]:
    return set(line[COLUMNS['Tags']].split(', '))


def get_color_category(line: List) -> str:
    color_category = line[COLUMNS['Color Category']]
    assert color_category in _COLOR_CATEGORIES, f'color_category "{color_category}" unknown'
    return _COLOR_CATEGORIES[color_category]


def get_colors(line: List) -> str:
    colors = line[COLUMNS['Color']]
    #assert color_category in _COLOR_CATEGORIES, f'color_category "{color_category}" unknown'
    return sorted(colors.lower())
