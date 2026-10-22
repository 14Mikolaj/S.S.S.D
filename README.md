# S.S.S.D

A Python terminal RPG I made before starting university. It has ASCII maps,
turn-based battles, equipment, character stats, and quests.

There are two versions:

- [`main`](https://github.com/14Mikolaj/S.S.S.D/tree/main) is the original project,
  kept as a time capsule.
- [`playable`](https://github.com/14Mikolaj/S.S.S.D/tree/playable) fixes the bugs
  that got in the way of playing it on modern Python, keeping the old artwork,
  story, and game structure.

## Run

Use Python 3; this branch has been tested with Python 3.14. The main game only
uses the standard library, so there are no packages to install.

From the project directory:

```sh
git switch playable
python main_.py
```

Press Enter through the opening screens, then type the numbers shown in the
menus. Use a wide terminal with a small monospace font and Unicode support;
the world map needs about 200 columns. Enter `q` at the world map to quit,
or press Ctrl+C at any time.

The village and desert are playable. The farm and other unfinished destinations
show a message and return you to the map. There is no save system.

To revisit the original version, run `git switch main`.

## Fixes on this branch

- Coyote quest completion and cactus defeat no longer crash.
- Defeated enemies cannot retaliate; resurrection returns to the world map.
- Potions consume one item and heal the advertised 25% of maximum HP. Empty
  inventories cannot produce negative item counts.
- Shop quantities are validated before purchase.
- Equipment bonuses no longer stack when re-equipped, and base stats stay
  separate from equipment bonuses. Equipping armour does not heal you for free.
- Level-ups retain leftover experience.
- ASCII-art strings compile without invalid-escape warnings, preserving their
  displayed contents.

Run the regression tests with:

```sh
python -B -W error::SyntaxWarning -m unittest discover -s tests -v
```

## Files

- `main_.py` — main game.
- `SSSDpak/` — maps, battle displays, and game helpers.
- `main_Retro_Retro.py` — an older version, kept unchanged for reference. It
  still has Windows-specific audio imports and old string warnings; use
  `main_.py` to play.
- `Cheat Codes.txt` — original in-game cheat notes, saved in UTF-16.
- `tests/` — scripted gameplay regression checks using Python's standard library.

Python caches, Windows shortcuts, and launchers tied to old local paths are
excluded from Git. The original music files are also excluded: no music
license or attribution was included with the project. The main game runs
without them.
