"""A small terminal front end for the expanded S.S.S.D adventure."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys
import textwrap
import time

from . import content
from .engine import Game, SEALS, SHOP_STOCK
from .model import GameState, Player
from .presentation import (
    COMBAT_ACTIONS, COMPACT_COMBAT_ACTIONS, LANDMARKS, PROPS,
    Illustration, cards, scene,
)
from .scene_art import LOCATION_ART, SCREEN_ART
from .sprites import COMPACT_ENEMY_ART, ITEM_ART, render_battle
from .storage import SaveError, load_game, save_game
from .world_map import render_world_map


def default_save_path() -> Path:
    """Keep the default slot beside the game, independent of the current folder."""
    return Path(__file__).resolve().parent.parent / ".saves" / "slot1.json"


def normalize_name(value: str) -> str:
    """Validate terminal-facing names before they enter a saved game."""
    if any(not char.isprintable() for char in value):
        raise ValueError("Names cannot contain control characters.")
    name = value.strip() or "Xehspfe"
    if len(name) > 32:
        raise ValueError("Keep your name to 32 characters or fewer.")
    return name


def parse_quantity(value: str) -> int:
    """Accept positive whole numbers without floats or negative purchases."""
    value = value.strip()
    if not value.isdecimal():
        raise ValueError("Enter a positive whole number.")
    quantity = int(value)
    if not 1 <= quantity <= 99:
        raise ValueError("Choose a quantity from 1 to 99.")
    return quantity


def item_name(item_id: str | None) -> str:
    if item_id is None:
        return "Empty"
    return content.ITEMS.get(item_id, {}).get("name", item_id.replace("_", " "))


class Console:
    """Plain text works in pipes; an interactive terminal may clear between menus."""

    def __init__(self, input_fn=None, output=None, *, clear=True, visual=True):
        self.input_fn = input_fn if input_fn is not None else input
        self.output = output if output is not None else sys.stdout
        self.clear_enabled = clear
        self.visual = visual
        self.rows = 0
        self.input_echoes = (input_fn is None and not getattr(sys.stdin, "closed", True)
                             and sys.stdin.isatty())

    @property
    def width(self) -> int:
        return max(20, min(78, shutil.get_terminal_size((80, 24)).columns - 2))

    @property
    def height(self) -> int:
        return max(12, shutil.get_terminal_size((80, 24)).lines)

    def write(self, text="", *, indent=0):
        prefix = " " * indent
        for line in str(text).split("\n"):
            wrapped = textwrap.wrap(
                line, width=self.width, initial_indent=prefix,
                subsequent_indent=prefix, replace_whitespace=False,
            )
            print("\n".join(wrapped) if wrapped else "", file=self.output)
            self.rows += len(wrapped) or 1

    def lines(self, messages):
        for message in messages:
            self.write(message)

    def rule(self):
        self.write("-" * self.width)

    def art(self, text):
        lines = [line.rstrip() for line in text.strip("\n").splitlines()]
        if self.visual and all(len(line) <= self.width for line in lines):
            print("\n".join(lines), file=self.output)
            self.rows += len(lines)

    def gallery(self, entries):
        return cards(entries, self.width, self.height,
                     max_lines=self.height - self.rows - 4)

    def clear(self):
        self.rows = 0
        if (self.clear_enabled and self.output.isatty() and self.input_echoes
                and os.environ.get("TERM") != "dumb"):
            print("\033[2J\033[H", end="", file=self.output)

    def read(self, prompt="> ", *, strip=True) -> str:
        print(prompt, end="", file=self.output, flush=True)
        value = self.input_fn("")
        if not self.input_echoes:
            # Piped input does not echo its newline as an interactive terminal does.
            print(file=self.output)
        self.rows += 1
        return value.strip() if strip else value

    def pause(self):
        self.read("\n[Enter] Continue ")

    def choose(self, options, *, back="Back", illustration=None) -> str:
        """Read an existing numeric option; invalid input never escapes the menu."""
        options = [(str(key), label) for key, label in options]
        valid = {str(key) for key, _ in options} | {"0"}
        visual = illustration if self.visual else None
        if visual and not visual.keys <= valid:
            raise ValueError("An illustration advertises a missing menu option.")
        if visual and any(len(line) > self.width for page in visual.pages for line in page.splitlines()):
            visual = None  # Resizing must never hide the available choices.
        page = 0

        def display():
            if visual:
                self.art(visual.pages[page])
            for key, label in options:
                if not visual or key not in visual.keys:
                    self.write(f"[{key}] {label}")
            if visual and len(visual.pages) > 1:
                self.write(f"Page {page + 1}/{len(visual.pages)} | [<] Previous | [>] Next")
            self.write(f"[0] {back}" + (" | [?] Explain choices" if visual else ""))

        display()
        while True:
            answer = self.read()
            if answer in valid:
                return answer
            if visual and answer == "?":
                for key, label in options:
                    self.write(f"[{key}] {label}")
                self.write(f"[0] {back}")
                continue
            if visual and answer in {"<", ">"} and len(visual.pages) > 1:
                page = (page + (1 if answer == ">" else -1)) % len(visual.pages)
                display()
                continue
            self.write("Choose one of the numbers above.")


class GameCLI:
    def __init__(self, console: Console, save_path: Path, *, seed=None):
        self.console = console
        self.save_path = Path(save_path).expanduser()
        self.seed = seed
        self.game: Game | None = None
        self.has_checkpoint = False

    def active_battle(self) -> bool:
        return (self.game is not None and self.game.battle is not None
                and not self.game.battle.finished)

    def save(self, *, announce=False) -> bool:
        """An encounter is deliberately excluded from persisted state."""
        if self.game is None or self.active_battle():
            return False
        try:
            save_game(self.game.state, self.save_path)
        except (SaveError, OSError) as exc:
            self.console.write(f"Could not save: {exc}")
            self.console.write("You can keep playing, but this progress has not been saved.")
            return False
        self.has_checkpoint = True
        if announce:
            self.console.write(f"Checkpoint saved: {self.save_path}")
        return True

    def heading(self, title):
        self.console.clear()
        self.console.rule()
        self.console.write(title)
        if self.game is not None:
            player = self.game.player
            self.console.write(
                f"{player.name} | Lv {player.level} | "
                f"HP {player.hp}/{player.max_hp} | "
                f"Energy {player.energy}/{player.max_energy} | {player.gold} gold"
            )
        self.console.rule()

    def illustrated_menu(self, name, choices, *, back="Back"):
        """Keep dispatch, help text and drawing hotspots on the same numbered keys."""
        picture = scene(SCREEN_ART.get(name, ""),
                        {token: key for token, key, _ in choices}, self.console.width)
        if picture is None:
            picture = self.console.gallery([(key, label, PROPS.get(token, PROPS["character"]))
                                            for token, key, label in choices])
        return self.console.choose([(key, label) for _, key, label in choices],
                                   back=back, illustration=picture)

    def vignette(self, name, fallback="journal"):
        picture = scene(SCREEN_ART.get(name, ""), {}, self.console.width)
        self.console.art(picture.pages[0] if picture else PROPS[fallback])

    def item_gallery(self, options, item_ids):
        """The key sits on the same shelf/card as the object it selects."""
        return self.console.gallery([(key, label, ITEM_ART[item])
                                     for (key, label), item in zip(options, item_ids)])

    def perform(self, action, *args, pause=True):
        battle = self.game.battle if action == self.game.combat else None
        messages = action(*args)
        self.console.write()
        if action == self.game.rest:
            self.vignette("rest", "rest")
        elif battle and battle.result in {"victory", "defeat"}:
            self.vignette(battle.result, "character")
        self.console.lines(messages)
        if not self.active_battle():
            self.save()
        if pause:
            self.console.pause()
        return messages

    def main_menu(self) -> int:
        while True:
            self.heading("S.S.S.D | THE WARDS OF ASSONANCE")
            self.console.write("An expanded adventure, grown from the original terminal RPG.")
            choice = self.illustrated_menu("title", [
                ("new", "1", "New adventure"), ("continue", "2", "Continue from checkpoint"),
            ], back="Quit")
            if choice == "0":
                return 0
            if choice == "1":
                if not self.new_game():
                    continue
            else:
                if not self.continue_game():
                    continue
            self.adventure()
            self.game = None

    def new_game(self) -> bool:
        archive_damaged = False
        if self.save_path.exists():
            self.console.write(f"A checkpoint already exists at {self.save_path}.")
            self.console.write("Starting again will replace it. A valid save is backed up; a damaged file is archived.")
            if self.console.read("Type YES to replace it, or Enter to cancel: ") != "YES":
                return False
            try:
                load_game(self.save_path)
            except SaveError:
                if not self.save_path.is_file():
                    self.console.write("The save path is not a readable game file. Choose another path with --save.")
                    self.console.pause()
                    return False
                archive_damaged = True
        while True:
            try:
                name = normalize_name(self.console.read("Your name [Xehspfe]: ", strip=False))
                break
            except ValueError as exc:
                self.console.write(exc)
        if archive_damaged:
            archive = self.save_path.with_name(self.save_path.name + f".corrupt-{time.time_ns()}")
            try:
                self.save_path.rename(archive)
            except OSError as exc:
                self.console.write(f"Could not preserve the damaged file: {exc}")
                self.console.write("New game cancelled. Choose another path with --save.")
                self.console.pause()
                return False
            self.has_checkpoint = False
            self.console.write(f"Damaged save preserved at: {archive}")
            self.console.pause()
        self.game = Game(GameState(player=Player(name=name)), seed=self.seed)
        self.heading("A beginning, somewhere in the sand")
        self.vignette("prologue", "travel")
        self.console.lines(content.PROLOGUE)
        self.save()
        self.console.write("Tip: the journal keeps your next story objective and quest progress.")
        self.console.pause()
        return True

    def continue_game(self) -> bool:
        try:
            state = load_game(self.save_path)
        except (SaveError, OSError) as exc:
            self.console.write(f"Could not continue: {exc}")
            self.console.write("The existing file has been left untouched.")
            backup = self.save_path.with_name(self.save_path.name + ".bak")
            if backup.exists():
                self.console.write(f"A backup exists at {backup}. Use --save with that path to try it.")
            self.console.write("New adventure preserves a damaged file before replacing the slot.")
            self.console.pause()
            return False
        self.game = Game(state, seed=self.seed)
        self.has_checkpoint = True
        return True

    def adventure(self):
        while True:
            state = self.game.state
            location = content.LOCATIONS[state.location]
            self.heading(f"{location['name']} | Day {state.day}")
            self.console.write(location["description"])
            if self.game.player.stat_points:
                self.console.write(f"You have {self.game.player.stat_points} attribute points to spend.")
            if state.location == "village":
                actions = [
                    ("locals", "Talk to the locals", self.locals),
                    ("quests", "Quest board", self.quest_board),
                    ("shop", "Jimmy's shop", self.shop),
                    ("smith", "The smith's workshop", self.workshop),
                    ("rest", "Rest at the inn (free; next day)", lambda: self.perform(self.game.rest)),
                ]
            elif state.location == "farm":
                actions = [
                    ("harvest", "Harvest the farm", lambda: self.perform(self.game.harvest)),
                    ("rest", "Rest at the farm (free; next day)", lambda: self.perform(self.game.rest)),
                    ("farmer", "Talk to the farmer", lambda: self.perform(self.game.talk, "farmer")),
                ]
            else:
                actions = [("explore", "Explore the area", lambda: self.encounter(self.game.explore))]
                if location.get("boss"):
                    actions.append(("challenge", "Challenge the guardian", lambda: self.encounter(self.game.challenge)))
                actions.append(("rest", "Make camp (partial recovery; next day)", lambda: self.perform(self.game.rest)))
            if state.location == "castle" and "finale_ready" in state.flags and state.ending is None:
                actions.append(("ending", "Decide the fate of the old magic", self.ending))
            actions += [
                ("travel", "Travel / world map", self.travel),
                ("inventory", "Inventory & equipment", self.inventory),
                ("character", "Character & training", self.character),
                ("journal", "Journal / next objective", self.journal),
            ]
            keys = {token: str(index) for index, (token, _, _) in enumerate(actions, 1)}
            picture = scene(LOCATION_ART[state.location], keys, self.console.width)
            if picture:
                # Carried objects stay below the landscape; exits belong in it.
                toolbar = (f" .--. [{keys['inventory']}] Pack    o [{keys['character']}] Train"
                           f"    __/__ [{keys['journal']}] Journal\n"
                           " |__|              /|\\             |__|__|")
                if "ending" in keys:
                    toolbar += f"\n    \\ * / [{keys['ending']}] Decide the fate of the old magic"
                carried = {keys[token] for token in ("inventory", "character", "journal", "ending")
                           if token in keys}
                picture = Illustration((picture.pages[0] + "\n" + toolbar,),
                                       picture.keys | carried)
            else:
                picture = self.console.gallery([(keys[token], label, PROPS[token])
                                                for token, label, _ in actions])
            choice = self.console.choose(
                [(str(index), label) for index, (_, label, _) in enumerate(actions, 1)],
                back="Save & return to title", illustration=picture,
            )
            if choice == "0":
                if self.save(announce=True):
                    self.console.pause()
                    return
                self.console.write("Your adventure is still open. Progress is kept here while you continue playing.")
                self.console.pause()
                continue
            actions[int(choice) - 1][2]()

    def encounter(self, action):
        self.save()
        self.perform(action, pause=False)
        if self.active_battle():
            self.console.pause()
            self.combat()
        else:
            self.console.pause()

    def combat(self):
        actions = [
            ("1", "Attack", "attack"),
            ("2", "Power strike (-3 energy)", "power"),
            ("3", "Guard (+3 energy)", "guard"),
            ("4", "Mend (-4 energy)", "mend"),
            ("5", "Drink potion", "potion"),
            ("6", "Use antidote", "antidote"),
        ]
        while self.active_battle():
            battle = self.game.battle
            self.heading(f"BATTLE | {battle.enemy['name']} | Turn {battle.turn + 1}")
            self.console.write(f"Enemy HP: {battle.enemy_hp}/{battle.enemy['hp']}")
            self.console.write(f"Next move: {battle.intent}")
            if battle.enemy_guarding:
                self.console.write("The enemy is guarding now: your next strike will deal less damage.")
            if getattr(battle, "poison_turns", 0):
                self.console.write(f"Poisoned: {battle.poison_turns} turns remaining. An antidote can help.")
            self.console.write(
                f"Supplies: {self.game.player.inventory.get('potion', 0)} potions, "
                f"{self.game.player.inventory.get('antidote', 0)} antidotes"
            )
            keys = {command: key for key, _, command in actions}
            picture = scene(COMBAT_ACTIONS, keys, self.console.width)
            if picture is not None and self.console.height - self.console.rows >= 13:
                self.console.art(render_battle(battle.enemy_id, self.console.width))
            else:
                self.console.art(COMPACT_ENEMY_ART[battle.enemy_id])
                picture = scene(COMPACT_COMBAT_ACTIONS, keys, self.console.width)
            if picture is None:
                # Very narrow displays keep every combat action on one page.
                picture = Illustration(("\n".join(
                    f"{icon} [{key}] {label}" for icon, key, label in (
                        ("/", "1", "Attack"), ("/*", "2", "Power -3E"),
                        ("O", "3", "Guard +3E"), ("+", "4", "Mend -4E"),
                        ("(+)", "5", "Potion"), ("(x)", "6", "Antidote"))),),
                    frozenset(keys.values()))
            choice = self.console.choose(
                [(key, label) for key, label, _ in actions], back="Try to flee",
                illustration=picture,
            )
            command = "flee" if choice == "0" else actions[int(choice) - 1][2]
            self.perform(self.game.combat, command)

    def travel(self):
        self.heading("WORLD MAP")
        state = self.game.state
        here = content.LOCATIONS[state.location]
        self.console.write(f"You are at {here['name']}. Numbers mark roads from here.")
        neighbors = list(here["neighbors"])
        options = []
        for index, location_id in enumerate(neighbors, 1):
            place = content.LOCATIONS[location_id]
            visited = "visited" if location_id in state.visited else "unexplored"
            locked = " | LOCKED: needs all three seals" if location_id == "castle" and not set(SEALS) <= state.flags else ""
            options.append((str(index), f"{place['name']} | level {place.get('level', 1)} | {visited}{locked}"))
        keys = {location: str(index) for index, location in enumerate(neighbors, 1)}
        drawing = render_world_map(state.location, keys, self.console.width,
                                   sealed=set(SEALS) <= state.flags)
        if drawing:
            self.console.write("[@] You are here | [.] Distant | [#]/LOCK Needs three seals")
            picture = Illustration((drawing,), frozenset(keys.values()))
        else:
            # Small screens keep the reachable destinations and their landmarks.
            picture = self.console.gallery([(key, label, LANDMARKS[location])
                                            for (key, label), location in zip(options, neighbors)])
        choice = self.console.choose(options, illustration=picture)
        if choice != "0":
            self.perform(self.game.move, neighbors[int(choice) - 1])

    def locals(self):
        while True:
            self.heading("THE LOCALS")
            people = [("kieth", "Kieth - rumors and the road ahead"),
                      ("jimmy", "Jimmy - supplies and questionable advice"),
                      ("smith", "The smith - steel, recipes and upgrades")]
            choice = self.illustrated_menu("locals", [(npc, str(i), label)
                                                      for i, (npc, label) in enumerate(people, 1)])
            if choice == "0":
                return
            self.perform(self.game.talk, people[int(choice) - 1][0])

    def quest_board(self):
        while True:
            self.heading("THE VILLAGE QUEST BOARD")
            quest_ids = list(content.QUESTS)
            options = [
                (str(i), f"{content.QUESTS[qid]['name']} [{self.game.state.quests.get(qid, 'available')}]")
                for i, qid in enumerate(quest_ids, 1)
            ]
            notices = self.console.gallery([(key, label, " .----.\n | !? |\n '----'")
                                           for key, label in options])
            choice = self.console.choose(options, illustration=notices)
            if choice == "0":
                return
            qid = quest_ids[int(choice) - 1]
            quest = content.QUESTS[qid]
            self.heading(quest["name"])
            self.console.art(PROPS["quests"])
            self.console.write(f"Posted by: {quest.get('giver', 'the village')}")
            self.console.write(quest["description"])
            self.describe_objectives(quest)
            reward = quest.get("reward", {})
            reward_parts = []
            if isinstance(reward, dict):
                for key in ("gold", "xp"):
                    if reward.get(key):
                        reward_parts.append(f"{reward[key]} {key}")
                for item, count in reward.get("items", {}).items():
                    reward_parts.append(f"{item_name(item)} x{count}")
            if reward_parts:
                self.console.write("Reward: " + ", ".join(reward_parts))
            status = self.game.state.quests.get(qid)
            if status == "complete":
                self.console.write("Completed. The village remembers.")
                self.console.pause()
            else:
                action = self.game.claim_quest if status == "active" else self.game.accept_quest
                label = "Claim reward" if status == "active" else "Accept quest"
                if self.console.choose([("1", label)]) == "1":
                    self.perform(action, qid)

    def describe_objectives(self, quest):
        objectives = quest.get("objectives", {})
        if isinstance(objectives, dict):
            for key, total in objectives.items():
                kind, target = key.split(":", 1)
                catalog = content.ITEMS if kind == "own" else content.ENEMIES if kind == "kill" else content.LOCATIONS
                label = f"{kind.title()} {catalog[target]['name']}"
                current = self.game.objective_progress(key)
                self.console.write(f"  {label}: {min(current, total)}/{total}")
        else:
            for objective in objectives:
                self.console.write(f"  {objective}")

    def quantity(self) -> int | None:
        while True:
            value = self.console.read("Quantity 1-99 [1], or 0 to cancel: ")
            if value == "0":
                return None
            try:
                return parse_quantity(value or "1")
            except ValueError as exc:
                self.console.write(exc)

    def shop(self):
        while True:
            self.heading("JIMMY'S SHOP")
            choice = self.illustrated_menu("shop", [("buy", "1", "Buy supplies or equipment"),
                                                    ("sell", "2", "Sell items")])
            if choice == "0":
                return
            buying = choice == "1"
            self.heading("JIMMY'S SHELVES | BUY" if buying else "YOUR ITEMS | SELL")
            stock = list(SHOP_STOCK) if buying else list(self.game.player.inventory)
            if not stock:
                self.console.write("Your bag is empty.")
                self.console.pause()
                continue
            options = []
            for index, item in enumerate(stock, 1):
                info = content.ITEMS[item]
                price = info["price"] if buying else max(1, info["price"] // 2)
                owned = self.game.player.inventory.get(item, 0)
                options.append((str(index), f"{info['name']}\n{price} gold each | own {owned}"))
            item_choice = self.console.choose(options, illustration=self.item_gallery(options, stock))
            if item_choice == "0":
                continue
            item_id = stock[int(item_choice) - 1]
            info = content.ITEMS[item_id]
            price = info["price"] if buying else max(1, info["price"] // 2)
            self.heading(("BUY | " if buying else "SELL | ") + item_name(item_id))
            self.console.art(ITEM_ART[item_id])
            self.console.write(f"{price} gold each | own {self.game.player.inventory.get(item_id, 0)}")
            self.console.write(info.get("description", ""))
            quantity = self.quantity()
            if quantity is not None:
                self.perform(self.game.buy if buying else self.game.sell, item_id, quantity)

    def inventory(self):
        while True:
            self.heading("INVENTORY & EQUIPMENT")
            player = self.game.player
            for slot, item in player.equipment.items():
                tier = player.upgrades.get(item, 0)
                suffix = f" +{tier}" if tier else ""
                self.console.write(f"{slot.title()}: {item_name(item)}{suffix}")
            items = list(player.inventory)
            options = [
                (str(i), f"{item_name(item)} x{player.inventory[item]}")
                for i, item in enumerate(items, 1)
            ]
            options.append((str(len(items) + 1), "Unequip an item"))
            choice = self.console.choose(options, illustration=self.item_gallery(options[:-1], items))
            if choice == "0":
                return
            if int(choice) == len(items) + 1:
                slots = [(slot, item) for slot, item in player.equipment.items() if item]
                if not slots:
                    self.console.write("You have no equipment to remove.")
                    self.console.pause()
                    continue
                self.heading("REMOVE EQUIPMENT")
                slot_options = [
                    (str(i), f"{slot.title()}: {item_name(item)}")
                    for i, (slot, item) in enumerate(slots, 1)
                ]
                selection = self.console.choose(slot_options, illustration=self.item_gallery(
                    slot_options, [item for _, item in slots]))
                if selection != "0":
                    self.perform(self.game.equip, "unequip:" + slots[int(selection) - 1][0])
                continue
            item = items[int(choice) - 1]
            info = content.ITEMS[item]
            self.heading(info["name"])
            self.console.art(ITEM_ART[item])
            self.console.write(info.get("description", ""))
            stats = [f"{key} +{info[key]}" for key in ("attack", "defense", "hp", "energy") if info.get(key)]
            if stats:
                self.console.write(" / ".join(stats))
            if info.get("slot"):
                if self.console.choose([("1", "Equip")]) == "1":
                    self.perform(self.game.equip, item)
            elif item in {"potion", "antidote"}:
                if self.console.choose([("1", "Use")]) == "1":
                    self.perform(self.game.use, item)
            else:
                self.console.write("A crafting material or keepsake. Recipes are at the village smith.")
                self.console.pause()

    def character(self):
        while True:
            self.heading("CHARACTER & TRAINING")
            player = self.game.player
            self.console.write(f"Experience: {player.xp}/{player.xp_to_next}")
            self.console.write(f"Attack {player.attack} | Defense {player.defense} | Critical chance {player.crit:.0%}")
            self.console.write(f"Strength {player.strength} | Vitality {player.vitality} | Agility {player.agility}")
            self.console.write(f"Unspent points: {player.stat_points}")
            self.console.write("Leveling raises all attributes and restores your health and energy.")
            choice = self.illustrated_menu("character", [
                ("strength", "1", "Train strength (more damage)"),
                ("vitality", "2", "Train vitality (health and defense)"),
                ("agility", "3", "Train agility (energy and critical chance)"),
            ])
            if choice == "0":
                return
            self.perform(self.game.train, ("strength", "vitality", "agility")[int(choice) - 1])

    def workshop(self):
        while True:
            self.heading("THE SMITH'S WORKSHOP")
            choice = self.illustrated_menu("workshop", [("craft", "1", "Craft equipment and supplies"),
                                                       ("upgrade", "2", "Upgrade a weapon or armor")])
            if choice == "0":
                return
            if choice == "1":
                self.crafting()
            else:
                self.upgrading()

    def crafting(self):
        recipes = list(content.RECIPES)
        self.heading("CRAFTING RECIPES")
        options = [
            (str(i), content.RECIPES[recipe]["name"])
            for i, recipe in enumerate(recipes, 1)
        ]
        choice = self.console.choose(options, illustration=self.item_gallery(
            options, [content.RECIPES[recipe]["produces"] for recipe in recipes]))
        if choice == "0":
            return
        recipe_id = recipes[int(choice) - 1]
        recipe = content.RECIPES[recipe_id]
        self.heading("AT THE ANVIL | " + recipe["name"])
        self.console.art(ITEM_ART[recipe["produces"]])
        self.console.write(f"Makes: {item_name(recipe['produces'])} x{recipe.get('quantity', 1)}")
        self.console.write(f"Smith's fee: {recipe.get('gold', 0)} gold")
        for item, quantity in recipe["ingredients"].items():
            count = self.game.player.inventory.get(item, 0)
            self.console.write(f"  {item_name(item)}: need {quantity}, own {count}")
        self.console.write("Ingredients are consumed. Unequip any gear you want to use as a material.")
        if self.console.choose([("1", "Craft this recipe")]) == "1":
            self.perform(self.game.craft, recipe_id)

    def upgrading(self):
        self.heading("EQUIPMENT UPGRADES")
        player = self.game.player
        candidates = [item for item in player.inventory if content.ITEMS[item].get("slot") in {"weapon", "armor"}]
        if not candidates:
            self.console.write("Bring a weapon or a piece of armor to the smith.")
            self.console.pause()
            return
        options = [
            (str(i), f"{item_name(item)} +{player.upgrades.get(item, 0)}")
            for i, item in enumerate(candidates, 1)
        ]
        choice = self.console.choose(options, illustration=self.item_gallery(options, candidates))
        if choice == "0":
            return
        item = candidates[int(choice) - 1]
        self.heading("UPGRADE | " + item_name(item))
        self.console.art(ITEM_ART[item])
        tier = player.upgrades.get(item, 0) + 1
        if tier > 3:
            self.console.write("This item is already at the maximum upgrade, +3.")
            self.console.pause()
            return
        cost = f"{tier * 20} gold and {tier} ore"
        if tier >= 2:
            cost += " and 1 crystal"
        self.console.write(f"Upgrade to +{tier}: {cost}.")
        self.console.write("Weapon upgrades add 2 attack; armor upgrades add 1 defense.")
        if self.console.choose([("1", "Upgrade")]) == "1":
            self.perform(self.game.upgrade, item)

    def journal(self):
        self.heading("JOURNAL | THE ROAD AHEAD")
        self.vignette("journal")
        self.console.lines(self.game.journal())
        self.console.pause()

    def ending(self):
        self.heading("THE OLD MAGIC IS LISTENING")
        self.console.write("The last guardian has fallen. The choice belongs to you.")
        self.console.write("Restore the old magic, or release it. Either path lets you keep exploring afterward.")
        choice = self.illustrated_menu("ending", [("restore", "1", "Restore the old magic"),
                                                ("release", "2", "Release the old magic")])
        if choice != "0":
            self.perform(self.game.finish, "restore" if choice == "1" else "release")

    def farewell(self):
        self.console.write()
        if self.active_battle():
            self.console.write("The encounter was interrupted. Partial combat has not been saved.")
        if self.has_checkpoint:
            self.console.write("Goodbye. Continue resumes your latest successful checkpoint.")
        else:
            self.console.write("Goodbye. No checkpoint was loaded or saved this session.")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Play the expanded S.S.S.D terminal adventure.")
    parser.add_argument("--save", type=Path, default=default_save_path(), help="checkpoint file (default: .saves/slot1.json beside the game)")
    parser.add_argument("--seed", type=int, help="seed the adventure's random number generator")
    parser.add_argument("--plain", action="store_true", help="use text lists without ASCII illustrations")
    args = parser.parse_args(argv)
    cli = GameCLI(Console(visual=not args.plain), args.save, seed=args.seed)
    try:
        result = cli.main_menu()
    except (EOFError, KeyboardInterrupt):
        cli.farewell()
        return 0
    cli.farewell()
    return result


if __name__ == "__main__":
    raise SystemExit(main())
