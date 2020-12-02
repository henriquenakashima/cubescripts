# TODO: Make this an actual API

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
