"""Campaign and economy invariants through the same rules used by the CLI."""

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from sssd.content import ENEMIES, ITEMS, LOCATIONS, QUESTS, RECIPES
from sssd.engine import Game, SEALS, SHOP_STOCK
from sssd.storage import load_game, save_game


class WorldTests(unittest.TestCase):
    def setUp(self):
        self.game = Game(seed=31)

    def strong_player(self):
        """Skip grinding only in rule tests; every encounter/action remains real."""
        player = self.game.player
        player.strength = player.vitality = 100
        player.hp = player.max_hp
        player.gold = 1000

    def finish_fight(self):
        for _ in range(100):
            if self.game.battle is None:
                return
            self.game.combat("attack")
        self.fail("Encounter did not terminate")

    def discover_and_defeat(self):
        self.game.explore()
        self.finish_fight()
        self.game.explore()
        self.finish_fight()
        self.game.challenge()
        self.assertIsNotNone(self.game.battle)
        self.finish_fight()

    def test_connected_world_and_content_references(self):
        seen, frontier = set(), ["village"]
        obtainable = set(SHOP_STOCK) | set(self.game.player.inventory) | {"herb"}
        for item in ITEMS.values():
            self.assertGreaterEqual(item["price"], 0)
        while frontier:
            current = frontier.pop()
            if current in seen:
                continue
            seen.add(current)
            location = LOCATIONS[current]
            for neighbor in location["neighbors"]:
                self.assertIn(current, LOCATIONS[neighbor]["neighbors"])
                frontier.append(neighbor)
            self.assertTrue(set(location.get("enemies", [])) <= set(ENEMIES))
            obtainable.update(location.get("resources", {}))
            if location.get("boss"):
                self.assertIn(location["boss"], ENEMIES)
        self.assertEqual(seen, set(LOCATIONS))
        for enemy in ENEMIES.values():
            self.assertTrue(set(enemy["pattern"]) <= {"attack", "heavy", "poison", "guard"})
            obtainable.update(enemy.get("loot", {}))
        for quest in QUESTS.values():
            obtainable.update(quest["reward"].get("items", {}))
            for key in quest["objectives"]:
                kind, identifier = key.split(":")
                self.assertIn(identifier, {"own": ITEMS, "kill": ENEMIES, "explore": LOCATIONS}[kind])
        for recipe in RECIPES.values():
            self.assertTrue(set(recipe["ingredients"]) <= set(ITEMS))
            self.assertIn(recipe["produces"], ITEMS)
            obtainable.add(recipe["produces"])
        self.assertEqual(obtainable, set(ITEMS), "Every declared item must be obtainable")

    def test_bad_routes_and_castle_lock_do_not_move_or_advance_time(self):
        original = deepcopy(self.game.state)
        self.game.move("castle")
        self.assertEqual(self.game.state, original)
        self.game.move("bridge")
        steps = self.game.state.steps
        message = self.game.move("castle")
        self.assertIn("sealed", " ".join(message))
        self.assertEqual(self.game.state.location, "bridge")
        self.assertEqual(self.game.state.steps, steps)

    def test_farm_harvest_once_each_day_and_rest_is_available_without_gold(self):
        self.game.move("farm")
        self.game.player.gold = 0
        self.game.harvest()
        self.assertEqual(self.game.player.inventory["herb"], 3)
        self.game.harvest()
        self.assertEqual(self.game.player.inventory["herb"], 3)
        self.game.player.hp = 1
        self.game.rest()
        self.assertEqual(self.game.player.hp, self.game.player.max_hp)
        self.game.harvest()
        self.assertEqual(self.game.player.inventory["herb"], 6)

    def test_quest_delivery_consumes_supplies_and_pays_only_once(self):
        self.game.accept_quest("farm_supplies")
        self.game.player.add_item("herb", 3)
        gold = self.game.player.gold
        self.game.claim_quest("farm_supplies")
        self.assertEqual(self.game.state.quests["farm_supplies"], "complete")
        self.assertNotIn("herb", self.game.player.inventory)
        self.assertGreater(self.game.player.gold, gold)
        after = deepcopy(self.game.state)
        self.game.claim_quest("farm_supplies")
        self.assertEqual(self.game.state, after)

    def test_active_quest_tracks_avoid_random_quarry_grind(self):
        self.strong_player()
        self.game.talk("kieth")
        self.game.move("desert")
        encounters = []
        for _ in range(20):
            self.game.explore()
            if self.game.battle:
                encounters.append(self.game.battle.enemy_id)
                self.finish_fight()
            if len(encounters) == 3:
                break
        self.assertEqual(encounters, ["cactus", "cactus", "coyote"])

    def test_shop_rejects_invalid_or_unaffordable_transactions(self):
        for quantity in (-2, 0, 100, True, "2", 1.5):
            original = deepcopy(self.game.state)
            self.game.buy("potion", quantity)
            self.game.sell("potion", quantity)
            self.assertEqual(self.game.state, original)
        original = deepcopy(self.game.state)
        self.game.buy("iron_sword")
        self.game.sell("rusty_sword")  # last copy is equipped
        self.assertEqual(self.game.state, original)
        self.game.buy("potion", 2)
        self.assertEqual(self.game.player.inventory["potion"], 5)
        self.assertEqual(self.game.player.gold, 35 - ITEMS["potion"]["price"] * 2)

    def test_crafting_checks_every_ingredient_before_spending_anything(self):
        self.game.player.gold = 1000
        self.game.player.add_item("ore", 20)
        original = deepcopy(self.game.state)
        self.game.craft("dawn_blade")
        self.assertEqual(self.game.state, original)
        recipe_id = next(key for key, value in RECIPES.items() if value["produces"] == "potion")
        recipe = RECIPES[recipe_id]
        for item, quantity in recipe["ingredients"].items():
            self.game.player.add_item(item, quantity)
        count = self.game.player.inventory["potion"]
        self.game.craft(recipe_id)
        self.assertEqual(self.game.player.inventory["potion"], count + recipe["quantity"])

    def test_upgrade_is_bounded_and_selling_last_copy_removes_upgrade(self):
        player = self.game.player
        player.gold = 1000
        player.add_item("ore", 20)
        player.add_item("crystal", 10)
        attack = player.attack
        for _ in range(3):
            self.game.upgrade("rusty_sword")
        self.assertEqual(player.attack, attack + 6)
        original = deepcopy(self.game.state)
        self.game.upgrade("rusty_sword")
        self.assertEqual(self.game.state, original)
        self.game.equip("unequip:weapon")
        self.game.sell("rusty_sword")
        self.assertNotIn("rusty_sword", player.upgrades)

    def test_world_actions_cannot_bypass_battle(self):
        from sssd.combat import Battle
        self.game.battle = Battle(self.game.player, "cactus", self.game.rng)
        original = deepcopy(self.game.state)
        for method, args in [("rest", ()), ("move", ("farm",)), ("talk", ()),
                             ("buy", ("potion",)), ("use", ("potion",)),
                             ("equip", ("unequip:weapon",)), ("train", ("strength",)),
                             ("harvest", ()), ("craft", ("potion",))]:
            self.assertIn("encounter", " ".join(getattr(self.game, method)(*args)))
        self.assertEqual(self.game.state, original)

    def test_victory_rewards_cannot_be_claimed_twice(self):
        from sssd.combat import Battle
        self.strong_player()
        self.game.battle = Battle(self.game.player, "cactus", self.game.rng)
        self.finish_fight()
        original = deepcopy(self.game.state)
        self.game.combat("attack")
        self.assertEqual(self.game.state, original)
        self.assertEqual(self.game.state.progress["kill:cactus"], 1)

    def test_defeat_keeps_equipment_and_returns_to_village(self):
        from sssd.combat import Battle
        self.game.move("forest")
        player = self.game.player
        player.hp, player.gold = 1, 101
        self.game.battle = Battle(player, "hollow_king", self.game.rng)
        for _ in range(5):
            if self.game.battle is None:
                break
            self.game.combat("attack")
        self.assertIsNone(self.game.battle)
        self.assertEqual(self.game.state.location, "village")
        self.assertEqual(player.hp, player.max_hp)
        self.assertEqual(player.gold, 91)
        self.assertEqual(player.equipment["weapon"], "rusty_sword")
        self.assertNotIn("boss:hollow_king", self.game.state.flags)

    def test_campaign_has_reachable_endings_and_persists_completion(self):
        self.strong_player()
        self.game.talk("kieth")
        for route in [("forest",), ("village", "desert", "caves"),
                      ("desert", "village", "bridge", "sea")]:
            for place in route:
                self.game.move(place)
                self.assertEqual(self.game.state.location, place)
            self.discover_and_defeat()
        self.assertTrue(set(SEALS) <= self.game.state.flags)
        self.game.move("bridge")
        self.game.move("castle")
        self.discover_and_defeat()
        self.assertIn("finale_ready", self.game.state.flags)
        for choice in ("restore", "release"):
            with self.subTest(ending=choice), tempfile.TemporaryDirectory() as folder:
                game = Game(deepcopy(self.game.state))
                self.assertIn("THE END", " ".join(game.finish(choice)))
                saved = deepcopy(game.state)
                game.finish("release" if choice == "restore" else "restore")
                self.assertEqual(game.state, saved)
                path = Path(folder) / "slot.json"
                save_game(game.state, path)
                self.assertEqual(load_game(path), saved)
                game.move("bridge")
                self.assertEqual(game.state.location, "bridge", "Post-ending exploration remains open")


if __name__ == "__main__":
    unittest.main()
