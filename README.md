# S.S.S.D

A Python terminal RPG I made before starting university. It has ASCII maps,
turn-based battles, equipment, character stats, and quests.

This repository preserves the old project, including its unfinished parts and
rough edges. The original game code has been kept as-is.

## Run

Use Python 3. The main game only uses the standard library, so there are no
packages to install.

From the project directory:

```sh
python main_.py
```

Press Enter through the opening screens, then type the numbers shown in the
menus. Use a wide terminal with a small monospace font and Unicode support;
the maps are much wider than a typical terminal window. Press Ctrl+C to stop.

## Files

- `main_.py` — main game.
- `SSSDpak/` — maps, battle displays, and game helpers.
- `main_Retro_Retro.py` — an older version, kept for reference. It still has
  Windows-specific audio imports; use `main_.py` to play.
- `Cheat Codes.txt` — original in-game cheat notes, saved in UTF-16.

Python caches, Windows shortcuts, and launchers tied to old local paths are
excluded from Git. The original music files are also excluded: no music
license or attribution was included with the project. The main game runs
without them.

Some areas and menus are unfinished. Modern Python versions may also warn
about backslashes in the original ASCII art strings.
