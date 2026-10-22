# S.S.S.D — The Wards of Assonance

A Python terminal RPG I made before starting university, with a new expanded
edition on `ai_glowup`. The old ASCII fantasy, questionable jokes, living cacti,
and deeply unreasonable camel are still here. There is now a whole adventure
around them.

## Three versions

| Branch | What it contains |
| --- | --- |
| [`main`](https://github.com/14Mikolaj/S.S.S.D/tree/main) | The original project, kept as a time capsule. |
| [`playable`](https://github.com/14Mikolaj/S.S.S.D/tree/playable) | The classic game with bug fixes and modern Python support. |
| [`ai_glowup`](https://github.com/14Mikolaj/S.S.S.D/tree/ai_glowup) | This expanded edition, built with AI assistance on top of `playable`. |

The original and bug-fixed branches remain separate. The expanded edition also
keeps `main_.py` and `SSSDpak/` intact, so the classic game still runs here.

## Play

Use Python 3.10 or newer; development and tests use Python 3.14. No extra
packages, downloads, API keys, or AI service are needed to play.

From the project directory:

```sh
git switch ai_glowup
python play.py
```

Choose **New adventure**, enter a name (or press Enter for Xehspfe), and speak
with **Kieth** in the village. Your journal always shows the next story goal.

Menus use numbers. **0** goes back; in combat it attempts to flee. At the
location menu, **0** saves and returns to the title. Ctrl+C exits safely to the
last checkpoint.

The ASCII scenery is also the menu: choose the number beside a building, path,
camp, person, or guardian. On the world map, travel numbers appear **inside the
destination's landmark**. `@` marks your current location, `.` a distant region,
and `LOCK` a castle that still needs the three seals. Only neighboring places
have travel numbers; geographic proximity does not imply an additional road.

The original **173-column, 64-line island** returns on wide terminals, with
travel numbers updated for the current roads. Locations, buildings, equipment,
and creatures use larger illustrations too. Exploring a forest, speaking to
the farmer, making camp, harvesting, shopping, crafting, and other actions open
their own illustrated scenes with the actual dialogue and results.
Wide windows also reveal full shop, forge, inn, and training interiors, with
their choices placed beside the shelves, anvil, people, and exercise stations.

Use a large terminal for the full drawings: around **132 columns × 60 rows**
for the expanded locations and narrative scenes, or **180 × 75** for the whole
original island. There is no 78-column art limit. Smaller windows show alternate
layouts or let you view a large drawing in sections instead of shrinking it.
**`<` / `>`** move through scene views and shelf pages; all choice numbers work
from every view. Choices outside the current view are listed under **Elsewhere**.
At an action result, **Enter** continues and the view controls only inspect the
picture; they do not repeat the action. **`?`** explains menu choices. For text
lists without the artwork, run `python play.py --plain`.

Look closely at odd little landmarks for optional discoveries. Their extra
choices come after the familiar location options, so existing numbers stay the
same. At the farm, a particularly smug crow runs **Noughts and Crows**: choose
a numbered square to place X, then the crow plays O. Make three in a row; your
first win **or draw** earns 12 gold and two herbs. Games are free, **0** leaves
the table, and replays are for bragging rights. Discoveries and collected
prizes are saved; an unfinished board starts fresh next time.

## The adventure

David, the druid who raised you, disappeared into Thenttkil's living forest.
Now his old wards are failing. Follow their traces across ten connected places:
the village, farm, desert, caves, forest, shore, bridge, plains, mountains, and
castle. Find the three lost seals and decide what should become of the magic
David left behind.

- **A complete story and two endings**, with exploration available afterward.
- **Fourteen enemy types**, including three seal wardens, an optional storm
  drake, and the final boss.
- **Tactical combat:** visible enemy intentions, power attacks, guarding,
  energy, healing magic, poison, antidotes, and escape attempts.
- **Character growth:** levels, spare XP carried forward, and attributes you
  can train. Equipment bonuses are derived from what you actually wear.
- **Twenty items:** weapons, armour, charms, consumables, and crafting materials.
- **Six village jobs** with tracked objectives and rewards. Active jobs help
  you find relevant enemies instead of relying entirely on luck.
- **Crafting and upgrades:** six recipes, including a blade forged from a
  storm drake's scale, plus three upgrade tiers for weapons and armour.
- **Working farm and camps:** gather herbs once per day, rest for free in the
  village or farm, and recover partially at wilderness camps.
- **Five optional curiosities:** strange conversations, a woodland riddle,
  small keepsakes, and a crow with an inflated opinion of its board-game skills.

Death sends you back to the village, costing 10% of your gold. Equipment,
quest progress, and discoveries are kept. Levels restore health and energy.

Explore a guardian's region twice to find its refuge. Stronger equipment,
training, supplies, and paying attention to enemy intentions help when a fight
is too difficult. The mountain challenge is optional.

## Saves

The game automatically checkpoints outside combat to `.saves/slot1.json`.
The previous valid checkpoint is retained as `.saves/slot1.json.bak`. A fight
interrupted by Ctrl+C or a closed terminal returns to the checkpoint before
the encounter; unfinished battles are not saved.

Saving uses validated JSON and atomic replacement. Unreadable files are left
alone. Starting a new game over an existing slot asks for `YES`; damaged files
are preserved separately before a new slot is created. Saves and recovery
copies in `.saves/` are excluded from Git.

Use separate slots or a repeatable random seed if you want:

```sh
python play.py --save .saves/second-adventure.json
python play.py --seed 42
```

The seed controls a session's random choices; reloading does not preserve the
exact random-generator position. Classic-game sessions cannot be imported.

## Classic game

```sh
python main_.py
```

This launches the bug-fixed classic edition, which still needs a wide terminal
and has no save system. `main_Retro_Retro.py` is an unchanged historical variant
with Windows-specific audio imports. The original music and machine-specific
launchers remain excluded from Git.

## Development

The expanded edition separates world data, player state, combat, progression,
saves, and terminal menus under `sssd/`. Everything uses the standard library.

```sh
python -B -W error::SyntaxWarning -m unittest discover -s tests -v
```

Tests cover both the classic edition and the expansion: gameplay paths,
economy and inventory invariants, campaign completion, combat, save validation
and recovery, and terminal-menu flows.
