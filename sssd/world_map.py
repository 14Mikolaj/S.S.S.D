"""The original island restored, with continuous landscapes for smaller screens.

Location markers are rebound to the active menu, never to historical numbers.
Land outlines and landmarks describe geography; they do not invent road links.
"""

import re

from .content import LOCATIONS
from .legacy_art import ORIGINAL_WORLD_MAP


SHORT_NAMES = {
    "sea": "SEA", "castle": "CASTLE", "forest": "FOREST",
    "village": "VILLAGE", "farm": "FARM", "mountains": "MOUNTAINS",
    "caves": "CAVES", "plains": "PLAINS", "bridge": "BRIDGE", "desert": "DESERT",
}

_DETAILED_ISLAND = r'''
         ~                    ~                         ~                             ~
                                ______________________________
                      _________/              /\              \______              ~
       ~             /                    ___/^^\___                 \______
                    /          I>        /  (oo)    \      <I                \__
                   /           |      __/  /  \\    \__     |                   \___
   ~              /          _/\_   _/____/____\\______\_  _/\_       8888           \
                 /           |[]|___|                  |___|[]|    8888888            \
                /            |  |   |  _   _   _   _   |   |  |       ||      8888     |
               /             |[]|   | |_| |_| |_| |_|  |   |[]|    8888888   8888888   |
              /              |__|___|_______/\_________|___|__|       ||        ||     |
  ~          /                    CASTLE[?]     /__\          _______/  \_______||__   |
    __|__   /          8888                 __/____\__       /    /\    /\     /\   \  |
   /__|_\  /       8888888888              /__________\     /    /__\__/__\___/__\   | |
 ~~\____/~/   8888     ||      8888                         |    |[]|  |[]|   |[]|   | |
  SEA[?] /  8888888  8888888  88888888    8888               |    VILLAGE[?]          | |
   ~    /      ||      ||       ||    888888888              \___|__|__|__|___|__|__/  |
       /     8888888  FOREST[?] 8888888    ||     .     .         .   .    .    .       |
      /         ||    8888888     ||   8888888                      _       _           |
     /     /\   ||      ||   /\  ||      ||           .         _| |_____| |_         |
    /     /^^\ /  \    /  \ /^^\/  \    /  \                   | |___   ___| |        |
   /    _/    \_      /\  _/    \_     /\            .          \____| |____/         |
  /    /  /\    \    /^^\/  /\    \   /^^\        PLAINS[?]           | |      _        |
 /    /__/  \____\__/    \_/  \____\_/    \__                      ___|_|____/ \__     |
|       MOUNTAINS[?]        /\                \|/  \|/  \|/       DESERT[?]             |
|   /\     /\    /\       /^^\                |    |    |                     .        |
|__/^^\___/^^\__/^^\_____/    \___         .  .  .  .  .  .         ______________      |
|  /    \ /    \/    \         ___\_                               /______________\     |
|_/      V      \     \       /     \             _____            | []  __  [] |      |
|      _______________       /       \___________/     \_          |____|__|____|      |
 \    /     /^^^^\    \_____/                    |  |    \           ::: ::: :::       |
  \__/      |    |                             _|__|__   \     \|/  ::: ::: :::       |
      CAVES[?]          .          ~       ~   |______|   |     -+-    FARM[?]         |
       \                                  ~   |______|   |      |   ::: ::: :::      |
        \_____            _______            BRIDGE[?]   |          ::: ::: :::     /
              \__________/       \___          |  |      /\_________________________/
     ~                               \_________|__|_____/                     ~
                   ~                           ~                  ~
'''

_SCENIC_ISLAND = r'''
       ~                 ____________________                  ~
                 _______/       /\           \_____
    ~           /       I>   __/^^\__   <I         \______
               /       _/\_ /  (oo)  \ _/\_                \_
              /        |[]|/___/\___\|[]|       8888         \
             /         |  |   /__\   |  |     8888888        |
      ~     /          |__|___|__|___|__|        ||     8888  |
   __|__   /              CASTLE[?]          ___/\____8888888 |
  /__|_\  /    8888       8888              /____\  /\   ||  |
 ~\____/~/  888888888   888888888  8888     |[]  []|/__\_/  \ |
 SEA[?] /      ||         ||    8888888    | VILLAGE[?] |    |
   ~   /    8888888   FOREST[?]    ||      |___|__|__|__|    |
      /        ||      8888888  8888888                      |
     /   /\   /  \        ||      ||          _    |    _    |
    /   /^^\      /\     /  \    /  \        |_|___|___|_|   |
   /   / /\ \    /^^\        .        .        \___   __/    |
  /___/ /  \_\__/    \___         PLAINS[?]        | |       |
 |      MOUNTAINS[?]     \    \|/  \|/  \|/      DESERT[?]   |
 |   /\    /\      /\     \    |    |    |         |_|       |
 |__/^^\__/^^\____/^^\____/            .        ____________ |
 |   ____/^^^^^\___           ____            /____________\|
  \_/    |     |   \_________/    \          | []  __  [] | |
   CAVES[?]                      | |  \       |____|__|____| |
    \                  ~        _|_|_  |        ::: :::    |
     \____       ____     ~    |_____| |  \|/   FARM[?]    |
          \_____/    \___       BRIDGE[?]   |    ::: :::   /
   ~                    \______|_|_|___/\_______________/
                 ~                           ~
'''

_NARROW_ISLAND = r'''
   ~                ~                 ~
             __________________
       _____/        /\        \____
      /    I>     __/^^\__   <I      \
     /    _/\_   /  (oo)  \ _/\_     |
    /     |[]|___|__/\____|_|[]|     |
   /      |  |     /__\    |  |     |
  /       |__|_____|__|____|__|     /
 /             CASTLE[?]          /
|      8888           8888       |
|    88888888       88888888      |
|       ||    FOREST[?] ||       |
|    88888888       88888888      |
|       ||            ||        |
|______/  \__________/  \___     |
     ~    __|__            \    |
  SEA[?] /__|_\      /\  /\ \   |
  ~   ~  \____/   __/__\/__\_\  |
       ~   ~     | []    []   | |
                 | VILLAGE[?]| |
          _______|____|__|___| |
   ~     /                     |
        /    /\    /\          |
       /    /^^\__/^^\          \
      / ___/    \/    \___       |
     /     MOUNTAINS[?]          |
    /       /\  /\              |
   /  _____/^^\/^^\____         |
  /  /    /^^^^\       \        |
 |__/     |    |        \       |
 |    CAVES[?]        .         |
 |            .    .      .     |
 |    \|/ \|/ \|/    _   |   _  |
 |     |   |   |    |_|__|__|_| |
 |    PLAINS[?]      \___ ___/  |
 |                       |     |
 |   __________      DESERT[?]  |
 |  /__________\        _|_     |
 |  | [] __ [] |               |
 |  |___|__|___|     ::: :::    |
 |      FARM[?]      ::: :::    |
  \       _________            /
   \_____/   | |   \__________/
        ~  __|_|__         ~
    ~     |_______|  ~
          BRIDGE[?]
      ~      | |          ~
'''


def _lines(art: str) -> list[str]:
    return [line.rstrip() for line in art.strip("\n").splitlines()]


def _with_coastal_tower(art: str, margin: int) -> str:
    """Keep the old map's offshore watchtower beside the smaller island."""
    lines = [" " * margin + line for line in _lines(art)]
    tower = [r"   /\ ", r"  /__\ ", r"  |8 |", r" /___\ ", r" |III|",
             r" |   |", r" |III|", r" |   |", r" |III|", r"_|___|_",
             r" /|||\ ", r"/_____\ ", r"  ~  ~"]
    for row, stroke in enumerate(tower, 4):
        lines[row] = stroke.ljust(margin) + lines[row][margin:]
    return "\n".join(lines)


_LABEL = re.compile(r"\b(" + "|".join(SHORT_NAMES.values()) + r") ?\[(?:\d+|\?)\]")


def _bind_markers(art: str, current: str, choices: dict[str, str], sealed: bool) -> str:
    markers = {}
    for location, name in SHORT_NAMES.items():
        marker = "@" if location == current else choices.get(location)
        if marker is None:
            marker = "#" if location == "castle" and not sealed else "."
        markers[name] = marker

    def replace(match):
        name = match[1]
        # Retain every original column, including the old two-digit mountain key.
        return (name + "[" + markers[name] + "]").ljust(len(match[0]))

    lines = _lines(_LABEL.sub(replace, art))
    if not sealed:
        for index, line in enumerate(lines):
            if "CASTLE[" in line:
                lines[index] = re.sub(r"(CASTLE\[[^]]\]) {5}", r"\1 LOCK", line, count=1)
                break
    return "\n".join(lines)


def render_world_map(current: str, choices: dict[str, str], width: int,
                     *, sealed: bool = False) -> str:
    """Render a detailed island; the caller may pan a tall drawing vertically.

    At 173+ columns this restores the actual 173x64 legacy island. At 146..172
    only its empty offshore margin is removed, preserving every land feature.
    Smaller terminals receive continuous illustrated islands: 105x38 at 105+
    columns, 74x28 at 74+, and 39x47 at 48+. Below 48 this returns an empty string
    so the interface can use accessible destination cards instead of clipping.

    ``sealed=True`` means all ward seals are recovered and the castle is open.
    Otherwise its marker is [#], or its actionable key, with LOCK beside it.
    """
    if width < 48:
        return ""
    if current not in LOCATIONS:
        raise ValueError("The current location is not in the world.")
    neighbors = set(LOCATIONS[current]["neighbors"])
    for destination, key in choices.items():
        if destination not in neighbors:
            raise ValueError("Travel keys must refer to actual neighboring destinations.")
        if not isinstance(key, str) or len(key) != 1 or key not in "123456789":
            raise ValueError("Travel keys must be one-digit strings from the current menu.")
    if len(set(choices.values())) != len(choices):
        raise ValueError("Travel keys must be unique.")

    if width >= 173:
        art = ORIGINAL_WORLD_MAP
    elif width >= 146:
        # These 27 columns contain only spaces and isolated waves, no island art.
        art = "\n".join(line[27:] for line in _lines(ORIGINAL_WORLD_MAP))
    elif width >= 105:
        art = _with_coastal_tower(_DETAILED_ISLAND, 16)
    elif width >= 74:
        art = _with_coastal_tower(_SCENIC_ISLAND, 10)
    else:
        art = _NARROW_ISLAND
    return _bind_markers(art, current, choices, sealed)
