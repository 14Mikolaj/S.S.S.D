"""Mechanics invariants and save corruption checks for the expanded adventure."""

import copy
import json
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

from sssd.combat import Battle
from sssd.content import ENEMIES, ITEMS
from sssd.model import GameState, Player
from sssd.storage import MAX_SAVE_BYTES, SaveError, load_game, save_game


class PredictableRandom(random.Random):
    def random(self):
        return 0.99

    def randint(self, low, high):
        return 0


class PlayerTests(unittest.TestCase):
    def test_equipment_is_idempotent_and_does_not_heal(self):
        player = Player(hp=20, energy=2)
        original = (player.attack, player.defense, player.max_hp, player.max_energy)
        for _ in range(10):
            player.equip("rusty_sword")
            player.equip("tunic")
        self.assertEqual(original, (player.attack, player.defense, player.max_hp, player.max_energy))
        self.assertEqual((20, 2), (player.hp, player.energy))

    def test_changing_health_equipment_clamps_without_healing(self):
        equipment = {"test_charm": {"name": "Test Charm", "slot": "charm", "hp": 25,
                                     "energy": 3, "attack": 2, "defense": 1}}
        with patch.dict(ITEMS, equipment):
            player = Player()
            old_max = player.max_hp
            player.add_item("test_charm")
            player.equip("test_charm")
            self.assertEqual(old_max + 25, player.max_hp)
            self.assertEqual(old_max, player.hp)
            player.hp = player.max_hp
            player.energy = player.max_energy
            player.equipment["charm"] = None
            player.clamp_resources()
            self.assertEqual(old_max, player.hp)
            self.assertEqual(player.max_energy, player.energy)

    def test_inventory_refuses_negative_bool_and_equipped_removals(self):
        player = Player()
        original = copy.deepcopy(player.inventory)
        for amount in (-1, 0, True, 1.5, 100):
            self.assertFalse(player.remove_item("potion", amount))
        self.assertFalse(player.remove_item("rusty_sword"))
        self.assertFalse(player.remove_item("nonexistent"))
        self.assertEqual(original, player.inventory)
        for amount in (-1, 0, True, 1.5):
            with self.assertRaises(ValueError):
                player.add_item("potion", amount)
        self.assertTrue(player.remove_item("potion", 3))
        self.assertNotIn("potion", player.inventory)

    def test_xp_overflow_grants_every_level(self):
        player = Player(hp=1, energy=0)
        messages = player.gain_xp(60 + 85 + 10)
        self.assertEqual((3, 10, 6), (player.level, player.xp, player.stat_points))
        self.assertEqual((7, 7, 7), (player.strength, player.vitality, player.agility))
        self.assertEqual((player.max_hp, player.max_energy), (player.hp, player.energy))
        self.assertEqual(2, len(messages))


class CombatTests(unittest.TestCase):
    def setUp(self):
        self.enemy_patch = patch.dict(ENEMIES, {
            "test_dummy": {"name": "Unionized Test Dummy", "hp": 300, "attack": 12,
                           "defense": 2, "pattern": ["attack", "heavy", "poison", "guard"]},
        })
        self.enemy_patch.start()
        self.addCleanup(self.enemy_patch.stop)

    def battle(self, player=None):
        return Battle(player or Player(), "test_dummy", PredictableRandom())

    def test_invalid_and_unaffordable_actions_do_not_take_turns(self):
        player = Player(energy=0)
        battle = self.battle(player)
        before = copy.deepcopy(player)
        for action in ("bananas", "power", "mend", "potion", "antidote"):
            battle.act(action)
            self.assertEqual(before, player)
            self.assertEqual(0, battle.turn)
            self.assertEqual(300, battle.enemy_hp)

    def test_potion_consumes_exactly_one(self):
        player = Player(hp=20)
        battle = self.battle(player)
        battle.enemy["pattern"] = ["guard"]
        battle.act("potion")
        self.assertEqual(2, player.inventory["potion"])
        self.assertEqual(20 + player.max_hp * 2 // 5, player.hp)
        self.assertEqual(1, battle.turn)

    def test_dead_enemy_cannot_retaliate_or_poison(self):
        player = Player(hp=1)
        battle = self.battle(player)
        battle.enemy_hp = 1
        battle.poison_turns = 2
        battle.act("attack")
        self.assertEqual("victory", battle.result)
        self.assertEqual(1, player.hp)
        self.assertEqual(0, battle.poison_turns)
        snapshot = copy.deepcopy(player)
        battle.act("attack")
        self.assertEqual(snapshot, player)
        self.assertEqual(1, battle.turn)

    def test_battle_never_awards_rewards(self):
        player = Player()
        battle = self.battle(player)
        battle.enemy_hp = 1
        battle.act("attack")
        self.assertEqual((0, 35), (player.xp, player.gold))

    def test_guard_blunts_telegraphed_heavy_attack_and_restores_energy(self):
        ordinary = self.battle(Player(energy=0))
        guarded = self.battle(Player(energy=0))
        ordinary.turn = guarded.turn = 1
        self.assertIn("HEAVY", guarded.intent)
        ordinary.act("attack")
        guarded.act("guard")
        self.assertGreater(guarded.player.hp, ordinary.player.hp)
        self.assertEqual(3, guarded.player.energy)

    def test_antidote_cures_and_uses_one_item(self):
        battle = self.battle()
        battle.enemy["pattern"] = ["guard"]
        battle.poison_turns = 2
        before_hp = battle.player.hp
        battle.act("antidote")
        self.assertEqual(0, battle.poison_turns)
        self.assertNotIn("antidote", battle.player.inventory)
        self.assertEqual(before_hp, battle.player.hp)

    def test_successful_escape_skips_enemy_and_poison_damage(self):
        battle = self.battle(Player(hp=1))
        battle.poison_turns = 3
        with patch.object(battle.rng, "random", return_value=0):
            battle.act("flee")
        self.assertEqual("fled", battle.result)
        self.assertEqual(1, battle.player.hp)
        self.assertEqual(0, battle.poison_turns)

    def test_defeat_and_energy_are_clamped(self):
        battle = self.battle(Player(hp=1))
        battle.act("attack")
        self.assertEqual("defeat", battle.result)
        self.assertEqual(0, battle.player.hp)
        self.assertLessEqual(battle.player.energy, battle.player.max_energy)

    def test_same_seed_produces_same_encounter(self):
        first = Battle(Player(), "test_dummy", random.Random(127))
        second = Battle(Player(), "test_dummy", random.Random(127))
        for action in ("attack", "guard", "power", "mend", "attack", "flee"):
            self.assertEqual(first.act(action), second.act(action))
            self.assertEqual(first.player, second.player)
            self.assertEqual(first.enemy_hp, second.enemy_hp)
            self.assertEqual(first.result, second.result)


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "saves" / "slot1.json"
        self.state = GameState()

    def test_round_trip_and_previous_good_backup(self):
        self.state.flags.add("story_started")
        self.state.player.upgrades["rusty_sword"] = 1
        self.state.journal.append("The mayor has misplaced the apocalypse paperwork.")
        self.assertEqual(self.path, save_game(self.state, self.path))
        self.assertEqual(self.state, load_game(self.path))
        self.state.player.gold += 12
        save_game(self.state, self.path)
        backup = self.path.with_name(self.path.name + ".bak")
        self.assertEqual(35, load_game(backup).player.gold)
        self.assertEqual(47, load_game(self.path).player.gold)

    def mutate_save(self, mutate):
        save_game(self.state, self.path)
        document = json.loads(self.path.read_text())
        mutate(document)
        self.path.write_text(json.dumps(document))
        with self.assertRaises(SaveError):
            load_game(self.path)
        self.path.unlink()

    def test_invalid_typed_values_equipment_locations_and_versions_rejected(self):
        mutations = [
            lambda d: d.update(version=999),
            lambda d: d.update(version=True),
            lambda d: d["state"]["player"].update(gold=True),
            lambda d: d["state"]["player"].update(hp=1_000_000),
            lambda d: d["state"]["player"].update(energy=-1),
            lambda d: d["state"]["player"].update(strength=0),
            lambda d: d["state"]["player"].update(name="\u001b[2J"),
            lambda d: d["state"]["player"]["inventory"].update(potion=-5),
            lambda d: d["state"]["player"]["inventory"].update(potion=True),
            lambda d: d["state"]["player"]["inventory"].pop("rusty_sword"),
            lambda d: d["state"]["player"]["equipment"].update(weapon="potion"),
            lambda d: d["state"]["player"]["upgrades"].update(rusty_sword=4),
            lambda d: d["state"]["player"]["upgrades"].update(iron_sword=1),
            lambda d: d["state"].update(location="not-a-place"),
            lambda d: d["state"].update(flags=["unknown_flag"]),
            lambda d: d["state"].update(quests={"unknown": "active"}),
            lambda d: d["state"].update(progress={"kill:imaginary": 1}),
            lambda d: d["state"].update(ending="unknown"),
            lambda d: d["state"].update(day=2),
            lambda d: d["state"].update(visited=[]),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutations.index(mutate)):
                self.mutate_save(mutate)

    def test_truncation_and_oversize_leave_file_untouched(self):
        self.path.parent.mkdir()
        for payload in (b'{"version":1,"state":', b"x" * (MAX_SAVE_BYTES + 1),
                        b'{"version":1,"version":1,"state":{}}'):
            with self.subTest(length=len(payload)):
                self.path.write_bytes(payload)
                with self.assertRaises(SaveError):
                    load_game(self.path)
                self.assertEqual(payload, self.path.read_bytes())

    def test_corrupt_existing_save_and_good_backup_are_preserved(self):
        save_game(self.state, self.path)
        self.state.player.gold += 1
        save_game(self.state, self.path)
        backup = self.path.with_name(self.path.name + ".bak")
        original_backup = backup.read_bytes()
        self.path.write_text("not JSON anymore")
        with self.assertRaises(SaveError):
            save_game(self.state, self.path)
        self.assertEqual("not JSON anymore", self.path.read_text())
        self.assertEqual(original_backup, backup.read_bytes())

    def test_failed_atomic_replace_preserves_previous_checkpoint(self):
        save_game(self.state, self.path)
        original = self.path.read_bytes()
        self.state.player.gold += 1
        from sssd import storage
        original_replace = storage.os.replace

        def fail_final_replace(source, destination):
            if Path(destination) == self.path:
                raise OSError("Simulated disk write failure")
            return original_replace(source, destination)

        with patch("sssd.storage.os.replace", side_effect=fail_final_replace):
            with self.assertRaises(SaveError):
                save_game(self.state, self.path)
        self.assertEqual(original, self.path.read_bytes())
        self.assertEqual([], list(self.path.parent.glob("*.tmp")))

    def test_invalid_state_is_rejected_before_modifying_save(self):
        save_game(self.state, self.path)
        original = self.path.read_bytes()
        self.state.player.hp = self.state.player.max_hp + 1
        with self.assertRaises(SaveError):
            save_game(self.state, self.path)
        self.assertEqual(original, self.path.read_bytes())


if __name__ == "__main__":
    unittest.main()
