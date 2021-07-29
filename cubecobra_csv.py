
import csv
import dataclasses
from pathlib import Path
from typing import List, Set

import requests

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
    'Multicolored': 'm',
    'Hybrid': 'h',
    'Colorless': 'c',
    'Land': 'land',
}


@dataclasses.dataclass
class CubeCard:
    name: str
    color_category: str
    colors: str
    tags: Set[str]

    def __post_init__(self):
        assert self.color_category in 'wubrgchml0', f'{self}'

    def __str__(self):
        return self.name


def request_cube_csv(cube_name, cube_id) -> Path:
    url = f'https://cubecobra.com/cube/download/csv/{cube_id}'
    # url += '?primary=Color%20Category&secondary=Types-Multicolor&tertiary=CMC2'
    response = requests.get(url)
    filename = Path('cube_csvs', f'{cube_name}.csv')
    open(filename, 'wb').write(response.content)
    return filename


def load_cube_names(filename, tag_filter: Set[str]=None) -> List[str]:
    cube_cards: List[CubeCard] = load_cube(filename)
    cards = []
    for cube_card in cube_cards:
        if tag_filter is None or tag_filter.intersection(cube_card.tags):
            cards.append(cube_card.name)
    return cards


def load_cube(filename) -> List[CubeCard]:
    cards = []
    with open(filename) as f:
        reader = csv.reader(f)
        header_line = next(reader)
        _assert_header(header_line)
        for line in reader:
            card_name = _get_name(line)
            tags = _get_tags(line)
            color_category = _get_color_category(line)
            colors = _get_colors(line)
            cards.append(CubeCard(card_name, color_category, colors, tags))
    return cards


def _assert_header(header_line):
    assert header_line == EXPECTED_HEADER


def _get_name(line: List) -> str:
    return line[COLUMNS['Name']]


def _get_tags(line: List) -> Set[str]:
    return set(t.strip() for t in line[COLUMNS['Tags']].split(';'))


def _get_color_category(line: List) -> str:
    color_category = line[COLUMNS['Color Category']]
    assert color_category in _COLOR_CATEGORIES, f'color_category "{color_category}" unknown'
    return _COLOR_CATEGORIES[color_category]


def _get_colors(line: List) -> str:
    colors = line[COLUMNS['Color']]
    #assert color_category in _COLOR_CATEGORIES, f'color_category "{color_category}" unknown'
    return sorted(colors.lower())
