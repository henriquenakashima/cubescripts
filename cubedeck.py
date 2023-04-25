# Setup:
# 1. Download cube list .txt from CubeCobra's export to .txt function
# 2. (Windows, non-WSL only) Install pyreadline3
#
# Usage:
# $ python3 cubedeck.py MyCubeList.txt
#
# Enter card: Mo [tab]
# Mogg War Marshal      Moment's Peace        Monastery Swiftspear  Mortarpod             Mountain
# Moldervine Cloak      Momentary Blink       Monoskelion           Mortify
#
# Enter card: Moldervine Cloak
#
# Enter card: Moment's Peace
#
# Enter card: Momentary Blink
#
# Enter card: :u         # Undo last card added (Momentary Blink)
#
# Enter card: :nl        # Add empty line to separate sideboard
#
# Enter card: Monoskelion
#
# Enter card: 10 Forest  # autocomplete doesn't work with number
#
# Enter card: :ls        # List deck input so far
# ['Moldervine Cloak', 'Moment's Peace', '', 'Monoskelion', '10 Forest']
#
# Enter card: :wq        # Save to file and open in default application
# Saved deck to 20230425-001458.txt
#
# Enter card: :q         # Exit without saving

from datetime import datetime

import os
import platform
import readline
import sys
import subprocess


def load_cube(cube_file):
  cube = []
  with open(cube_file) as f:
    for line in f:
      card = line.strip()
      if card:
        cube.append(card)
  return cube


BASIC_LANDS = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']
CUBE_CARDS = load_cube(sys.argv[1])
CARDS = BASIC_LANDS + CUBE_CARDS
CARDS_LOWER = {card.lower(): card for card in CARDS}


def open_file_with_default(file):
  if platform.system() == 'Darwin':       # macOS
      subprocess.call(('open', file))
  elif platform.system() == 'Windows':    # Windows
      os.startfile(file)
  else:                                   # linux variants
      if 'microsoft' in platform.uname().release.lower():
          subprocess.call(('wslview', file))   # WSL
      else:
          subprocess.call(('xdg-open', file))  # Actual linux


def enable_autocomplete():
  if readline.__doc__ is not None and 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete") # macOS
  else:
    readline.parse_and_bind("tab: complete")


def card_completer(text, state):
  text_to_complete = readline.get_line_buffer().lower()
  options = [CARDS_LOWER[i] for i in CARDS_LOWER if i.startswith(text_to_complete)]
  if state < len(options):
    return options[state][readline.get_begidx():]
  else:
    return None


def add_card(deck, card):
  count_str = None
  card_to_check = card
  if card[0].isdigit():
    parts = card.split(' ', 1)
    if len(parts) > 1 and parts[0].isdigit():
        count_str = parts[0]
        card_to_check = parts[1]
  
  card_canon = card_to_check.lower()
  if card_canon not in CARDS_LOWER:
    yn = input('"%s" not in cardlist. Are you sure you want to add it to the deck? ' % card_to_check)
    if not yn.strip().startswith('y'):
      print('Not added.')
      return
      
  add_card_with_count(deck, card_canon, count_str)


def add_card_with_count(deck, card_canon, count_str):
  card = CARDS_LOWER.get(card_canon, card_canon)
  if count_str is None:
    deck.append(card)
  else:
    deck.append('%s %s' % (count_str, card))


def add_delimiter(deck):
  deck.append('')


def remove_last_card(deck):
  if len(deck) == 0:
    print('Empty deck, cannot delete.')
    return
    
  deck.pop()


def save_deck(deck):
  file_name = datetime.today().strftime('%Y%m%d-%H%M%S') + '.txt'
  with open(file_name, 'w') as f:
    for card in deck:
      f.write(card)
      f.write('\n')
  print('Saved deck to %s' % file_name)
  open_file_with_default(file_name)


if __name__ == '__main__':
  deck = []
  enable_autocomplete()
  readline.set_completer(card_completer)
  readline.set_completer_delims('')
  
  while True:
    command = input('Enter card: ').strip()
    
    if command == '':
      continue
    if command == ':q':
      print('Exiting without saving.')
      exit(0)
    elif command == ':wq':
      save_deck(deck)
      exit(0)
    elif command == ':l':
      print(deck)
    elif command == ':nl':
      add_delimiter(deck)
    elif command == ':u':
      remove_last_card(deck)
    elif command.startswith(':'):
      print('Unrecognized command "%s"' % command)
    else:
      add_card(deck, command)

