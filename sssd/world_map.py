"""A compact illustrated atlas: travel keys live inside their destinations.

These are regional vignettes rather than a road diagram. Their adjacency does
not imply a route; the world graph alone decides which destinations get keys.
All drawing characters are ASCII, so character counts equal terminal columns.
"""

from .content import LOCATIONS


SHORT_NAMES = {
    "sea": "SEA", "castle": "CASTLE", "forest": "FOREST",
    "village": "VILLAGE", "farm": "FARM", "mountains": "MOUNTAINS",
    "caves": "CAVES", "plains": "PLAINS", "bridge": "BRIDGE", "desert": "DESERT",
}

_ORDER = ("sea", "castle", "forest", "village", "farm",
          "mountains", "caves", "plains", "bridge", "desert")
_CELL_WIDTH = 14


def _vignette(location: str, marker: str, locked: bool) -> list[str]:
    label = SHORT_NAMES[location] + "[" + marker + "]"
    inside = label.center(12)
    scenes = {
        "sea": [
            r" ~    __|__ ~ ",
            r"    __\___/   ",
            "~" + inside + "~",
            r"  ~     ~     ",
            r"~  ~~~    ~~~ ",
            r" ~~   ~~~   ~ ",
        ],
        "castle": [
            r" |_|_|_|_|_|  ",
            r" | ^     ^ |  ",
            "|" + inside + "|",
            r" | []   [] |  ",
            " |   LOCK  |  " if locked else r" |   /\    |  ",
            r"_|___|_|___|_ ",
        ],
        "forest": [
            r"  /\  /\ /\   ",
            r" /^^\/^^V^^\  ",
            "/" + inside + "\\",
            r" /^^\/^^\/^\  ",
            r"  || || ||    ",
            r"._||_||_||_.  ",
        ],
        "village": [
            r"   /\  /\     ",
            r" _/ _\/ _\_   ",
            "|" + inside + "|",
            r"| []  __  [] |",
            r"|____|__|____|",
            r" .  .  .  .   ",
        ],
        "farm": [
            r"   _/\_   \|/ ",
            r"  /____\   |  ",
            "|" + inside + "|",
            r" |__[]__| ::: ",
            r"  ::: ::: ::: ",
            r"  ::: ::: ::: ",
        ],
        "mountains": [
            r"   /\ /\      ",
            r"  /  V  \     ",
            "/" + inside + "\\",
            r" / ^  /\ \    ",
            r"/___\/__\_\   ",
            r"  ^  ^  ^     ",
        ],
        "caves": [
            r"   _______    ",
            r" _/       \_  ",
            "/" + inside + "\\",
            r"|   /^^^\   | ",
            r"|___|   |___| ",
            r"  .  ...  .   ",
        ],
        "plains": [
            r"       .      ",
            r"  \|/  |  \|/ ",
            "(" + inside + ")",
            r"  \|/    \|/  ",
            r"_.,___.,___._ ",
            r" .   .    .   ",
        ],
        "bridge": [
            r"   |      |   ",
            r" __|______|__ ",
            "|" + inside + "|",
            r" __|______|__ ",
            r" ~ |  ~~  | ~ ",
            r"~~  ~   ~~  ~ ",
        ],
        "desert": [
            r"  _   |   _   ",
            r" |_|  |  |_|  ",
            "(" + inside + ")",
            r"   \__|__/    ",
            r"  _   |  __   ",
            r"_/ \__|_/  \_ ",
        ],
    }
    return [line.ljust(_CELL_WIDTH) for line in scenes[location]]


def render_world_map(current: str, choices: dict[str, str], width: int,
                     *, sealed: bool = False) -> str:
    """Draw all ten regions, using the caller's actual neighbor key assignments.

    ``sealed=True`` means the three ward seals are recovered and the castle is
    open. A locked castle has ``[#]`` unless it has a travel key, in which case
    that key and a separate ``LOCK`` label appear inside its battlements.

    At >=76 columns this returns a 76-column, 14-line panorama. At 48..75 it
    returns a 46-column, 14-line atlas. Below 48 it returns an empty string so
    the caller can provide a narrower menu. It never crops names or markers.
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

    compact = width < 76
    columns = 3 if compact else 5
    cell_height = 3 if compact else 6
    inner_width = columns * _CELL_WIDTH + columns - 1
    title = " ASSONANCE / TRAVELLER'S ATLAS "
    lines = ["+" + title.center(inner_width, "-") + "+"]
    cells = []
    for location in _ORDER:
        marker = "@" if location == current else choices.get(location)
        if marker is None:
            marker = "#" if location == "castle" and not sealed else "."
        drawing = _vignette(location, marker, location == "castle" and not sealed)
        if compact:
            drawing = [drawing[row] for row in (0, 2, 4)]
        cells.append(drawing)
    while len(cells) % columns:
        cells.append([" " * _CELL_WIDTH] * cell_height)
    for offset in range(0, len(cells), columns):
        row = cells[offset:offset + columns]
        for line_index in range(cell_height):
            lines.append("|" + " ".join(cell[line_index] for cell in row) + "|")
    lines.append("+" + "-" * inner_width + "+")
    return "\n".join(lines)
