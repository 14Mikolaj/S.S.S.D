"""Bounded terminal flows, including interrupted encounters and save failures."""

from collections import deque
from dataclasses import asdict
from io import StringIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from sssd.cli import Console, GameCLI, main
from sssd.combat import Battle
from sssd.engine import Game
from sssd.storage import SaveError, load_game, save_game


class CLITests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="sssd-cli-tests-")
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "slot.json"

    def cli(self, answers, *, game=True):
        pending = deque(answers)
        output = StringIO()

        def read(_prompt):
            if not pending:
                self.fail("Unexpected extra input request:\n" + output.getvalue()[-600:])
            value = pending.popleft()
            if isinstance(value, BaseException):
                raise value
            return value

        cli = GameCLI(Console(read, output, clear=False), self.path, seed=4)
        if game:
            cli.game = Game(seed=4)
        return cli, pending, output

    def test_new_adventure_quest_and_continue(self):
        cli, pending, output = self.cli([
            "1", "Rai", "",       # new adventure and prologue
            "1", "1", "", "0",  # Kieth, then leave the locals
            "2", "1", "1", "", "0",  # accept the first board quest
            "9", "",              # journal
            "0", "", "0",         # save, then quit the title
        ], game=False)
        self.assertEqual(cli.main_menu(), 0)
        self.assertFalse(pending)
        saved = load_game(self.path)
        self.assertEqual(saved.player.name, "Rai")
        self.assertIn("story_started", saved.flags)
        self.assertEqual(saved.quests["trail_watch"], "active")
        self.assertIn("Next:", output.getvalue())
        self.assertNotIn("\033", output.getvalue())

        cli, pending, _ = self.cli(["2", "0", "", "0"], game=False)
        self.assertEqual(cli.main_menu(), 0)
        self.assertFalse(pending)
        self.assertEqual(asdict(load_game(self.path)), asdict(saved))

    def test_invalid_names_and_purchase_quantities_reprompt(self):
        cli, pending, output = self.cli(["bad\x1bname", "n" * 33, "  Rai  ", ""], game=False)
        self.assertTrue(cli.new_game())
        self.assertFalse(pending)
        self.assertEqual(cli.game.player.name, "Rai")
        self.assertIn("control characters", output.getvalue())
        self.assertIn("32 characters", output.getvalue())

        cli, pending, output = self.cli(["1", "1", "1.5", "-2", "2", "", "0"])
        cli.shop()
        self.assertFalse(pending)
        self.assertEqual(cli.game.player.inventory["potion"], 5)
        self.assertEqual(cli.game.player.gold, 3)
        self.assertEqual(output.getvalue().count("positive whole number"), 2)

    def test_new_game_needs_yes_and_preserves_previous_save(self):
        original = Game().state
        original.player.name = "Original"
        save_game(original, self.path)
        original_bytes = self.path.read_bytes()

        cli, pending, _ = self.cli(["yes"], game=False)
        self.assertFalse(cli.new_game())
        self.assertFalse(pending)
        self.assertEqual(self.path.read_bytes(), original_bytes)

        cli, pending, _ = self.cli(["YES", "New adventurer", ""], game=False)
        self.assertTrue(cli.new_game())
        self.assertFalse(pending)
        self.assertEqual(load_game(self.path).player.name, "New adventurer")
        backup = self.path.with_name(self.path.name + ".bak")
        self.assertEqual(backup.read_bytes(), original_bytes)

    def test_new_game_archives_corruption_and_keeps_valid_backup(self):
        backup = self.path.with_name(self.path.name + ".bak")
        save_game(Game().state, backup)
        backup_bytes = backup.read_bytes()
        self.path.write_bytes(b"{damaged checkpoint")
        cli, pending, output = self.cli(["YES", "Recovered", "", ""], game=False)
        self.assertTrue(cli.new_game())
        self.assertFalse(pending)
        archives = list(self.path.parent.glob("slot.json.corrupt-*"))
        self.assertEqual(len(archives), 1)
        self.assertEqual(archives[0].read_bytes(), b"{damaged checkpoint")
        self.assertEqual(backup.read_bytes(), backup_bytes)
        self.assertEqual(load_game(self.path).player.name, "Recovered")
        self.assertIn("Damaged save preserved", output.getvalue())

    def test_continue_does_not_rewrite_a_damaged_save(self):
        self.path.write_bytes(b"not json")
        cli, pending, output = self.cli([""], game=False)
        self.assertFalse(cli.continue_game())
        self.assertFalse(pending)
        self.assertEqual(self.path.read_bytes(), b"not json")
        self.assertIn("left untouched", output.getvalue())

    def test_failed_save_and_return_keeps_adventure_open(self):
        cli, pending, output = self.cli(["0", "", EOFError()])
        state = cli.game.state
        state.player.gold = 123
        with patch("sssd.cli.save_game", side_effect=SaveError("disk full")):
            with self.assertRaises(EOFError):
                cli.adventure()
        self.assertFalse(pending)
        self.assertIs(cli.game.state, state)
        self.assertEqual(state.player.gold, 123)
        self.assertIn("adventure is still open", output.getvalue())
        self.assertNotIn("Checkpoint saved", output.getvalue())

    def test_interrupted_real_battle_preserves_pre_encounter_checkpoint(self):
        cli, pending, _ = self.cli(["", "1", "", EOFError()])
        cli.game.move("desert")
        cli.game.player.strength = 1
        before_encounter = asdict(cli.game.state)
        with patch("sssd.cli.save_game", wraps=save_game) as writer:
            with self.assertRaises(EOFError):
                cli.encounter(cli.game.explore)
        self.assertFalse(pending)
        self.assertTrue(cli.active_battle())
        self.assertLess(cli.game.battle.enemy_hp, cli.game.battle.enemy["hp"])
        self.assertGreater(cli.game.battle.turn, 0)
        self.assertEqual(writer.call_count, 1)
        self.assertEqual(asdict(load_game(self.path)), before_encounter)

    def test_farm_dialogue_is_reachable(self):
        cli, pending, output = self.cli(["3", "", "0", ""])
        cli.game.move("farm")
        cli.adventure()
        self.assertFalse(pending)
        self.assertIn("The farmer points at a cactus.", output.getvalue())

    def test_battle_shows_current_guard_and_next_intent(self):
        cli, pending, output = self.cli([EOFError()])
        cli.game.battle = Battle(cli.game.player, "cactus")
        cli.game.battle.enemy_guarding = True
        with self.assertRaises(EOFError):
            cli.combat()
        self.assertFalse(pending)
        self.assertIn("Preparing an ordinary attack", output.getvalue())
        self.assertIn("enemy is guarding now", output.getvalue())

    def test_eof_and_ctrl_c_exit_without_creating_a_save(self):
        for interruption in (EOFError, KeyboardInterrupt):
            with self.subTest(interruption=interruption.__name__):
                with patch("builtins.input", side_effect=interruption):
                    with patch("sys.stdout", new_callable=StringIO) as output:
                        self.assertEqual(main(["--save", str(self.path)]), 0)
                self.assertFalse(self.path.exists())
                self.assertIn("No checkpoint was loaded or saved", output.getvalue())


if __name__ == "__main__":
    unittest.main()
