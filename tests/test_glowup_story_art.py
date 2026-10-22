"""Illustrated action results retain the rules, checkpoints and menu keys."""

from collections import deque
import copy
from functools import wraps
from io import StringIO
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from sssd.cli import Console, GameCLI
from sssd.detailed_art import EQUIPMENT_ART
from sssd.engine import Game
from sssd.presentation import equipment_dock
from sssd.storage import load_game, save_game
from sssd.story_art import EVENT_ART, WIDE_EVENT_ART


class StoryArtTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="sssd-story-art-")
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "slot.json"

    def make_cli(self, read, *, location="farm", seed=0):
        output = StringIO()
        cli = GameCLI(Console(read, output, clear=False), self.path, seed=seed)
        cli.game = Game(seed=seed)
        cli.game.state.location = location
        cli.game.state.visited.add(location)
        return cli, output

    def track(self, game, name):
        calls = []
        method = getattr(game, name)

        @wraps(method)
        def counted(*args, **kwargs):
            calls.append((args, kwargs))
            return method(*args, **kwargs)

        setattr(game, name, counted)
        return calls

    def test_farmer_menu_opens_rich_dialogue_without_repeating_talk_or_save(self):
        for columns in (80, 140):
            with self.subTest(columns=columns):
                answers = deque(["3", ">", "<", "", EOFError()])
                dialogue_views = []

                def read(_prompt):
                    frame = "\n".join(cli.console.frame)
                    if "A WORD WITH FARMER" in frame:
                        dialogue_views.append(frame)
                        self.assertEqual(expected.state, cli.game.state)
                        self.assertEqual(expected.state, load_game(self.path))
                        self.assertEqual(1, len(calls))
                        self.assertEqual(1, save.call_count)
                    self.assertTrue(answers, "Unexpected extra farmer-menu prompt.")
                    answer = answers.popleft()
                    if isinstance(answer, BaseException):
                        raise answer
                    return answer

                cli, output = self.make_cli(read)
                expected = Game(copy.deepcopy(cli.game.state), seed=0)
                messages = expected.talk("farmer")
                calls = self.track(cli.game, "talk")
                with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((columns, 24))):
                    with patch("sssd.cli.save_game", wraps=save_game) as save:
                        with self.assertRaises(EOFError):
                            cli.adventure()
                self.assertFalse(answers)
                self.assertEqual(3, len(dialogue_views))
                self.assertIn("Scene 2/", dialogue_views[1])
                self.assertIn("Scene 1/", dialogue_views[2])
                source = WIDE_EVENT_ART if columns == 140 else EVENT_ART
                self.assertIn(source["talk_farmer"].strip("\n").splitlines()[0].strip(),
                              dialogue_views[0])
                self.assertIn(" ".join(messages[0].split()), " ".join(output.getvalue().split()))
                self.assertIsNone(cli.console.story_views)

    def test_forest_intermediate_scene_keeps_single_exploration_and_checkpoint(self):
        for seed, encounter in ((0, False), (1, True)):
            with self.subTest(seed=seed, encounter=encounter):
                answers = deque(["1", ">", "<", "", EOFError()])
                exploration_views = []

                def read(_prompt):
                    frame = "\n".join(cli.console.frame)
                    if "EXPLORING |" in frame:
                        exploration_views.append(frame)
                        self.assertEqual(expected.state, cli.game.state)
                        self.assertEqual(1, len(calls))
                        self.assertEqual(1 if encounter else 2, save.call_count)
                        self.assertEqual(initial if encounter else expected.state,
                                         load_game(self.path))
                    self.assertTrue(answers, "Unexpected extra exploration prompt.")
                    answer = answers.popleft()
                    if isinstance(answer, BaseException):
                        raise answer
                    return answer

                cli, output = self.make_cli(read, location="forest", seed=seed)
                initial = copy.deepcopy(cli.game.state)
                expected = Game(copy.deepcopy(initial), seed=seed)
                messages = expected.explore()
                self.assertEqual(encounter, expected.battle is not None)
                calls = self.track(cli.game, "explore")
                with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((80, 24))):
                    with patch("sssd.cli.save_game", wraps=save_game) as save:
                        with self.assertRaises(EOFError):
                            cli.adventure()
                self.assertFalse(answers)
                self.assertEqual(3, len(exploration_views))
                self.assertIn("88888888888", exploration_views[0])
                self.assertIn("Scene 2/", exploration_views[1])
                self.assertIn("Scene 1/", exploration_views[2])
                self.assertEqual(1, cli.game.state.progress["explore:forest"])
                self.assertEqual(expected.state, cli.game.state)
                self.assertIn(messages[1], output.getvalue())
                if encounter:
                    self.assertEqual(expected.battle.enemy_id, cli.game.battle.enemy_id)
                    self.assertEqual(0, cli.game.battle.turn)
                self.assertIsNone(cli.console.story_views)

    def test_consecutive_result_panels_do_not_share_pages_or_replay_harvest(self):
        answers = deque([">", "<", "", ">", "<", ""])
        stage = "talk"

        def read(_prompt):
            frame = "\n".join(cli.console.frame)
            if stage == "talk":
                self.assertIn("A WORD WITH FARMER", frame)
                self.assertEqual(1, save.call_count)
            else:
                self.assertIn("AMONG THE BEET ROWS", frame)
                self.assertNotIn("A WORD WITH FARMER", frame)
                self.assertEqual(expected.state, cli.game.state)
                self.assertEqual(2, save.call_count)
            self.assertTrue(answers, "Unexpected extra result prompt.")
            return answers.popleft()

        cli, _ = self.make_cli(read)
        expected = Game(copy.deepcopy(cli.game.state), seed=0)
        expected.talk("farmer")
        expected.harvest()
        calls = self.track(cli.game, "harvest")
        with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((80, 24))):
            with patch("sssd.cli.save_game", wraps=save_game) as save:
                cli.perform(cli.game.talk, "farmer")
                self.assertIsNone(cli.console.story_views)
                stage = "harvest"
                cli.perform(cli.game.harvest)
        self.assertFalse(answers)
        self.assertEqual(1, len(calls))
        self.assertEqual(expected.state, cli.game.state)
        self.assertEqual(expected.state, load_game(self.path))
        self.assertIsNone(cli.console.story_views)

    def test_wide_terminal_reveals_more_than_the_old_78_column_limit(self):
        console = Console(lambda _: "", StringIO(), clear=False)
        with patch("sssd.cli.shutil.get_terminal_size", return_value=os.terminal_size((180, 50))):
            self.assertEqual(178, console.width)
            self.assertGreater(console.width, 173)

    def test_equipment_dock_preserves_separate_objects_and_attached_keys(self):
        keys = {"inventory": "7", "character": "8", "journal": "9"}
        drawing = equipment_dock(keys, EQUIPMENT_ART, 78)
        lines = drawing.splitlines()
        self.assertLessEqual(max(map(len, lines)), 78)
        for column, token in enumerate(keys):
            start = column * 26  # Each 22-column object has a four-column gutter.
            for row, original in enumerate(EQUIPMENT_ART[token].splitlines()):
                self.assertEqual(original.rstrip(), lines[row][start:start + 22].rstrip())
        self.assertEqual({"7", "8", "9"}, set(re.findall(r"\[(\d+)\]", lines[-1])))
        self.assertIn("[7] Inventory", lines[-1])
        self.assertIn("[8] Training", lines[-1])
        self.assertIn("[9] Journal", lines[-1])
        narrow = equipment_dock(keys, EQUIPMENT_ART, 40)
        self.assertLessEqual(max(map(len, narrow.splitlines())), 40)
        for key in keys.values():
            self.assertEqual(1, narrow.count(f"[{key}]"))


if __name__ == "__main__":
    unittest.main()
