"""Optional discoveries, legal crow games, and once-only persisted rewards."""

import copy
import json
from pathlib import Path
import tempfile
import unittest

from sssd.combat import Battle
from sssd.engine import Game, SEALS
from sssd.model import GameState
from sssd.secrets import CrowGame, SECRETS
from sssd.storage import SaveError, load_game, save_game


# Complete games against the actual crow, including a fork that beats it.
MATCHES = {"loss": (1, 2, 4), "draw": (1, 2, 7, 6, 8), "win": (1, 9, 7, 8)}


def play_match(board, result):
    for square in MATCHES[result]:
        board.play(square)
    return board


class CrowRulesTests(unittest.TestCase):
    def test_illegal_and_occupied_squares_never_take_a_turn(self):
        game = CrowGame()
        for square in (-1, 0, 10, True, 1.5, "1", None):
            before = game.board
            game.play(square)
            self.assertEqual(before, game.board)
            self.assertFalse(game.finished)
        game.play(1)
        self.assertEqual("X", game.board[0])
        self.assertEqual("O", game.board[4])
        before = game.board
        for square in (1, 5):
            game.play(square)
            self.assertEqual(before, game.board)

    def test_crow_blocks_a_line_and_never_overwrites_a_mark(self):
        game = CrowGame()
        game.play(1)
        game.play(2)
        self.assertEqual(["X", "X", "O"], game.board[:3])
        self.assertEqual("O", game.board[4])
        self.assertEqual(2, game.board.count("X"))
        self.assertEqual(2, game.board.count("O"))

    def test_real_win_draw_and_loss_finish_and_replay_verifies_them(self):
        for result in MATCHES:
            with self.subTest(result=result):
                game = play_match(CrowGame(), result)
                self.assertTrue(game.finished)
                self.assertEqual(result, game.result)
                self.assertEqual(result, game.verified_result())
                before = game.board
                game.play(3)
                self.assertEqual(before, game.board)
                if result == "draw":
                    self.assertNotIn(" ", game.board)

    def test_board_view_cannot_edit_actual_game_and_forged_history_fails(self):
        game = CrowGame()
        displayed_board = game.board
        displayed_board[:3] = ["X", "X", "X"]
        self.assertEqual([" "] * 9, game.board)
        with self.assertRaises(AttributeError):
            game.result = "win"
        game._result = "win"  # Even internal tampering must not buy a reward.
        self.assertIsNone(game.verified_result())

    def test_crow_strategy_is_deterministic(self):
        first, second = CrowGame(), CrowGame()
        for square in MATCHES["draw"]:
            self.assertEqual(first.play(square), second.play(square))
            self.assertEqual(first.board, second.board)


class SecretIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="sssd-secret-tests-")
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "slot.json"

    def at(self, location):
        game = Game(seed=42)
        game.state.location = location
        game.state.visited.add(location)
        return game

    def test_each_discovery_and_item_reward_happens_only_once(self):
        for location, secret in SECRETS.items():
            with self.subTest(location=location):
                game = self.at(location)
                before = copy.deepcopy(game.state)
                game.investigate()
                first_journal = list(game.state.journal)
                game.investigate()
                self.assertEqual(first_journal, game.state.journal)
                game.secret_action(secret["reward_action"])
                for item, quantity in secret["reward"].items():
                    self.assertEqual(before.player.inventory.get(item, 0) + quantity,
                                     game.player.inventory[item])
                earned_inventory = copy.deepcopy(game.player.inventory)
                game.secret_action(secret["reward_action"])
                self.assertEqual(earned_inventory, game.player.inventory)
                self.assertEqual((before.steps, before.day, before.player.hp, before.player.xp),
                                 (game.state.steps, game.state.day, game.player.hp, game.player.xp))
                self.assertFalse(set(SEALS) & game.state.flags)
                self.assertEqual(before.quests, game.state.quests)
                self.assertIsNone(game.state.ending)
                save_game(game.state, self.path)
                restored = Game(load_game(self.path))
                restored.secret_action(secret["reward_action"])
                self.assertEqual(earned_inventory, restored.player.inventory)

    def test_riddle_can_be_retried_without_punishment(self):
        game = self.at("forest")
        initial = copy.deepcopy(game.player)
        self.assertIn("try again", " ".join(game.secret_action("mayor")))
        self.assertEqual(initial, game.player)
        self.assertIn("try again", " ".join(game.secret_action("tree")))
        self.assertEqual(initial, game.player)
        game.secret_action("echo")
        self.assertEqual(1, game.player.inventory["crystal"])
        self.assertIn("secret_reward:knocking_tree", game.state.flags)

    def test_win_and_draw_each_qualify_for_the_same_first_prize(self):
        for result in ("win", "draw"):
            with self.subTest(result=result):
                game = self.at("farm")
                original_gold = game.player.gold
                session = play_match(game.start_crow_game(), result)
                game.claim_crow_prize(session)
                self.assertEqual(original_gold + 12, game.player.gold)
                self.assertEqual(2, game.player.inventory["herb"])
                self.assertIn("crow_prize", game.state.flags)
                self.assertEqual(1, game.state.progress["crow:played"])
                game.claim_crow_prize(session)
                self.assertEqual(original_gold + 12, game.player.gold)
                self.assertEqual(1, game.state.progress["crow:played"])
                second = play_match(game.start_crow_game(), result)
                game.claim_crow_prize(second)
                self.assertEqual(original_gold + 12, game.player.gold)
                self.assertEqual(2, game.player.inventory["herb"])
                self.assertEqual(2, game.state.progress["crow:played"])

    def test_losing_costs_nothing_and_later_draw_still_earns_prize(self):
        game = self.at("farm")
        initial = copy.deepcopy(game.player)
        game.claim_crow_prize(play_match(game.start_crow_game(), "loss"))
        self.assertEqual(initial, game.player)
        self.assertNotIn("crow_prize", game.state.flags)
        game.claim_crow_prize(play_match(game.start_crow_game(), "draw"))
        self.assertEqual(initial.gold + 12, game.player.gold)
        self.assertEqual(2, game.state.progress["crow:played"])

    def test_result_strings_other_sessions_and_unfinished_games_cannot_claim(self):
        game = self.at("farm")
        valid_but_foreign = play_match(CrowGame(), "win")
        own_unfinished = game.start_crow_game()
        before = copy.deepcopy(game.state)
        for alleged_score in ("win", "draw", None, valid_but_foreign, own_unfinished):
            game.claim_crow_prize(alleged_score)
            self.assertEqual(before, game.state)
        own_unfinished._result = "draw"
        game.claim_crow_prize(own_unfinished)
        self.assertEqual(before, game.state)

    def test_starting_new_session_invalidates_previous_scorecard(self):
        game = self.at("farm")
        previous = play_match(game.start_crow_game(), "win")
        game.start_crow_game()
        before = copy.deepcopy(game.state)
        game.claim_crow_prize(previous)
        self.assertEqual(before, game.state)

    def test_wrong_location_and_active_battle_block_every_secret_action(self):
        game = self.at("village")
        before = copy.deepcopy(game.state)
        self.assertIsNone(game.start_crow_game())
        game.secret_action("stamp")
        game.secret_action([])
        game.claim_crow_prize(play_match(CrowGame(), "draw"))
        self.assertEqual(before, game.state)

        game = self.at("farm")
        session = play_match(game.start_crow_game(), "win")
        game.battle = Battle(game.player, "cactus")
        before = copy.deepcopy(game.state)
        for action, args in ((game.investigate, ()),
                             (game.secret_action, ("scarecrow",)),
                             (game.claim_crow_prize, (session,))):
            self.assertIn("encounter", " ".join(action(*args)))
            self.assertEqual(before, game.state)
        self.assertIsNone(game.start_crow_game())
        self.assertEqual(before, game.state)

    def test_crow_reward_and_statistics_persist_without_saving_a_live_board(self):
        game = self.at("farm")
        game.claim_crow_prize(play_match(game.start_crow_game(), "draw"))
        save_game(game.state, self.path)
        data = json.loads(self.path.read_text())
        self.assertEqual(1, data["version"])
        self.assertNotIn("board", data["state"])
        restored = Game(load_game(self.path))
        original_gold = restored.player.gold
        restored.claim_crow_prize(play_match(restored.start_crow_game(), "win"))
        self.assertEqual(original_gold, restored.player.gold)
        self.assertEqual(2, restored.player.inventory["herb"])
        self.assertEqual({"crow:played": 2, "crow:drawn": 1, "crow:won": 1},
                         restored.state.progress)
        save_game(restored.state, self.path)
        self.assertEqual(restored.state, load_game(self.path))

    def test_existing_version_one_saves_still_load_and_unknown_secrets_do_not(self):
        previous_version_state = GameState()
        save_game(previous_version_state, self.path)
        self.assertEqual(previous_version_state, load_game(self.path))
        document = json.loads(self.path.read_text())
        document["state"]["flags"].append("secret:invented")
        self.path.write_text(json.dumps(document))
        with self.assertRaises(SaveError):
            load_game(self.path)

    def test_locations_without_curiosities_leave_state_unchanged(self):
        game = self.at("caves")
        before = copy.deepcopy(game.state)
        game.investigate()
        game.secret_action("echo")
        self.assertEqual(before, game.state)


if __name__ == "__main__":
    unittest.main()
