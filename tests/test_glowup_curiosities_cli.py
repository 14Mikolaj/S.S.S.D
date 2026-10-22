"""Play optional discoveries through their displayed controls and checkpoints."""

from collections import deque
from io import StringIO
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from sssd.cli import Console, GameCLI
from sssd.engine import Game
from sssd.storage import load_game


class CuriosityCLITests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="sssd-curiosity-cli-")
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "slot.json"

    def make_cli(self, answers, location="farm", visual=True):
        pending = deque(answers)
        frames = []

        def read(_):
            frames.append("\n".join(cli.console.frame))
            self.assertTrue(pending, "Unexpected input prompt: " + frames[-1])
            return pending.popleft()

        cli = GameCLI(Console(read, StringIO(), clear=False, visual=visual), self.path)
        cli.game = Game(seed=4)
        cli.game.state.location = location
        cli.game.state.visited.add(location)
        return cli, pending, frames

    def test_crow_board_legal_moves_and_saved_one_time_prize(self):
        for visual in (True, False):
            for columns, rows in ((80, 24), (132, 52)):
                with self.subTest(visual=visual, columns=columns):
                    # Occupied square 1 is rejected on the second turn. Then win.
                    cli, pending, frames = self.make_cli(["1", "1", "9", "7", "8", ""], visual=visual)
                    gold = cli.game.player.gold
                    herbs = cli.game.player.inventory.get("herb", 0)
                    with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((columns, rows))):
                        cli.crow_game()
                    self.assertFalse(pending)
                    self.assertEqual(gold + 12, cli.game.player.gold)
                    self.assertEqual(herbs + 2, cli.game.player.inventory["herb"])
                    self.assertEqual(1, cli.game.state.progress["crow:played"])
                    self.assertEqual(1, cli.game.state.progress["crow:won"])
                    self.assertEqual(cli.game.state, load_game(self.path))
                    self.assertIn("NOUGHTS AND CROWS | WIN", frames[-1])
                    # Before input errors add explanatory rows, the entire board
                    # and controls fit a short terminal, rather than hiding cells.
                    if visual:
                        self.assertLessEqual(len(frames[0].splitlines()) + 1, rows)
                        for key in range(1, 10):
                            self.assertIn(f"[{key}]", frames[0])
                    # A new CLI session and a repeated win retain the first prize.
                    replay, remaining, _ = self.make_cli(["1", "9", "7", "8", ""], visual=visual)
                    replay.game = Game(load_game(self.path))
                    with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((columns, rows))):
                        replay.crow_game()
                    self.assertFalse(remaining)
                    self.assertEqual(gold + 12, replay.game.player.gold)
                    self.assertEqual(2, replay.game.state.progress["crow:won"])

    def test_leaving_crow_table_costs_nothing_and_awards_nothing(self):
        cli, pending, _ = self.make_cli(["1", "0"])
        gold = cli.game.player.gold
        inventory = dict(cli.game.player.inventory)
        cli.crow_game()
        self.assertFalse(pending)
        self.assertEqual(gold, cli.game.player.gold)
        self.assertEqual(inventory, cli.game.player.inventory)
        self.assertNotIn("crow_prize", load_game(self.path).flags)
        self.assertNotIn("crow:played", cli.game.state.progress)

    def test_help_and_repeated_occupied_moves_keep_short_terminal_readable(self):
        cli, pending, frames = self.make_cli(["?", "?", "1", "1", "1", "1", "0"])
        with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((80, 24))):
            cli.crow_game()
        self.assertFalse(pending)
        for frame in frames:
            self.assertLessEqual(len(frame.splitlines()) + 1, 24, frame)
        self.assertIn("Help 1/", frames[1])
        self.assertIn("[9]", frames[2])
        self.assertNotIn("crow:played", cli.game.state.progress)

    def test_forest_wrong_answer_retry_and_viewing_do_not_duplicate_reward(self):
        cli, pending, frames = self.make_cli(
            ["", "2", "", "1", ">", "<", "", "1", "", "0"], location="forest")
        crystals = cli.game.player.inventory.get("crystal", 0)
        with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((80, 24))):
            cli.curiosity()
        self.assertFalse(pending)
        self.assertEqual(crystals + 1, cli.game.player.inventory["crystal"])
        self.assertIn("secret_reward:knocking_tree", load_game(self.path).flags)
        self.assertTrue(any("Scene 2/" in frame for frame in frames))

    def test_wide_services_use_larger_scenes_with_working_menu_hotspots(self):
        for method, markers in (("shop", ("Browse", "Sell")),
                                ("workshop", ("Craft", "Improve")),
                                ("character", ("Strength", "Vitality", "Agility"))):
            with self.subTest(method=method):
                cli, pending, frames = self.make_cli(["0"], location="village")
                with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((132, 52))):
                    getattr(cli, method)()
                self.assertFalse(pending)
                self.assertGreater(len(frames[0].splitlines()), 28)
                self.assertLessEqual(len(frames[0].splitlines()) + 1, 52)
                # Art, excluding the full-width HUD rules, should use the space.
                body = frames[0].splitlines()[4:-2]
                self.assertGreater(max(map(len, body)), 100)
                for index, marker in enumerate(markers, 1):
                    self.assertIn(f"[{index}]", frames[0])
                    self.assertIn(marker.lower(), frames[0].lower())


if __name__ == "__main__":
    unittest.main()
