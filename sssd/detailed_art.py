"""Roomier hand-drawn scenes and recognizable equipment-dock objects.

The village's bell tower, 888-canopy trees, clustered rooftops, and branching
streets adapt Rai's original ``villagemap`` in SSSDpak/maps.py. Other scenes
extend the expanded world's existing landmarks. Braced names are semantic
menu hotspots, rendered by the UI as numbered keys such as [1].
"""

import re


LOCATION_ART = {
    "village": r'''
          888888                         /\                      888888
       88888888888                      /==\                  8888888888
     888888888888888                   /====\                888888888888
    88888888888888888                 /______\                 | || |
          |  || |                    /|  /\  |\                | || |
          | ||  |                     | /__\ |                 || | |
          ||  | |                     |  ()  |                 | | ||
         / |  |  \                   /|______|\               /  |  \
    .                           ____/==========\____                 .
                  ( )          /________||__________\       ) )
                   (           |   /\   ||   /\    |       ( (
      _______    __||__        |  |::|  ||  |::|   |     ___|_|___
     /=======\  /======\       |  |__| ____ |__|   |    /=========\
    /_________\/________\      |      | .. |       |   /___________\
   /|  SHOP  |\|  INN  |\     |______|____|_______|  /| []  FORGE |\
    | []  [] | | [] [] |           /      \           |  _  __   |
    |   __   | |   __  |    . . . /        \ . . .    | (_) |[]| |
____|__|__|__|_|__|__|_|___      /          \      ___|_____|__|_|____
    {shop} Shop   {rest} Inn       /    .--.    \        {smith} Smith
          o   o        .----.  |   ( ~  )   |       ____
         /|\ /|\       | !! |  |    '--'    |      /====\
    {locals} Locals      {quests} Jobs |            |     /______\
______________________ __||___/              \________________________
        .     .     .          {travel} Road out          .     .
'''.strip("\n"),
    "farm": r'''
             .--.                  \   |   /                  .--.
          .-(    ).                  .---.                  .-(    ).
         (________)              -- ( SUN ) --             (________)
                                    '---'
            /\                     /   |   \       ______
           /==\                                   /      \
          /====\      ____                       /  WIND  \
     ____/______\____|____|                      /____||____\
    /=====================\                          ||
   /_______________________\                 |-------||-------|
  /|  HAYLOFT   |  LOFT    |\                |       ||       |
   |   ____     |    ____  |                         ||
   |  |####|    |   |####| |     o                   ||
   |__|####|____|___|####|_|    /|\          ________||________
   |  BED  |    |   ____  |    / \          v  v  v  v  v  v
   |  []   |    |  | /\ | |   {farmer} Farmer   |  |  |  |  |  |
___|_______|____|__|/__\|_|___               v  v  v  v  v  v
    {rest} Barn bed      :        . . . .     |  |  |  |  |  |
                       :       .           {harvest} Harvest the rows
   _______________     :      .       o       v  v  v  v  v  v
  /___/___/___/___/|    :     .      _|_      |  |  |  |  |  |
  | hay hay hay |/   . : . . .     /_|_\
__|_____________|____________________________________________________
                        {travel} Follow the farm road
'''.strip("\n"),
    "desert": r'''
             \  |  /
              .---.                          ___
         ----( SUN )----              ____.-'   '-.___
              '---'              ____/               '---.__
             /  |  \        ____/                         '---.__
___________________________/_________________________________________
              ~                  ~                  ~
          ____             _____        ______
    ____.'    '----._____.-'     '------'      '---.______
_.-'                                                    '----.____
                          {explore} Search the dune trail
          __                          .       .
         /  \            __            .       .
  __     |  |           /  \            .       .
 /  \    |  |           |  |             .       .
 |  |    |  |           |  |              .       .
 |  |____|  |___________|  |                .        /\
 \_______    _____________/                 .       /  \____
         |  |                                .    /  /     \
         |  |            ~                    .  /__/_______\
         |  |                                    | /  \    |
      ___|__|___                                  |/____\___|
___.-'          '-.___              (  )       {rest} Sheltered camp
                     '---.__________)(__ ___________________________
       {travel} Road out
'''.strip("\n"),
    "caves": r'''
         /\      /\                 /\                 /\
     ___/  \____/  \_____      ____/  \_____      ____/  \____
 ___/    /\       /\    \____/     /\     \____/     /\     \___
/        ||       \/              ||                \/         \
|    /\  \/                 /\    \/      /\                    |
|    \/                    /  \           \/       /\           |
|            .       *     \  /                   \/           |
|   /\       :              \/              .--------------.   |
|  /||\      :    {explore} Follow crystal tracks |  ___    ___  |   |
|  \||/      :                              | ( O )  ( O ) |   |
|   \/       : . . . . . . . . . . .        |  ---    ---  |   |
|      *                           .        |    .----.    |   |
|     /\       ___                  .       |   /______\   |   |
|    /||\     /   \                  .      |__COLOSSUS____|   |
|    \||/    / /\  \                  .       / |    | \       |
|     \/    / /__\  \                  .  ___/  |____|  \___   |
|__________/_________\                    {challenge} Guardian's lair |
|              :                              .                |
|         /\   :            (   )              .                |
|        /  \  :             ) (               .                |
|_______/____\_:_____________ _)(_ _____________________________|
        {rest} Sheltered camp             {travel} Return to daylight
'''.strip("\n"),
    "forest": r'''
       888888888              88888888888              8888888888
    888888888888888        888888888888888888        88888888888888888
  88888888888888888888    888888888888888888888    888888888888888888888
 8888888888888888888888  88888888888888888888888  88888888888888888888888
       |  ||  |                | || |              |   ___   |
       || ||  |                || | |              |  ( O )  |
       | |||  |                | || |              |   ---   |
       |  ||  |    ____        || | |              |  _____  |
       || |   |   /____\       | || |              | /     \ |
       |  ||  |   | () |       || | |              ||   _   ||
       | |||  |   |____|       | || |              ||  / \  ||
      /   |    \    ||        /  |   \             || |   | ||
_____/____|_____\___||_______/____|____\____________||_|___|_||____
       .           :                                 {challenge} Root gate
        .          :      {explore} Follow the lantern trail  / | \
         . . . . . : . . . . . . . . . . . . . . .     /  |  \
                  .              /\             .     /   |   \
        _        .              /  \             .   / /  |  \ \
       /_\      .              /____\             ._/ /___|___\ \_
       | |     .       (   )  /      \             .
_______|_|____._________ ) ( _/________\_____________________________
              {travel} Woodland road       {rest} Camp beneath the boughs
'''.strip("\n"),
    "sea": r'''
          .--.                     .--.                  _||_
       .-(    ).                .-(    ).              __|__|__
      (________)               (________)            /========\
                                        |\           |  ____  |
                         |              | \          | ( () ) |
                         |\             |  \         |  '--'  |
                       __|_\____________|___\        |___||___|
                       \                    /        |   ||   |
         ~      ~       \__________________/    ~    | []  [] |
    ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  |        |
  ~        ~         ~         ~          ~         _|________|_
 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~     {challenge} Drowned bell
        ______         ______             ______         .
_______/      \_______/      \___________/      \________._________
     .       .       .       .       .       .       .   .
      {explore} Walk the tide line    . . . . . . . . . . .  .
       .                          .                     .
        .       ____             .       /\             .
         .     / __ \           .       /  \            .
          .    \____/          .       /____\    (   )
           .                  .       /      \    ) (
____________.________________._______/________\___ _)(_ ______________
           {travel} Coastal road                 {rest} Beach camp
'''.strip("\n"),
    "bridge": r'''
          /\                  LAST HONEST BRIDGE                 /\
         /==\                                                  /==\
        /____\             |   |   |   |   |   |              /____\
        | [] |_____________|___|___|___|___|___|______________| [] |
        |    |=============|===|===|===|===|===|==============|    |
        | [] |                                               | [] |
    . . |    |      {explore} Patrol the ancient crossing          |    | . .
   .    |____|_______________________________________________|____|    .
  .       \          /\          /\          /\          /            .
 .         \________/  \________/  \________/  \________/              .
.            |    |      |    |      |    |      |    |                 .
     ~ ~ ~ ~~|    |~~~~~~|    |~~~~~~|    |~~~~~~|    |~ ~ ~ ~
   ~       ~ |    |      |    |      |    |      |    |      ~
      ~ ~ ~ _|____|_ ~ ~_|____|_ ~ ~_|____|_ ~ ~_|____|_ ~ ~
  ~  ~ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~
     ~     ~          ~           ~            ~       ~
 __________________________________________________________________
/         .                                           /\           \
|          .                                         /  \          |
|   {travel} River road              (   )             /____\         |
|                                  ) (             /      \        |
|__________________________________ _)(_ _________/________\_______|
                                               {rest} Riverside camp
'''.strip("\n"),
    "plains": r'''
          .--.                     .--.                    .--.
       .-(    ).                .-(    ).               .-(    ).
      (________)               (________)              (________)
                          ___                  ___
            ___          /   \                /   \            ___
       ____/   \________/     \______________/     \__________/   \__
______/
           _                ___                    _
          |_|              /___\                  |_|
           |               |   |                   |
          /|\              | * |                  /|\
_____._____|________.______|___|_____._____________|______.__________
     .                                .                           .
     {explore} Follow the old lantern road . . . . . . . . . . . . . .
      .                            .                          \|/
       .      \|/                 .           \|/              |
        .      |                 .             |              / \
         .                      .                    /\
          .                    .                    /  \
           .      ______      .                    /____\     (   )
            .    /______\    .                    /      \     ) (
_____________.___|______|___.____________________/________\___ _)(_ __
      {travel} Road to the village                    {rest} Camp in the grass
'''.strip("\n"),
    "mountains": r'''
                              /\                       /\
                /\           /  \           /\        /  \
               /  \         / /\ \         /  \      / /\ \
      /\      / /\ \       / /  \ \       / /\ \____/ /  \ \____
     /  \____/ /  \ \_____/ /    \ \_____/ /  \            /\    \
    / /\                 /        \           /\          /  \    \
   / /  \      /\       /          \         /  \        / /\ \    \
  / /    \    /  \     /            \_______/    \______/ /  \ \____\
 /        \__/ /\ \___/                  \                  ___
/             /  \           {challenge} The drake's nest      _/   \_
                     _____                . . . . .    /  o o  \
        {explore} Climb  /     \___            .            \_ ^ _/
       . . . . . /         \_____         .       /\    /| V |\
      .          /               \        .   ___/  \__/ |___| \__
     .          /                 \        . /                    \
    .          /                   \        .
   .    ____                            /\   .
  .    /____\                          /  \   .
 .     | () |                         /____\   .         (   )
.      |____|                        /      \   .         ) (
_________||_________________________/________\___________ _)(_ _____
    {travel} Down the mountain                 {rest} Sheltered high camp
'''.strip("\n"),
    "castle": r'''
         |>>>                  /\                       <<<|
       __|___                 /==\                    ____|__
      |_|_|_|                /____\                   |_|_|_|
      | []  |                | () |                   |  [] |
      |     |________________|____|___________________|     |
      | []  | |_| |_| |_| |_|_|__|_|_| |_| |_| |_| |_ |  [] |
      |     |                                         |     |
      |  [] |             THE HOLLOW CROWN            | []  |
      |     |               .-----------.             |     |
      | []  |               |  /\   /\  |             |  [] |
      |     | {explore} Courts   | |  | |  | | {challenge} Throne |     |
      |_____|_______________|_|__|_|__|_|_____________|_____|
             \               /         \              /
              \_____________/           \____________/
             .               |         |              .
            .                |   ___   |               .
           .                 |  /   \  |                .
          .                  | /     \ |                 .
         .        /\         |/       \|                  .
        .        /  \        /         \        (   )      .
       .        /____\      /           \        ) (        .
_______._______/______\____/_____________\_______ _)(_ _______.______
     {travel} Castle road          {rest} Camp outside the walls
'''.strip("\n"),
}


EQUIPMENT_ART = {
    "inventory": r'''
       .--------.
    .-'__________'-.
   /  /          \  \
  |  |  .------.  |  |
  |  |__| [==] |__|  |
  | /  /'------'\  \ |
  ||  |   ____   |  ||
  ||__|__| [] |__|__||
  |______|____|______|
   '----------------'
'''.strip("\n"),
    "character": r'''
        .------.
        |  XX  |
        '---+--'
   .--------|--------.
   |  |  .--+--.  |  |
   '--'  | XXX |  '--'
         '-----'
     _      |      _
    [#]====[|]====[#]
        ___/ \___
'''.strip("\n"),
    "journal": r'''
  _________ _________
 /        /\        \
/  ---   /  \  ---   \
| ----- | || | ----- |
| ---   | || |   --- |
| ----- | || | ----- |
|_______|_||_|_______|
 \______\ || /______/
          ||
          \/
'''.strip("\n"),
}


SCREEN_ART = {
    "shop": r'''
    .------------------ LITTLE JIMMY'S EMPORIUM ------------------.
    |                                                            |
    |   ___   ___   ___              /\    /\    /\               |
    |  /___\ /___\ /___\             ||    ||    ||     ______    |
    |  | + | | + | | x |            =||=  =||=  =||=   /______\   |
    |  \___/ \___/ \___/             ||    ||    ||    |______|   |
    |============================================================|
    |    _      _      _                ________                 |
    |   / \    / \    / \              /_______/\      ____      |
    |   \_/    \_/    \_/             |  [] [] | |    /____\     |
    |=================================|________|/=====|____|=====|
    |                                                            |
    |   {buy} Browse the shelves                 {sell} Sell your surplus   |
    |       .----------------.           .----------------.      |
    |       |  ___     ___   |           |   YOUR ITEMS   /|      |
    |       | |___|   |___|  |           |______________/ |      |
    |_______|________________|___________|______________|/_______|
            | |          | |             | |      | |
           _|_|_        _|_|_           _|_|_    _|_|_
'''.strip("\n"),
    "workshop": r'''
           )   )          THE SMITH'S WORKSHOP             /\
          (   (                                          /  \
        ___|_|___      .---------------------------.      |  |
       /=========\     |  /\   /\   /\    _    _   |     =|  |=
      /___________\    |  ||   ||   ||   | |  | |  |      |  |
      |  .-----.  |    | =||= =||= =||=  |_|  |_|  |      |  |
      |  | ( ) |  |    |  ||   ||   ||    |    |   |      |__|
      |  | ) ( |  |    '---------------------------'       ||
      |__|_)(_|__|                         ________________||___
      |__________|          _______       /                    /|
       | |    | |      ____/       \___  /____________________/ |
       |_|    |_|     /                 \|    ___  ___  ___   | |
                      \____       ______/|___|___||___||___|__|/
                           |     |       | |                | |
              {craft} Craft  |_____|       |_|                |_|
                       ___/       \___          {upgrade} Upgrade equipment
    ___     ___       /_______________\             _______
   /___\   /___\          |       |                /  _    \
   |ore|   |ore|       ___/         \___           |  (_)   |
___|___|___|___|____ __/_______________\__ _________\_______/______
'''.strip("\n"),
    "locals": r'''
   .---------------------- LITTLE JIMMY'S INN ----------------------.
   |  .----------.                           .-----------------.  |
   |  |  /\  /\  |        _____              |   TODAY'S NEWS  |  |
   |  | /  \/  \ |       /_____\             |   --  --  --    |  |
   |  '----------'       |     |             '-----------------'  |
   |                     |  o  |                                  |
   |     ______          |_____|             ___                  |
   |   _/______\_          ,.,.             _|_|_                 |
   |     (o  o)           (o  o)            (o  o)                |
   |     /|  |\           /|  |\            /|  |\                |
   |    / |__| \         / |__| \          / |__| \               |
   |     {kieth} Kieth          {jimmy} Jimmy            {smith} Smith             |
   |______________________________________________________________|
   |  ___      ___       ___       ___       ___       ___         |
   | |___|    |___|     |___|     |___|     |___|     |___|        |
   |______________________________________________________________|
       ||       ||        ||        ||        ||        ||
      /__\     /__\      /__\      /__\      /__\      /__\
'''.strip("\n"),
    "ending": r'''
                 THE BROKEN CROWN. THE CHOICE IS YOURS.
                  .                               *
            .     |     .                     .   |   .
            |\___/|\___/|                   *   \ | /   *
            |     *     |                    --- (*) ---
            |  *     *  |                   *   / | \   *
            |___________|                     '   |   '
             \_________/                          *
                 ||                         .-----------.
          _______||_______                 /   .-----.   \
         /                \               |   /       \   |
        /   /\        /\   \              |  |         |  |
       /___/  \______/  \___\              \  \       /  /
       |                    |               \  '-----'  /
       |  MANY HANDS CAN    |                '---------'
       |  HOLD THE WARDS    |                 ROOM TO GROW
       |____________________|
      {restore} Restore the wards              {release} Release the binding
    ___________________________          ___________________________
'''.strip("\n"),
    "title": r'''
       _____   _____   _____   ____                    |>>>
      / ____| / ____| / ____| |  _ \                ___|___
     | (___  | (___  | (___   | | | |               |_|_|_|
      \___ \  \___ \  \___ \  | | | |      /\       |  [] |
      ____) | ____) | ____) | | |_| |     /==\      |     |
     |_____/ |_____/ |_____/  |____/     /____\     | []  |
                                       | () |_____|     |_____
          THE WARDS OF ASSONANCE        |____| |_| |  [] | |_| |
                                       |    |     |     |     |
          .------------.               | [] |  ___|_____|___  |
         /   A ROAD     /|              |    | /             \ |
        /  HOME AGAIN / |              |____|/               \|
       /_____________/  |                   /    _______      \
       |             | /                   /    /       \      \
       |_____________|/                   /____/         \______\
           {new} New adventure                 {continue} Continue your story
            ________                          ________
      _____/        \________________________/        \____________
'''.strip("\n"),
}


# Extra landmarks preserve three early panoramas without stretching glyphs.
# The extra foreground gives wide terminals an actual panorama, not bigger text.
_WIDE_BACKDROPS = {
    "village": r'''
               |>>>
           ____|____
           |_|_|_|_|
           |  []   |
           |       |
           |   []  |
           |_______|
          /=========\
         /___________\
         |  []   []  |
         |     __    |
         |____|__|___|
             /  \
   ______   /    \    ______
  /======\ /      \  /======\
 /________\        /________\
 | []  [] |        | []  [] |
 |   __   |        |   __   |
_|__|__|__|________|__|__|__|_
        .      .      .
    _________       _______
   /=========\     /=======\
  /___________\   /_________\
  | []  [] [] |   |  [] [] |
__|___|__|____|___|___|__|_|__
'''.strip("\n"),
    "forest": r'''
       8888888888888
    8888888888888888888
  88888888888888888888888
 8888888888888888888888888
888888888888888888888888888
 8888888888888888888888888
    8888888888888888888
        |   ||   |
        ||  ||   |
        |  || |  |
        || |  || |
        |  |  |  |
        |  |  |  |     ___
        |  || |  |    /___\
        |  |  || |    | * |
        |  |  |  |    |___|
       /   |  |   \     ||
      / /  |  |  \ \    ||
     / /   |  |   \ \   ||
    / /    |  |    \ \  ||
___/ /____/    \____\ \_||___
  /_/    / /\ \     \_\
       _/ /  \ \_
      /__/    \__\
   . . . . . . . . . . . .
'''.strip("\n"),
    "farm": r'''
           \       /
            \     /
             \   /
          ____\_/____
         |____(O)____|
             / | \
            /  |  \
           /   |   \
          /    |    \
              /\
             /==\
            /====\
           /======\
          /________\
          |  ____  |
          | | () | |
          | |____| |
          |   __   |
          |__|__|__|
   v v v v          v v v v
   | | | |          | | | |
   v v v v          v v v v
   | | | |          | | | |
  __________________________
 /____/____/____/____/____/ /
'''.strip("\n"),
}


def _panorama(left: str, right: str) -> str:
    """Join drawn landmarks at a stable column despite variable token lengths."""
    left_lines, right_lines = left.splitlines(), right.splitlines()
    height = max(len(left_lines), len(right_lines))
    left_lines += [""] * (height - len(left_lines))
    right_lines += [""] * (height - len(right_lines))
    output = []
    for first, second in zip(left_lines, right_lines):
        visible = len(re.sub(r"\{[a-z_]+\}", "[ ]", first))
        output.append(first + " " * max(3, 80 - visible) + second)
    output += [
        "_" * 111,
        "      .           .          .            .          .           .          .           .          .",
        "           .           .          .            .          .           .          .           .",
    ]
    return "\n".join(line.rstrip() for line in output)


WIDE_LOCATION_ART = {
    name: _panorama(LOCATION_ART[name], backdrop)
    for name, backdrop in _WIDE_BACKDROPS.items()
}


def _visible_width(line: str) -> int:
    return len(re.sub(r"\{[a-z_]+\}", "[ ]", line))


def _straight_walls(drawing: str, indent: int, inside: int,
                    title: str | None = None) -> str:
    """Keep enclosing walls straight after replacing differently sized tokens."""
    lines = drawing.splitlines()
    prefix = " " * indent + "|"
    for index, line in enumerate(lines):
        if line.startswith(prefix) and line.endswith("|"):
            body = line[len(prefix):-1].rstrip()
            fill = "_" if body and set(body) <= {"_", "|"} else "=" if body and set(body) <= {"=", "|"} else " "
            padding = inside - _visible_width(body)
            if padding < 0:
                raise ValueError("A drawing extends past its enclosing wall.")
            lines[index] = prefix + body + fill * padding + "|"
    if title is not None:
        lines[0] = " " * indent + "." + (" " + title + " ").center(inside, "-") + "."
    return "\n".join(lines)


SCREEN_ART["shop"] = _straight_walls(
    SCREEN_ART["shop"], 4, 66, "LITTLE JIMMY'S EMPORIUM")
SCREEN_ART["locals"] = _straight_walls(
    SCREEN_ART["locals"], 3, 68, "LITTLE JIMMY'S INN")
LOCATION_ART["caves"] = _straight_walls(LOCATION_ART["caves"], 0, 63)


def _training_yard() -> str:
    shield = r'''
    .------------.
   /              \
  /    .------.    \
 |    /   ++   \    |
 |   |   ++++   |   |
 |    \   ++   /    |
  \    '------'    /
   \              /
    '-----..-----'
          ||
'''.strip("\n")
    boots = r'''
         ___
        /   \_
       /    __|
      /    /
     /    /      .
    /____/     .
     \__|    .
           .
        .
     . . . . . .
'''.strip("\n")
    columns = [EQUIPMENT_ART["character"].splitlines(),
               shield.splitlines(), boots.splitlines()]
    labels = ["{strength} Strength", "{vitality} Vitality", "{agility} Agility"]
    for column, label in zip(columns, labels):
        column.extend(["", label])
    border = "+" + "-" * 22 + "+"
    rows = ["              THE TRAINING YARD: GROW INTO YOUR LEGEND",
            "  ".join([border] * 3)]
    for index in range(12):
        cells = []
        for column in columns:
            line = column[index]
            padding = 22 - _visible_width(line)
            if padding < 0:
                raise ValueError("Training equipment exceeds its display column.")
            cells.append("|" + line + " " * padding + "|")
        rows.append("  ".join(cells))
    rows.append("  ".join([border] * 3))
    return "\n".join(rows)


SCREEN_ART["character"] = _training_yard()


class _Canvas:
    """Place complete drawings in one scene; semantic keys occupy three cells."""

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.rows = [[" "] * width for _ in range(height)]
        self.tokens = {}

    def put(self, x, y, drawing, *, clear=False):
        def key(match):
            token = match[0]
            if token not in self.tokens:
                self.tokens[token] = "~" + chr(65 + len(self.tokens)) + "~"
            return self.tokens[token]

        lines = [re.sub(r"\{[a-z_]+\}", key, line)
                 for line in drawing.strip("\n").splitlines()]
        if clear and x > 0 and len(lines) == 1 and re.search(r"~[A-Z]~", lines[0]):
            # Give a hotspot breathing room when it sits on a floorboard.
            lines[0] = " " + lines[0] + " "
            x -= 1
        block_width = max(map(len, lines), default=0)
        if x < 0 or y < 0 or x + block_width > self.width or y + len(lines) > self.height:
            raise ValueError(f"Drawing at {x},{y} extends outside {self.width}x{self.height}.")
        if clear:
            for row in range(y, y + len(lines)):
                self.rows[row][x:x + block_width] = [" "] * block_width
        for dy, line in enumerate(lines):
            for dx, char in enumerate(line):
                if char != " ":
                    self.rows[y + dy][x + dx] = char

    def text(self):
        result = "\n".join("".join(row).rstrip() for row in self.rows).rstrip("\n")
        for token, marker in self.tokens.items():
            result = result.replace(marker, token)
        return result


def _room(title, *, width=116, height=33):
    room = _Canvas(width, height)
    room.put(0, 0, "." + (" " + title + " ").center(width - 2, "-") + ".")
    for y in range(1, height - 1):
        room.put(0, y, "|")
        room.put(width - 1, y, "|")
    room.put(1, 3, "=" * (width - 2))
    # Uprights and floorboards belong to a single room, behind the furniture.
    for x in range(12, width - 4, 12):
        room.put(x, 1, "||\n||")
        for y in range(4, height - 8):
            room.put(x, y, "|")
    room.put(1, height - 8, "_" * (width - 2))
    for y in range(height - 6, height - 1, 2):
        room.put(1, y, "_" * (width - 2))
        offset = 5 if y % 4 else 12
        for x in range(offset, width - 2, 19):
            room.put(x, y - 1, "|")
    room.put(0, height - 1, "'" + "-" * (width - 2) + "'")
    return room


_CABINET = r'''
 .----------------------------.
 |       APOTHECARY            |
 |----------------------------|
 |   __      __      __       |
 |  _||_    _||_    _||_       |
 | / +  \  / +  \  / x  \      |
 | \____/  \____/  \____/      |
 |============================|
 |   _       _       _        |
 |  / \     / \     / \        |
 | ( @ )   ( @ )   ( @ )       |
 |  \_/     \_/     \_/        |
 |============================|
 |      HERBS AND TONICS       |
 '----------------------------'
'''.strip("\n")

_WEAPON_RACK = r'''
 .--------------------------.
 |   FOR THE ROAD AHEAD      |
 |--------------------------|
 |   /\      /\       /\    |
 |   ||      ||       ||    |
 |   ||      ||       ||    |
 |  =||=    =||=     =||=   |
 |   ||      ||       ||    |
 |==========================|
 |   .------.    .------.   |
 |  /        \  /        \  |
 | |    +     ||    *     | |
 |  \        /  \        /  |
 |   '------'    '------'   |
 '--------------------------'
'''.strip("\n")

_MERCHANT = r'''
       .--------.
      / . . . .  \
     /____________\
       / o    o \
      |    __    |
       \  \__/  /
        '------'
     ___/|    |\___
    /    |____|    \
   / /|  JIMMY  |\ \
  /_/ |        | \_\
 (__) |________| (__)
      |   ||   |
      |___||___|
       /_/  \_\
'''.strip("\n")

_CHEST = r'''
      .---------------------.
     /  ================== /|
    /_____________________/ |
   |          ___         | |
   |         |[=]|        | |
   |_________|___|________|/
'''.strip("\n")

_FORGE = r'''
        )     )
       (     (
      __|___|__
     /=========\
    /===========\
   /_____________\
   | .---------. |
   | |  (   )  | |
   | |   ) (   | |
   | |  (   )  | |
   | |   \ /   | |
   | |  ( V )  | |
   |_|___) (___|_|
   |_____________|
    | |       | |
    |_|       |_|
'''.strip("\n")

_ANVIL = r'''
          __________
      ___/          \________
     /                       \
    /_________________________\
        \       ________/
         |     |
         |_____|
      ___/     \___
     /_____________\
      |  |     |  |
      |__|     |__|
'''.strip("\n")

_SMITH = r'''
        ___
       _|_|_        _____
       (o o)       |_____|
       /===\         ||
      /|||||\        ||
    __\|||||/__     _||
   /   \___/   \   (___)
  / /|  ___  |\ \__/ /
 /_/ | |___| | \____/
(__) |_______|
     |   |   |
     |___|___|
      /_/ \_\
'''.strip("\n")

_GRINDSTONE = r'''
       .-----------.
     .'     |       '.
    /    \  |  /      \
   |------ (O) -------|
    \    /  |  \      /
     '.     |       .'
       '-----------'
           |   |
        ___|___|___
       /___________\
'''.strip("\n")

_WINDOW = r'''
 .---------------------.
 |  /\       |     /\  |
 | /  \      |    /  \ |
 |/____\_____|___/____\|
 |-----------+---------|
 |   8888    |   8888  |
 |    ||     |    ||   |
 '---------------------'
'''.strip("\n")


_CABINET = _straight_walls(_CABINET, 1, 28)
_WEAPON_RACK = _straight_walls(_WEAPON_RACK, 1, 26)


def _shop_interior():
    canvas = _room("LITTLE JIMMY'S EMPORIUM - GOODS, GEAR & GOSSIP")
    canvas.put(4, 5, _CABINET, clear=True)
    canvas.put(40, 5, _WEAPON_RACK, clear=True)
    canvas.put(83, 6, _MERCHANT, clear=True)
    canvas.put(9, 21, "{buy} Browse the shelves", clear=True)
    canvas.put(4, 23, r'''
  ___________           .----.
 /  HERBS   /|          |    |        /\
/__________/ |          |____|       /  \
|  @ @ @ @ | /           ||        /____\
|__________|/           _||_       (______)
''', clear=True)
    canvas.put(65, 24, _CHEST, clear=True)
    canvas.put(68, 22, "{sell} Sell at Jimmy's counter", clear=True)
    return canvas.text()


def _workshop_interior():
    canvas = _room("THE SMITH'S WORKSHOP - ASH, IRON & AMBITION")
    canvas.put(3, 5, _FORGE, clear=True)
    canvas.put(26, 5, r'''
 .-------------------------------.
 |  /\   /\   /\     __   __      |
 |  ||   ||   ||    |__| |__|     |
 | =||= =||= =||=    ||   ||      |
 |  ||   ||   ||     ||   ||      |
 '-------------------------------'
''', clear=True)
    canvas.put(72, 5, r'''
 .----------------------------------.
 |    THE SMITH KEEPS NO SHORTCUTS    |
 |    Measure twice. Hit it harder.  |
 '----------------------------------'
''', clear=True)
    canvas.put(33, 13, _ANVIL, clear=True)
    canvas.put(67, 10, _SMITH, clear=True)
    canvas.put(88, 18, _GRINDSTONE, clear=True)
    canvas.put(31, 25, "{craft} Craft at the anvil", clear=True)
    canvas.put(82, 29, "{upgrade} Improve your equipment", clear=True)
    canvas.put(5, 25, r'''
   ___       ___
  /___\     /___\
  |ORE|     |ORE|
  |___|     |___|
''', clear=True)
    return canvas.text()


def _locals_interior():
    canvas = _room("LITTLE JIMMY'S INN - THE USUAL TABLE")
    canvas.put(4, 5, _WINDOW, clear=True)
    canvas.put(87, 5, r'''
  .--------------------.
  |  A HOT MEAL        |
  |  A SAFE BED        |
  |  UNRELIABLE NEWS   |
  '--------------------'
''', clear=True)
    canvas.put(31, 5, r'''
         _______
       _/_______\_
        / o   o \
       |    >    |
        \ .---. /
         '-----'
      ___/|   |\___
     /    |___|    \
    / /|  /   \  |\ \
   /_/ | /     \ | \_\
  (__) |_________| (__)
''', clear=True)
    canvas.put(58, 5, _MERCHANT, clear=True)
    canvas.put(86, 11, r'''
        ___
       _|_|_
       (o o)
       /===\
      /|||||\
    __\|||||/__
   /   \___/   \
  / /|  ___  |\ \
 /_/ | |___| | \_\
(__) |_______| (__)
''', clear=True)
    canvas.put(30, 18, "{kieth} Kieth", clear=True)
    canvas.put(61, 21, "{jimmy} Jimmy", clear=True)
    canvas.put(87, 22, "{smith} Smith", clear=True)
    canvas.put(5, 15, r'''
    .----------.
    | ( )  ( ) |
    |  )    (  |
    | (  /\  ) |
    |__)_)(_( _|
    |__________|
''', clear=True)
    canvas.put(27, 24, r'''
 .------------------------------------------------------------------------------.
 |   ___         ______        ___          ________        ___           ___   |
 |  |___|       (______)       |___|        /________\      |___|         |___|  |
 |______________________________________________________________________________|
      ||            ||            ||              ||            ||          ||
     /__\          /__\          /__\            /__\          /__\        /__\
''', clear=True)
    return canvas.text()


def _character_interior():
    canvas = _room("THE TRAINING YARD - THREE WAYS TO SURVIVE TOMORROW", height=34)
    canvas.put(7, 5, r'''
          .--------.
          | X    X |
          |   __   |
          '---++---'
      ________||________
     /        ||        \
    /  .------++------.  \
   /  /|     XXXX     |\  \
  /__/ |    XXXXXX    | \__\
 (___) |     XXXX     | (___)
       '------------'
              ||
              ||
        ______||______
       /______________\
''', clear=True)
    canvas.put(45, 5, r'''
       .----------------.
      /                  \
     /    .----------.    \
    |    /     ++     \    |
    |   |     ++++     |   |
    |   |   ++++++++   |   |
    |    \    ++++    /    |
     \    '----------'    /
      \                  /
       '------.  .------'
              |  |
              |  |
           ___|__|___
          /__________\
''', clear=True)
    canvas.put(82, 5, r'''
     FINISH
      |  |
  ____|__|____
 |            |
 |   /\  /\   |
 |  /  \/  \  |
 | /___/\___\ |
 |            |
 |____________|
       .  .
      .    .
     .  __  .
    .  /  \  .
   .  /____\  .
''', clear=True)
    canvas.put(8, 22, "{strength} Strength: strike true", clear=True)
    canvas.put(43, 22, "{vitality} Vitality: stand firm", clear=True)
    canvas.put(80, 22, "{agility} Agility: move lightly", clear=True)
    canvas.put(5, 25, r'''
   ___                   ___
  [###]=================[###]
   |_|                   |_|
''', clear=True)
    canvas.put(45, 25, r'''
       .----.    .----.
       |XXXX|    |XXXX|
       |____|    |____|
''', clear=True)
    canvas.put(82, 25, r'''
  ____      ____      ____
 /____\    /____\    /____\
    .  .  .  .  .  .  .
''', clear=True)
    return canvas.text()


def _ending_interior():
    canvas = _room("THE LAST CHAMBER - WHAT WILL ASSONANCE REMEMBER?", height=34)
    crown = r'''
 .------------------------------.
 |                              |
 |      .    .    .    .         |
 |      |\__/|\__/|\__/|         |
 |      |      *       |         |
 |      |  *       *   |         |
 |      |______________|         |
 |        \__________/           |
 |             ||               |
 |         ____||____           |
 |        /          \          |
 |       / MANY HANDS \         |
 |      /______________\        |
 |      | HOLD THE WARDS|        |
 |      |______________|        |
 '------------------------------'
'''.strip("\n")
    freedom = r'''
 .------------------------------.
 |                              |
 |               *              |
 |           .   |   .          |
 |         *  \  |  /  *        |
 |          --  (*)  --          |
 |         *  /  |  \  *        |
 |           '   |   '          |
 |               *              |
 |                              |
 |         .----------.         |
 |        /            \        |
 |       /______________\       |
 |       | AN OPEN HAND |        |
 |       |______________|        |
 '------------------------------'
'''.strip("\n")
    canvas.put(4, 5, _straight_walls(crown, 1, 30), clear=True)
    canvas.put(78, 5, _straight_walls(freedom, 1, 30), clear=True)
    canvas.put(47, 7, r'''
      .--------.
     /          \
    |    o  o    |
    |     __     |
     \          /
      '--------'
         ||||
       __||||__
      /        \
     / /|    |\ \
    /_/ |____| \_\
        / || \
       /__||__\
''', clear=True)
    canvas.put(9, 23, "{restore} Restore the wards", clear=True)
    canvas.put(80, 23, "{release} Release the binding", clear=True)
    pedestal = r'''
      ____________
     /            \
    /______________\
   |    A PROMISE   |
   |_______________|
'''.strip("\n")
    canvas.put(9, 25, pedestal, clear=True)
    canvas.put(81, 25, pedestal.replace(" A PROMISE  ", "A BEGINNING "), clear=True)
    return canvas.text()


def _title_panorama():
    canvas = _Canvas(116, 34)
    canvas.put(5, 2, r'''
   _____   _____   _____   ____
  / ____| / ____| / ____| |  _ \
 | (___  | (___  | (___   | | | |
  \___ \  \___ \  \___ \  | | | |
  ____) | ____) | ____) | | |_| |
 |_____/ |_____/ |_____/  |____/
''')
    canvas.put(7, 10, "THE WARDS OF ASSONANCE")
    canvas.put(63, 1, r'''
       |>>>                         <<<|
     __|___                         ___|__
    |_|_|_|           /\            |_|_|_|
    | []  |          /==\           |  [] |
    |     |_________/____\__________|     |
    | []  | |_| |_| | () | |_| |_|  |  [] |
    |     |         |____|          |     |
    |     |      .----------.       |     |
    | []  |      |  /\  /\  |       |  [] |
    |_____|______|_|__||__|_|_______|_____|
           \       /    \        /
            \_____/      \______/
                  |      |
                  |      |
''')
    canvas.put(4, 14, r'''
        8888888
     8888888888888        .----------------.
   88888888888888888     /   TO THE       /|
       |   ||   |      /   ADVENTURER   / |
       ||  ||   |     /________________/  |
       |   ||  ||     |                | /
       ||  ||   |     |________________|/
      / |  ||  | \
 ____/ /|  ||  |\ \____
''')
    canvas.put(27, 25, "{new} Open a new chapter")
    canvas.put(73, 25, "{continue} Continue your story")
    canvas.put(62, 16, r'''
                    /       \
                   /         \
                  /           \
                 /             \
                /               \
               /                 \
              /                   \
             /                     \
            /                       \
''')
    canvas.put(0, 28, r'''
________       ___________                                     ___________      ___________       ___________
        \_____/           \____________             __________/           \____/           \_____/
                                       \___________/
             .                .                .                .                .                .
    .                  .               .                 .                .                .
''')
    return canvas.text()


WIDE_SCREEN_ART = {
    "shop": _shop_interior(),
    "workshop": _workshop_interior(),
    "locals": _locals_interior(),
    "character": _character_interior(),
    "ending": _ending_interior(),
    "title": _title_panorama(),
}



WIDE_LOCATION_ART["desert"] = r'''
                   \    |    /
                    .-------.                                           ___
             ------(   SUN   )------                       _________.--'   '---.____
                    '-------'                    _______.-'                         '---.___
                   /    |    \          ______.-'                                             '---._____
______________________________________.-'_______________________________________________________________'--.__
                  ~                        ~                           ~                         ~
                                            _________
             ___________            _____.-'         '----.                     ___________
        __.-'           '---.____.-'                       '---.___________.---'           '---.__
   __.-'                                                                                          '---.____
.-'                                                                                                        '--.
                                                        {explore} Follow the tracks into the dunes
                  __                                                    .               .
                 /  \                    __                              .               .
       __        |  |                   /  \                              .               .
      /  \       |  |                   |  |                               .               .
      |  |       |  |                   |  |                                .               .
      |  |       |  |                   |  |                                 .               .
      |  |_______|  |___________________|  |                                  .               .
      \__________    _____________________/                                    .               .
                 |  |                                                  /\       .               .
                 |  |                                                 /  \       .      _______
                 |  |                                                /    \_______     /       \
                 |  |                                               /  /\  \      \   /  WATER  \
                 |  |                                              /  /  \  \      \  |         |
                 |  |                                             /__/____\__\______\  \_______/
             ____|__|____                                        |  /      \  |    |
       __.--'            '---.___                                | /        \ |    |        (   )
  __.-'                          '---.____                       |/__________\|____|         ) (
-'                                         '---._____            {rest} Camp beside the dunes  _)(_
        {travel} Road back to the village             '---.______________________________________________
'''.strip("\n")


def _curiosities():
    """Hide small optional discoveries in the landscapes, beside their keys."""
    for collection in (LOCATION_ART, WIDE_LOCATION_ART):
        for location, label in (("village", "Odd well"), ("farm", "A smug crow"),
                                ("desert", "Cactus notice"), ("forest", "Tiny door"),
                                ("sea", "Bottle")):
            if location not in collection:
                continue
            drawing = collection[location]
            if location == "village":
                drawing = drawing.replace("{travel} Road out", " " * 14)
            wide = collection is WIDE_LOCATION_ART
            lines = drawing.splitlines()
            width = max(78 if not wide else 116, max(_visible_width(line) for line in lines))
            canvas = _Canvas(width, len(lines) + 5)
            canvas.put(0, 0, drawing)
            if location == "village":
                canvas.put(31, 18, (" " * 16 + "\n") * 5, clear=True)
                canvas.put(34, 19, r'''
    /\
   /==\
  /____\
  | || |
 .|_||_|.
 |~ ~ ~ |
 '------'
''', clear=True)
                canvas.put(32, 26, "{secret} " + label, clear=True)
                canvas.put(7, 27, "{travel} Road out", clear=True)
            elif location == "farm":
                canvas.put(30, 19, r'''
     ___
   <(o )___
    (_____)>
  ===/|/|======
''', clear=True)
                canvas.put(30, len(lines), "{secret} " + label)
            elif location == "desert":
                x, y = (44, 23) if wide else (29, 15)
                canvas.put(x, y, r'''
 .----------.
 |PERMIT 7B |
 | REQUIRED |
 '----------'
      ||
''', clear=True)
                canvas.put(43 if wide else 28, 29 if wide else 22, "{secret} " + label, clear=True)
            elif location == "forest":
                canvas.put(3, 16, r'''
  .--------.
 /^^^^^^^^^^\
 |  .----.  |
 |  | o  |  |
_|__|____|__|_
''', clear=True)
                canvas.put(3, 22, "{secret} " + label, clear=True)
            elif location == "sea":
                canvas.put(14, 17, r'''
    __
   |__|
   /  \
  | ~~ |
  '----'
''', clear=True)
                canvas.put(9, len(lines), "{secret} " + label)
            collection[location] = canvas.text()


_curiosities()


# Complete landscapes for wide terminals. Each drawing has a shared horizon,
# foreground and path; these are composed scenes rather than doubled panels.
_WIDE_TENT = r'''
          /\
         /  \
        /    \_______
       /  /\  \      \
      /  /  \  \      \
     /__/____\__\______\
     |  /    \  |    |
     | /      \ |    |
     |/________\|____|
'''.strip("\n")

_WIDE_LANTERN = r'''
   .------.
  /________\
  |   /\   |
  |  (  )  |
  |   \/   |
  '--------'
      ||
      ||
'''.strip("\n")

_WIDE_CRYSTAL = r'''
      /\
     /||\
    / || \
   /  ||  \
   \  ||  /
    \ || /
     \||/
      \/
'''.strip("\n")


def _wide_caves():
    canvas = _Canvas(116, 34)
    canvas.put(0, 0, r'''
             ______                  ___________                       ___________                 ________
     _______/      \________________/           \_____________________/           \_______________/        \__
 ___/       /\                 /\             /\                     /\                       /\              \
/           ||                 ||            /  \                    ||                      /  \              \
|           ||                 ||            \  /                    ||                      \  /              |
|           \/                 \/             \/                     \/                       \/               |
''')
    for y in range(6, 33):
        canvas.put(0, y, "|")
        canvas.put(114, y, "|")
    canvas.put(3, 7, _WIDE_CRYSTAL)
    canvas.put(18, 12, _WIDE_CRYSTAL)
    canvas.put(35, 5, _WIDE_CRYSTAL)
    canvas.put(29, 15, r'''
        .         .         .         .
       .                               .
      .                                 .
     .                                   .
    .                                     .
   .                                       .
  .                                         .
 .                                           .
''')
    canvas.put(71, 7, r'''
         .-------------------------.
        /  /\   /\   /\   /\   /\  \
       |  /__\_/__\_/__\_/__\_/__\  |
       |     ____         ____      |
       |    /    \       /    \     |
       |    | () |       | () |     |
       |    \____/       \____/     |
       |          _______           |
       |         /       \          |
       |        /_________\         |
       |____________________________|
        /    |             |    \
    ___/     |             |     \___
   /         |_____________|         \
  |__________|             |__________|
       |   |                  |   |
       |___|                  |___|
''')
    canvas.put(10, 24, _WIDE_TENT)
    canvas.put(44, 26, r'''
  (    )
   )  (
  ( /\ )
 __)_(__
''')
    canvas.put(33, 14, "{explore} Follow the crystal tracks")
    canvas.put(76, 25, "{challenge} The stone guardian")
    canvas.put(12, 33, "{rest} Sheltered camp")
    canvas.put(62, 33, "{travel} Return to daylight")
    return canvas.text()


def _wide_sea():
    canvas = _Canvas(116, 35)
    canvas.put(5, 1, r'''
     .----.                         .----.
  .-(      )-.                   .-(      )-.
 (____________)                 (____________)
''')
    canvas.put(22, 5, r'''
                  |                 |\
                  |\                | \
                  | \               |  \
                  |  \              |   \
             _____|___\_____________|____\_
             \                           /
              \_________________________/
''')
    canvas.put(2, 12, "~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~")
    canvas.put(0, 15, r'''
     ~         ~         ~         ~         ~         ~         ~         ~         ~         ~         ~
 ~       ~         ~         ~         ~         ~         ~         ~         ~         ~         ~        ~
    _______          _______          _______          _______          _______          _______          _____
___/       \________/       \________/       \________/       \________/       \________/       \________/
''')
    canvas.put(87, 0, r'''
          |>>>
        __|__
       |_____|
     __|_____|__
    /===========\
    |  .-----.  |
    |  | (O) |  |
    |  '-----'  |
    |_____||____|
    |     ||    |
    |   [====]  |
    |           |
    |  []   []  |
    |           |
    |    ___    |
    |   |   |   |
 ___|___|___|___|___
/___________________\
''', clear=True)
    canvas.put(7, 23, r'''
      __
     |__|
     /  \
    / ~~ \
    | () |
    '----'
''')
    canvas.put(45, 23, r'''
      .---.
   .-'     '-.
  /   .---.   \
  \  (_____)  /
   '---------'
''')
    canvas.put(76, 23, _WIDE_TENT)
    canvas.put(31, 19, "{explore} Search the tide line")
    canvas.put(84, 20, "{challenge} The drowned bell")
    canvas.put(3, 30, "{secret} Bottle")
    canvas.put(75, 33, "{rest} Beach camp")
    canvas.put(4, 34, "{travel} Follow the coastal road")
    canvas.put(28, 28, r'''
       .          .          .          .
      .                                  .
     .                                    .
    .                                      .
''')
    return canvas.text()


def _wide_bridge():
    canvas = _Canvas(116, 34)
    canvas.put(4, 1, r'''
           /\                                                                          /\
          /==\                        THE LAST HONEST BRIDGE                          /==\
         /====\                                                                      /====\
        /______\              |     |     |     |     |     |                       /______\
        |  []  |______________|_____|_____|_____|_____|_____|_______________________|  []  |
        |      |==============|=====|=====|=====|=====|=====|=======================|      |
        |  []  |                                                                    |  []  |
        |      |                                                                    |      |
        |______|____________________________________________________________________|______|
             \           /\           /\           /\           /\           /
              \_________/  \_________/  \_________/  \_________/  \_________/
                  |   |        |   |        |   |        |   |        |   |
                  |   |        |   |        |   |        |   |        |   |
                  |   |        |   |        |   |        |   |        |   |
                 _|___|_      _|___|_      _|___|_      _|___|_      _|___|_
''')
    canvas.put(28, 8, "{explore} Patrol the ancient crossing", clear=True)
    canvas.put(0, 16, r'''
  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
     ~       ~       ~       ~       ~       ~       ~       ~       ~       ~       ~       ~       ~
 ~       ~       ~       ~       ~       ~       ~       ~       ~       ~       ~       ~       ~       ~
     ~       ~       ~       ~       ~       ~       ~       ~       ~       ~       ~       ~       ~
______________________________________________________________________________________________________________
''')
    canvas.put(7, 24, _WIDE_LANTERN)
    canvas.put(76, 23, _WIDE_TENT)
    canvas.put(48, 27, r'''
  (   )
   ) (
  ( /\ )
 __)_(__
''')
    canvas.put(23, 33, "{travel} River road")
    canvas.put(76, 33, "{rest} Riverside camp")
    canvas.put(27, 23, r'''
   .                              .
    .                            .
     .                          .
      .                        .
       .                      .
''')
    return canvas.text()


def _wide_plains():
    canvas = _Canvas(116, 34)
    canvas.put(0, 0, r'''
          .----.                                .----.                                  .----.
       .-(      )-.                          .-(      )-.                            .-(      )-.
      (____________)                        (____________)                          (____________)

                        ________                           ________                          ________
           ____________/        \_________________________/        \________________________/        \______
__________/
''')
    canvas.put(5, 7, r'''
      \  |  /
       \ | /
    ----(O)----
       / | \
      /__|__\
      |  _  |
      | | | |
 _____|_|_|_|____
''')
    canvas.put(47, 9, r'''
      .-----------.
     /             \
    /   .-------.   \
   |    |  /\   |    |
   |    | (  )  |    |
   |    |  \/   |    |
   |    '-------'    |
   |_________________|
''')
    canvas.put(27, 15, _WIDE_LANTERN)
    canvas.put(81, 11, _WIDE_LANTERN)
    canvas.put(44, 19, "{explore} Follow the old lantern road")
    canvas.put(38, 21, r'''
       .                         .
      .                         .
     .                         .
    .                         .
   .                         .
  .                         .
 .                         .
.                         .
''')
    canvas.put(5, 26, r'''
  \|/            \|/
   |              |
  / \            / \
''')
    canvas.put(78, 23, _WIDE_TENT)
    canvas.put(5, 33, "{travel} Road to the village")
    canvas.put(77, 33, "{rest} Camp in the tall grass")
    canvas.put(1, 32, "_" * 110)
    return canvas.text()


def _wide_mountains():
    canvas = _Canvas(116, 35)
    canvas.put(0, 0, r'''
                                      /\                                     /\
                   /\                /  \                  /\               /  \
                  /  \              /    \                /  \             /    \
         /\      /    \            /  /\  \              /    \           /  /\  \
        /  \    /  /\  \          /  /  \  \            /  /\  \         /  /  \  \
       /    \__/  /  \  \________/  /    \  \__________/  /  \  \_______/  /    \  \___
      /  /\                  /     /      \                 /\           /      \      \
     /  /  \      /\        /     /        \               /  \         /        \      \
    /  /    \    /  \      /     /          \_____________/    \_______/          \______\
   /  /      \__/    \____/     /                                                        \
__/__/                                                                                   \____________
''')
    canvas.put(67, 12, r'''
             /\                 /\
            /  \    _______    /  \
           / /\ \__/       \__/ /\ \
          / /  \    o   o     /  \ \
         / /    \     ^     /    \ \
        /_/      \   ___   /      \_\
                  \__V_V__/
                   /|   |\
            ______/ |___| \______
           /                     \
         _/_______________________\_
        /__\__\__\__\__\__\__\__\__\
''')
    canvas.put(4, 12, _WIDE_LANTERN)
    canvas.put(21, 14, "{explore} Climb the winding pass")
    canvas.put(23, 16, r'''
                    .                 .
                   .                 .
                  .                 .
                 .                 .
                .                 .
               .                 .
              .                 .
             .                 .
            .                 .
''')
    canvas.put(6, 24, _WIDE_TENT)
    canvas.put(75, 25, "{challenge} The drake's nest")
    canvas.put(7, 34, "{rest} Sheltered high camp")
    canvas.put(62, 34, "{travel} Down the mountain")
    canvas.put(48, 28, r'''
   (   )
    ) (
   ( /\ )
  __)_(__
''')
    return canvas.text()


def _wide_castle():
    canvas = _Canvas(116, 35)
    canvas.put(4, 0, r'''
        |>>>                                     /\                                      <<<|
      __|___                                    /==\                                    ___|__
     |_|_|_|                                   /====\                                   |_|_|_|
     |  [] |                                  /______\                                  | []  |
     |     |                                  |  ()  |                                  |     |
     | []  |__________________________________|______|__________________________________|  [] |
     |     | |_| |_| |_| |_| |_| |_| |_| |_| |_|_|__|_|_| |_| |_| |_| |_| |_| |_| |_| |_ |     |
     |  [] |                                                                            | []  |
     |     |                                                                            |     |
     | []  |                             THE HOLLOW CROWN                               |  [] |
     |     |                              .-------------.                               |     |
     |  [] |                              |    /\ /\    |                               | []  |
     |     |                              |   /  V  \   |                               |     |
     | []  |                              |  |   |   |  |                               |  [] |
     |_____|______________________________|__|___|___|__|_______________________________|_____|
            \                              /           \                              /
             \____________________________/             \____________________________/
                        .                |               |                .
                       .                 |               |                 .
                      .                  |      ___      |                  .
                     .                   |     /   \     |                   .
                    .                    |    /     \    |                    .
                   .                     |   /       \   |                     .
                  .                      |__/         \__|                      .
''')
    canvas.put(17, 12, "{explore} Search the courts", clear=True)
    canvas.put(63, 12, "{challenge} Enter the throne room", clear=True)
    canvas.put(5, 25, _WIDE_TENT)
    canvas.put(83, 27, r'''
    .-----.
   /  /\   \
  |  (  )  |
   \__\/__/
''')
    canvas.put(30, 26, "{travel} Castle road")
    canvas.put(9, 34, "{rest} Camp outside the walls")
    canvas.put(43, 25, r'''
        /             \
       /               \
      /                 \
     /                   \
    /                     \
   /                       \
  /                         \
 /                           \
''')
    return canvas.text()


WIDE_LOCATION_ART.update({
    "caves": _wide_caves(),
    "sea": _wide_sea(),
    "bridge": _wide_bridge(),
    "plains": _wide_plains(),
    "mountains": _wide_mountains(),
    "castle": _wide_castle(),
})
