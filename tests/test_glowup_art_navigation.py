"""Exercise displayed hotspots through actual CLI navigation and game rules."""

from collections import deque
import copy
from io import StringIO
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from sssd.cli import Console, GameCLI, main
from sssd.combat import Battle
from sssd.content import ENEMIES, LOCATIONS
from sssd.engine import Game, SEALS
from sssd.storage import load_game, save_game


class ArtNavigationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="sssd-art-navigation-")
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "slot.json"

    def cli(self, read, output, *, location="village", visual=True, unlocked=False):
        cli = GameCLI(Console(read, output, clear=False, visual=visual), self.path, seed=11)
        cli.game = Game(seed=11)
        cli.game.state.location = location
        cli.game.state.visited.add(location)
        if unlocked or location == "castle":
            cli.game.state.flags.update(SEALS)
        return cli

    def travel_to_displayed_destination(self, origin, destination, *, visual, unlocked,
                                       expected_key=None):
        output = StringIO()
        calls = 0
        selected = None

        def read(_prompt):
            nonlocal calls, selected
            calls += 1
            if calls == 1:
                text = output.getvalue()
                if visual:
                    match = re.search(re.escape(destination.upper()) + r"\[(\d+)\]", text)
                    self.assertIsNotNone(match, f"No visible hotspot for {destination}:\n{text}")
                    selected = match[1]
                else:
                    selected = expected_key
                    full_label = LOCATIONS[destination]["name"]
                    self.assertIn(f"[{selected}] {full_label}", text)
                    self.assertNotIn("TRAVELLER'S ATLAS", text)
                    self.assertNotIn(destination.upper() + "[", text)
                return selected
            if calls == 2:
                return ""  # Actual travel action's result/continue prompt.
            self.fail("Travel unexpectedly requested another input.")

        cli = self.cli(read, output, location=origin, visual=visual, unlocked=unlocked)
        with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((80, 24))):
            with patch.object(cli.game, "move", wraps=cli.game.move) as move:
                cli.travel()
        move.assert_called_once_with(destination)
        self.assertEqual(2, calls)
        locked = destination == "castle" and not unlocked
        self.assertEqual(origin if locked else destination, cli.game.state.location)
        self.assertEqual(0 if locked else 1, cli.game.state.steps)
        if locked:
            self.assertIn("castle gate is sealed", output.getvalue())
        self.assertEqual(cli.game.state, load_game(self.path))
        return selected

    def test_every_road_uses_the_displayed_key_in_art_and_plain_modes(self):
        for origin, place in LOCATIONS.items():
            for destination in place["neighbors"]:
                unlock_cases = (False, True) if destination == "castle" else (False,)
                for unlocked in unlock_cases:
                    with self.subTest(origin=origin, destination=destination, unlocked=unlocked):
                        key = self.travel_to_displayed_destination(
                            origin, destination, visual=True, unlocked=unlocked)
                        self.travel_to_displayed_destination(
                            origin, destination, visual=False, unlocked=unlocked, expected_key=key)

    def test_each_location_advertises_every_available_action(self):
        common = {"Travel / world map", "Inventory & equipment",
                  "Character & training", "Journal / next objective"}
        for location in LOCATIONS:
            for finale_ready in ((False, True) if location == "castle" else (False,)):
                with self.subTest(location=location, finale_ready=finale_ready):
                    output = StringIO()

                    def stop_at_prompt(_prompt):
                        raise EOFError

                    cli = self.cli(stop_at_prompt, output, location=location)
                    if finale_ready:
                        cli.game.state.flags.add("finale_ready")
                    before = copy.deepcopy(cli.game.state)
                    with patch("sssd.cli.shutil.get_terminal_size",
                               return_value=os.terminal_size((80, 24))):
                        with patch.object(cli.console, "choose", wraps=cli.console.choose) as choose:
                            with self.assertRaises(EOFError):
                                cli.adventure()
                    options = choose.call_args.args[0]
                    keys = {str(key) for key, _ in options}
                    labels = {label for _, label in options}
                    shown_keys = set(re.findall(r"\[(\d+)\]", output.getvalue()))
                    self.assertEqual(keys | {"0"}, shown_keys)
                    self.assertTrue(common <= labels)
                    if location == "village":
                        self.assertTrue({"Talk to the locals", "Quest board", "Jimmy's shop",
                                         "The smith's workshop"} <= labels)
                    elif location == "farm":
                        self.assertTrue({"Harvest the farm", "Talk to the farmer"} <= labels)
                    else:
                        self.assertIn("Explore the area", labels)
                        self.assertEqual(bool(LOCATIONS[location].get("boss")),
                                         "Challenge the guardian" in labels)
                    self.assertEqual(finale_ready, "Decide the fate of the old magic" in labels)
                    self.assertEqual(before, cli.game.state)

    def test_castle_finale_shifts_the_visible_road_key_and_dispatch_together(self):
        road_keys = []
        for finale_ready in (False, True):
            output = StringIO()
            calls = 0

            def read(_prompt):
                nonlocal calls
                calls += 1
                if calls == 1:
                    match = re.search(r"\[(\d+)\]\s+Road", output.getvalue())
                    self.assertIsNotNone(match, "Castle scenery must advertise its actual exit.")
                    road_keys.append(int(match[1]))
                    return match[1]
                if calls == 2:
                    self.assertIn("WORLD MAP", output.getvalue())
                    self.assertIn("BRIDGE[1]", output.getvalue())
                    return "0"
                raise EOFError

            cli = self.cli(read, output, location="castle")
            if finale_ready:
                cli.game.state.flags.add("finale_ready")
            before = copy.deepcopy(cli.game.state)
            with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((80, 24))):
                with self.assertRaises(EOFError):
                    cli.adventure()
            self.assertEqual(3, calls)
            self.assertEqual(before, cli.game.state)
            self.assertEqual(finale_ready, "Decide the fate of the old magic" in output.getvalue())
        self.assertEqual(road_keys[0] + 1, road_keys[1])

    def test_narrow_map_pages_help_and_back_preserve_state_and_checkpoint(self):
        pending = deque([">", "<", "?", "0"])
        output = StringIO()
        screens = []

        def read(_prompt):
            self.assertEqual(before, cli.game.state)
            self.assertEqual(saved_bytes, self.path.read_bytes())
            screens.append(output.getvalue())
            self.assertTrue(pending, "Unexpected extra narrow-map prompt.")
            return pending.popleft()

        cli = self.cli(read, output)
        save_game(cli.game.state, self.path)
        saved_bytes = self.path.read_bytes()
        before = copy.deepcopy(cli.game.state)
        with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((40, 24))):
            cli.travel()
        self.assertFalse(pending)
        self.assertIn("Page 1/", screens[0])
        self.assertIn("Page 2/", screens[1][len(screens[0]):])
        self.assertIn("Page 1/", screens[2][len(screens[1]):])
        help_text = " ".join(screens[3][len(screens[2]):].split())
        for key, destination in enumerate(LOCATIONS["village"]["neighbors"], 1):
            self.assertIn(f"[{key}] {LOCATIONS[destination]['name']}", help_text)
        self.assertNotIn("TRAVELLER'S ATLAS", output.getvalue())
        self.assertEqual(before, cli.game.state)
        self.assertEqual(saved_bytes, self.path.read_bytes())

    def test_paging_does_not_renumber_destinations(self):
        pending = deque([">", "1", ""])
        output = StringIO()

        def read(_prompt):
            self.assertTrue(pending, "Unexpected extra paged travel prompt.")
            return pending.popleft()

        cli = self.cli(read, output)
        with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((40, 24))):
            cli.travel()
        self.assertFalse(pending)
        self.assertIn("Page 2/", output.getvalue())
        self.assertEqual("farm", cli.game.state.location)
        self.assertEqual(1, cli.game.state.steps)

    def test_plain_command_line_flag_keeps_real_adventure_inputs(self):
        initial = Game().state
        save_game(initial, self.path)
        # Continue, village travel key, farm road key, continue, save/leave, title quit.
        answers = ["2", "6", "1", "", "0", "", "0"]
        with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((80, 24))):
            with patch("builtins.input", side_effect=answers):
                with patch("sys.stdout", new_callable=StringIO) as output:
                    self.assertEqual(0, main(["--plain", "--save", str(self.path)]))
        self.assertEqual("farm", load_game(self.path).location)
        self.assertNotIn("TRAVELLER'S ATLAS", output.getvalue())
        self.assertNotIn("[?] Explain choices", output.getvalue())
        self.assertIn("[6] Travel / world map", output.getvalue())
        self.assertIn("[1] The Extremely Normal Farm", output.getvalue())

    def test_battle_art_keeps_danger_and_actions_visible_at_the_prompt(self):
        for width in (80, 66, 40):
            for enemy in ENEMIES:
                with self.subTest(width=width, enemy=enemy):
                    output = StringIO()

                    def stop_at_prompt(_prompt):
                        raise EOFError

                    cli = self.cli(stop_at_prompt, output)
                    cli.game.battle = Battle(cli.game.player, enemy)
                    cli.game.battle.enemy_guarding = True
                    cli.game.battle.poison_turns = 3
                    with patch("sssd.cli.shutil.get_terminal_size",
                               return_value=os.terminal_size((width, 24))):
                        with self.assertRaises(EOFError):
                            cli.combat()
                    lines = output.getvalue().splitlines()
                    self.assertLessEqual(len(lines), 24, output.getvalue())
                    self.assertLessEqual(max(map(len, lines)), width - 2)
                    self.assertIn("Next move:", output.getvalue())
                    self.assertIn("Poisoned:", output.getvalue())
                    self.assertEqual({str(key) for key in range(7)},
                                     set(re.findall(r"\[(\d+)\]", output.getvalue())))


if __name__ == "__main__":
    unittest.main()
