import json
import random

from typing import Dict, List


CardFace = Dict


def is_eligible(card: List[CardFace]):
    card_face = card[0]
    return card_face['type'] != 'Dungeon'


def main():
    with open('ModernAtomic.json', encoding='utf8') as f_oracle_cards:
        d: Dict = json.load(f_oracle_cards)
        print (d['meta'])
        all_cards: Dict = d['data']

    all_eligible_card_names: List[str] = [name for name, card in all_cards.items() if is_eligible(card)]
    random_unique_120: List[str] = random.sample(sorted(all_eligible_card_names), 120)
    with open('random_tringleton.txt', 'w+', encoding='utf8') as output:
        for card in random_unique_120:
            for _ in range(3):
                output.write(card + '\n')


if __name__ == '__main__':
    main()

