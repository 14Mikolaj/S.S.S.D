"""Terminal-sized illustrations whose numbered hotspots use the real menu keys."""

from __future__ import annotations

from dataclasses import dataclass
import re
import textwrap


@dataclass(frozen=True)
class Illustration:
    pages: tuple[str, ...]
    keys: frozenset[str] = frozenset()


TOKEN = re.compile(r"\{([a-z_]+)\}")


def scene(template: str, choices: dict[str, str], width: int) -> Illustration | None:
    """Substitute semantic hotspots without changing the art's column alignment."""
    tokens = set(TOKEN.findall(template))
    if not tokens <= choices.keys():
        return None  # Never advertise a choice that the menu cannot dispatch.
    drawing = TOKEN.sub(lambda match: f"[{choices[match[1]]}]", template).strip("\n")
    lines = [line.rstrip() for line in drawing.splitlines()]
    if not lines or max(map(len, lines)) > width:
        return None
    return Illustration(("\n".join(lines),), frozenset(choices[token] for token in tokens))


def cards(entries, width: int, height: int = 24, *, max_lines=None) -> Illustration:
    """Lay out labeled objects in a paged display; never crop a label or sprite.

    Entries are (menu key, label, ASCII sprite). Text wraps inside the frame;
    drawings keep their geometry. Numbers remain stable across pages.
    """
    if not entries:
        return Illustration(("(Nothing on this shelf yet.)",))
    columns = max(1, min(3, (width + 2) // 25))
    card_width = (width - 2 * (columns - 1)) // columns
    inside = card_width - 4
    blocks = []
    for key, label, sprite in entries:
        picture = sprite.strip("\n").splitlines()
        if any(len(line) > inside for line in picture):
            # A tiny object still marks the item on exceptionally small displays.
            picture = [r" /\ ", "<  >", r" \/ "]
        caption = []
        for line in f"[{key}] {label}".splitlines():
            caption.extend(textwrap.wrap(line, inside) or [""])
        blocks.append(picture + [""] + caption)

    rows = []
    for start in range(0, len(blocks), columns):
        group = blocks[start:start + columns]
        body_height = max(map(len, group))
        border = "+" + "-" * (card_width - 2) + "+"
        row = ["  ".join(border for _ in group)]
        for line in range(body_height):
            row.append("  ".join(
                "| " + (block[line] if line < len(block) else "").ljust(inside) + " |"
                for block in group
            ))
        row.append("  ".join(border for _ in group))
        rows.append(row)

    # Leave space for the screen heading, equipment/status, controls and prompt.
    budget = max(1, height - 9 if max_lines is None else max_lines)
    pages, page = [], []
    for row in rows:
        if page and len(page) + len(row) > budget:
            pages.append("\n".join(page))
            page = []
        page.extend(row)
    if page:
        pages.append("\n".join(page))
    return Illustration(tuple(pages), frozenset(str(entry[0]) for entry in entries))


# Pocket-sized props also serve as visual fallbacks for narrow terminals.
PROPS = {
    "locals": r"  o o o  " "\n" r" /|/|/|\ " "\n" r" /|/|/|  ",
    "quests": r" .----. " "\n" r" | !? | " "\n" r" '--||' ",
    "shop": r"  /___\  " "\n" r" | $ $ | " "\n" r" |__[]_| ",
    "smith": r"   /==  " "\n" r" __|___ " "\n" r"  \__/  ",
    "rest": r"    z Z " "\n" r" |o____ " "\n" r" |____| ",
    "travel": r"  /\  " "\n" r" /  \ " "\n" r"/ || \ ",
    "explore": r" \ | / " "\n" r" --+-- " "\n" r" / | \ ",
    "challenge": r" |^|^| " "\n" r" |/ \| " "\n" r" || || ",
    "harvest": r" \|/\|/ " "\n" r" -|-|-- " "\n" r" _|_|__ ",
    "farmer": r" _===_ " "\n" r"  (o)  " "\n" r" /|\   ",
    "inventory": r" .----. " "\n" r" | [] | " "\n" r" '----' ",
    "character": r"  o  " "\n" r" /|\ " "\n" r" / \ ",
    "journal": r" ___ ___ " "\n" r"|___|___|" "\n" r"|___|___|",
    "ending": r" \ * / " "\n" r" --O-- " "\n" r" / | \ ",
    "attack": r"   / " "\n" r"  /  " "\n" r"=+=  ",
    "power": r" * / *" "\n" r"  /   " "\n" r"=+= * ",
    "guard": r"/---\ " "\n" r"| + |" "\n" r" \_/ ",
    "mend": r"  +  " "\n" r"+ + +" "\n" r"  +  ",
    "potion": r" _||_ " "\n" r"( HP )" "\n" r" \__/ ",
    "antidote": r" _||_ " "\n" r"( XX )" "\n" r" \__/ ",
}

LANDMARKS = {
    "village": r" /\ /\ /\ " "\n" r"/__/__/__\ " "\n" r"|[]|[]|[]|",
    "farm": r"  /\  \|/ " "\n" r" /__\  |  " "\n" r" |[]| ::: ",
    "desert": r"  _|_   " "\n" r" |_|_|  " "\n" r"___|____",
    "caves": r"  _____  " "\n" r" / /^^\ \ " "\n" r"/__|  |__\ ",
    "forest": r" 888 888 " "\n" r"888888888" "\n" r" _||_||_ ",
    "sea": r"    |\   " "\n" r"  __|_\  " "\n" r"~~\___/~~",
    "bridge": r" |_|_|_| " "\n" r"_/_____\_" "\n" r"~~|~~~|~~",
    "plains": r"   .--.  " "\n" r" \|/  \|/" "\n" r"__|____|_",
    "mountains": r"   /\ /\ " "\n" r"  /  V  \ " "\n" r"_/__/\___\ ",
    "castle": r" |_|_|_| " "\n" r" | []  | " "\n" r"_|__[]_|_",
}


COMBAT_ACTIONS = r"""
     /  {attack} Attack       / * {power} Power (-3E)   /---\ {guard} Guard (+3E)
   =+=                      =+=                     \_+_/
    +   {mend} Mend (-4E)    (HP) {potion} Potion      (XX) {antidote} Antidote
"""

COMPACT_COMBAT_ACTIONS = r"""
 / {attack} Attack   /* {power} Power -3E
(_) {guard} Guard +3E  + {mend} Mend -4E
(+) {potion} Potion  (x) {antidote} Antidote
"""
