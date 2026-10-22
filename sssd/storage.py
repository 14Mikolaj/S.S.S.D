"""Versioned, validated JSON saves with atomic replacement and a good backup."""

from dataclasses import asdict, fields
import json
import os
from pathlib import Path
import tempfile

from .content import ENEMIES, ITEMS, LOCATIONS, QUESTS
from .model import GameState, Player


SAVE_VERSION = 1
MAX_SAVE_BYTES = 512 * 1024
MAX_NUMBER = 10_000_000


class SaveError(Exception):
    """A save could not be read or written safely."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SaveError(message)


def _integer(value, name: str, minimum: int = 0, maximum: int = MAX_NUMBER) -> int:
    _require(type(value) is int and minimum <= value <= maximum,
             f"Invalid {name}: expected an integer from {minimum} to {maximum}.")
    return value


def _string(value, name: str, maximum: int = 160) -> str:
    _require(isinstance(value, str) and 0 < len(value) <= maximum,
             f"Invalid {name}: expected nonempty text up to {maximum} characters.")
    _require(all(character.isprintable() for character in value),
             f"Invalid {name}: control characters are not allowed.")
    return value


def _object(value, name: str) -> dict:
    _require(type(value) is dict, f"Invalid {name}: expected an object.")
    return value


def _keys(value: dict, expected: set[str], name: str) -> None:
    _require(set(value) == expected, f"Invalid {name}: fields are missing or unrecognized.")


def _string_set(value, name: str, known: set[str] | None = None) -> set[str]:
    _require(type(value) is list and len(value) <= 1000,
             f"Invalid {name}: expected a short list.")
    checked = [_string(item, name) for item in value]
    _require(len(set(checked)) == len(checked), f"Invalid {name}: duplicate entries.")
    if known is not None:
        _require(set(checked) <= known, f"Invalid {name}: unknown entry.")
    return set(checked)


def _decode(document) -> GameState:
    root = _object(document, "save")
    _keys(root, {"version", "state"}, "save")
    _require(type(root["version"]) is int and root["version"] == SAVE_VERSION,
             f"Unsupported save version; this game reads version {SAVE_VERSION}.")
    data = _object(root["state"], "state")
    _keys(data, {field.name for field in fields(GameState)}, "state")
    player_data = _object(data["player"], "player")
    _keys(player_data, {field.name for field in fields(Player)}, "player")
    _string(player_data["name"], "player name", 40)
    for name in ("level", "strength", "vitality", "agility"):
        _integer(player_data[name], name, minimum=1, maximum=10000)
    for name in ("xp", "gold", "hp", "energy", "stat_points"):
        _integer(player_data[name], name)

    inventory = _object(player_data["inventory"], "inventory")
    _require(set(inventory) <= set(ITEMS), "Inventory contains an unknown item.")
    for item_id, quantity in inventory.items():
        _integer(quantity, f"quantity of {item_id}", minimum=1)
    equipment = _object(player_data["equipment"], "equipment")
    _keys(equipment, {"weapon", "armor", "charm"}, "equipment")
    for slot, item_id in equipment.items():
        if item_id is not None:
            _require(isinstance(item_id, str) and item_id in inventory,
                     "Equipped items must be owned.")
            _require(ITEMS[item_id].get("slot") == slot,
                     "An equipped item is in the wrong slot.")
    upgrades = _object(player_data["upgrades"], "upgrades")
    for item_id, level in upgrades.items():
        _require(item_id in inventory and ITEMS[item_id].get("slot") in {"weapon", "armor"},
                 "An upgrade must refer to an owned weapon or armor.")
        _integer(level, f"upgrade of {item_id}", maximum=3)
    player = Player(**player_data)
    _require(player.hp <= player.max_hp and player.energy <= player.max_energy,
             "Health or energy exceeds its maximum.")
    _require(player.xp < player.xp_to_next, "Experience exceeds the next level threshold.")

    location = _string(data["location"], "location")
    _require(location in LOCATIONS, "Save refers to an unknown location.")
    day = _integer(data["day"], "day", minimum=1)
    steps = _integer(data["steps"], "steps")
    _require(day == 1 + steps // 6, "The day does not match the travel counter.")
    harvest_day = _integer(data["harvest_day"], "harvest day")
    _require(harvest_day <= day, "The last harvest cannot be in the future.")
    visited = _string_set(data["visited"], "visited locations", set(LOCATIONS))
    _require(location in visited, "The current location must have been visited.")
    known_flags = {"story_started", "seal_root", "seal_stone", "seal_tide", "finale_ready", "ended"}
    known_flags.update(f"boss:{enemy_id}" for enemy_id in ENEMIES)
    flags = _string_set(data["flags"], "flags", known_flags)
    quests = _object(data["quests"], "quests")
    _require(set(quests) <= set(QUESTS), "Save refers to an unknown quest.")
    _require(all(status in ("active", "complete") for status in quests.values()),
             "Quest status must be active or complete.")
    progress = _object(data["progress"], "progress")
    valid_progress = {f"kill:{enemy_id}" for enemy_id in ENEMIES}
    valid_progress.update(f"explore:{place}" for place in LOCATIONS)
    _require(set(progress) <= valid_progress, "Save contains an unknown progress counter.")
    for key, value in progress.items():
        _integer(value, key)
    _require(data["ending"] is None or data["ending"] in ("restore", "release"),
             "Unknown ending.")
    journal = data["journal"]
    _require(type(journal) is list and len(journal) <= 50, "Journal must have at most 50 entries.")
    for entry in journal:
        _string(entry, "journal entry", 500)
    return GameState(player=player, location=location, day=day, steps=steps,
                     flags=flags, quests=quests, progress=progress, visited=visited,
                     harvest_day=harvest_day, ending=data["ending"], journal=list(journal))


def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise SaveError(f"Duplicate save field: {key}.")
        result[key] = value
    return result


def _read(path: Path) -> tuple[GameState, bytes]:
    try:
        with path.open("rb") as stream:
            raw = stream.read(MAX_SAVE_BYTES + 1)
        _require(len(raw) <= MAX_SAVE_BYTES, "Save file is too large.")
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_keys)
        return _decode(document), raw
    except SaveError:
        raise
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError) as exc:
        raise SaveError(f"Cannot read save {path}: {exc}") from exc


def load_game(path: str | Path) -> GameState:
    """Read without modifying the save or silently replacing a damaged file."""
    return _read(Path(path))[0]


def _atomic_write(path: Path, payload: bytes) -> None:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", prefix=f".{path.name}.",
                                         suffix=".tmp", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def save_game(state: GameState, path: str | Path) -> Path:
    """Validate first, retain the previous valid save as .bak, then replace atomically.

    An invalid existing save is never overwritten; callers can offer a different slot.
    Saves contain only game data, not executable Python objects or random generator state.
    """
    path = Path(path)
    try:
        data = asdict(state)
        data["flags"] = sorted(state.flags)
        data["visited"] = sorted(state.visited)
        document = {"version": SAVE_VERSION, "state": data}
        _decode(document)
        payload = (json.dumps(document, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        _require(len(payload) <= MAX_SAVE_BYTES, "Save file would be too large.")
        previous = None
        if path.exists():
            try:
                _, previous = _read(path)
            except SaveError as exc:
                raise SaveError(f"Existing save is unreadable; it was preserved. Choose another slot. {exc}") from exc
        path.parent.mkdir(parents=True, exist_ok=True)
        if previous is not None:
            _atomic_write(path.with_name(path.name + ".bak"), previous)
        _atomic_write(path, payload)
        return path
    except SaveError:
        raise
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError) as exc:
        raise SaveError(f"Cannot write save {path}: {exc}") from exc
