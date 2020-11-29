import json

from collections import defaultdict
from typing import Dict, Iterable, List, Tuple


def get_keywords(card: Dict) -> List[str]:
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


# Maps keywords to a list of cards containing them
KeywordDict = Dict[str, List[str]]


def keyword_count(filename: str) -> KeywordDict:
    # json file must contain a list of Scryfall card objects
    with open(filename, encoding='utf8') as f:
        d = json.load(f)
    k_dict = defaultdict(list)
    for card in d:
        for keyword in get_keywords(card):
            k_dict[keyword].append(card['name'])
    return k_dict


def keyword_report(k_dict: KeywordDict) -> None:
    for keyword, cards in _rank_keywords_descending(k_dict):
        print(keyword, len(cards))
    print(f'\nTotal unique keywords: {len(k_dict)}')


def keyword_report_full(k_dict: KeywordDict) -> None:
    for keyword, cards in _rank_keywords_descending(k_dict):
        print(f'{keyword} ({len(cards)})')
        for card in cards:
            print(f'  {card}')
        print()
    print(f'\nTotal unique keywords: {len(k_dict)}')


def _rank_keywords_descending(k_dict: KeywordDict) -> Iterable[Tuple[str, List[str]]]:
    return sorted(k_dict.items(), key=lambda kv: len(kv[1]), reverse=True)
