"""Regression journeys through the original interactive game, using only stdlib.

Run with: python -B -m unittest discover -s tests -v
Inputs name the menu that must request them, so an unexpected loop fails instead
of silently consuming a later answer. State injection keeps combat deterministic
without hours of grinding; all actions under test still use the real menus.
"""

import contextlib
from dataclasses import dataclass
import io
from pathlib import Path
import runpy
import sys
import unittest
from unittest.mock import patch
import warnings


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main_.py"


class GameStopped(BaseException):
    """Stop at an explicitly expected menu, bypassing game input error handlers."""


class HarnessFailure(BaseException):
    """Unexpected control flow must also bypass broad game exception handlers."""


@dataclass
class Step:
    caller: str
    reply: str | None = None
    updates: dict | None = None
    expected: dict | None = None
    prompt_contains: str | None = None


class BoundedOutput(io.StringIO):
    def write(self, value):
        if self.tell() + len(value) > 1_000_000:
            raise HarnessFailure("Game exceeded the output budget (possible loop)")
        return super().write(value)


class GameTests(unittest.TestCase):
    def play(self, steps, *, enemy=1, exits=False):
        """Run a fresh game until the final scripted menu or an expected quit."""
        script = iter([Step("<module>", ""), Step("<module>", ""), *steps])
        output = BoundedOutput()
        last_state = None
        consumed = 0
        line_budget = 250_000

        def game_input(prompt=""):
            nonlocal last_state, consumed
            output.write(prompt)
            caller = sys._getframe(1)
            frame = caller
            while frame is not None and frame.f_code.co_filename != str(MAIN):
                frame = frame.f_back
            if frame is None:
                raise HarnessFailure("Input did not originate in the game")
            state = frame.f_globals
            last_state = state.copy()
            try:
                step = next(script)
            except StopIteration:
                raise HarnessFailure(f"Unexpected extra input in {caller.f_code.co_name}")
            consumed += 1
            if caller.f_code.co_name != step.caller:
                raise HarnessFailure(
                    f"Input {consumed}: expected {step.caller}, "
                    f"got {caller.f_code.co_name}; prompt={prompt!r}"
                )
            if step.prompt_contains is not None and step.prompt_contains not in prompt:
                raise HarnessFailure(f"Input {consumed}: unexpected prompt {prompt!r}")
            if step.expected:
                for key, value in step.expected.items():
                    if state[key] != value:
                        raise HarnessFailure(
                            f"Input {consumed} in {step.caller}: "
                            f"expected {key}={value!r}, got {state[key]!r}"
                        )
            if step.updates:
                state.update(step.updates)
                last_state = state.copy()
            if step.reply is None:
                raise GameStopped()
            return step.reply

        def fixed_randint(low, high):
            if (low, high) == (1, 5):
                return enemy
            if (low, high) == (0, 100):
                return 100  # No random critical hits in these journeys.
            return low

        def bounded_trace(frame, event, arg):
            nonlocal line_budget
            if event == "line" and frame.f_code.co_filename.startswith(str(ROOT)):
                line_budget -= 1
                if line_budget <= 0:
                    raise HarnessFailure("Game exceeded its line budget (possible loop)")
            return bounded_trace

        old_trace = sys.gettrace()
        old_bytecode = sys.dont_write_bytecode
        try:
            sys.dont_write_bytecode = True
            sys.settrace(bounded_trace)
            with contextlib.redirect_stdout(output), patch("builtins.input", game_input), patch(
                "random.randint", fixed_randint
            ):
                try:
                    runpy.run_path(str(MAIN), run_name="__main__")
                except GameStopped:
                    self.assertFalse(exits, "Expected game to exit")
                except SystemExit as error:
                    self.assertTrue(exits, "Game exited before the expected menu")
                    self.assertIn(error.code, (None, 0))
                else:
                    self.fail("Game returned without reaching the scripted destination")
        except HarnessFailure as error:
            self.fail(str(error))
        finally:
            sys.settrace(old_trace)
            sys.dont_write_bytecode = old_bytecode
        self.assertIsNone(next(script, None), "Game stopped with scripted inputs remaining")
        return last_state, output.getvalue()

    def house_inventory(self, updates=None):
        return [
            Step("mapmain", "1", updates=updates),
            Step("villagemap", "1"),
            Step("housec", "2"),
        ]

    def combat(self, updates=None):
        return [Step("mapmain", "3", updates=updates), Step("desertmap", "2")]

    def test_startup_and_navigation(self):
        self.play([
            Step("mapmain", "1"),
            Step("villagemap", "1"),
            Step("housec", "1"),
            Step("stat", "1"),
            Step("housec", "2"),
            Step("inventory", "5"),
            Step("housec", "4"),
            Step("villagemap", "2"),
            Step("shopc", "6"),
            Step("villagemap", "4"),
            Step("forgec", "4"),
            Step("villagemap", "3"),
            Step("innc", "3"),
            Step("villagemap", "7"),
            Step("mapmain", "3"),
            Step("desertmap", "1"),
            Step("mapmain"),
        ])

    def test_world_quit_exits_cleanly(self):
        self.play([Step("mapmain", "q")], exits=True)

    def test_empty_items_leave_and_use_preserve_inventory_and_health(self):
        for choice in ("2", "1"):
            with self.subTest(choice=choice):
                state, output = self.play(self.house_inventory({"p_hp": 50}) + [
                    Step("inventory", "1"),
                    Step("items", choice),
                    Step("inventory"),
                ])
                self.assertEqual(state["pot_n"], 0)
                self.assertEqual(state["p_hp"], 50)
                self.assertIn("leave items [2]", output)

    def test_home_potion_consumes_one_and_heals_rounded_quarter(self):
        state, _ = self.play(self.house_inventory({"pot_n": 3, "p_hp": 50, "p_max_hp": 101}) + [
            Step("inventory", "1"), Step("items", "1"), Step("inventory"),
        ])
        self.assertEqual(state["pot_n"], 2)
        self.assertEqual(state["p_hp"], 76)

    def test_potion_health_is_capped(self):
        state, _ = self.play(self.house_inventory({"pot_n": 1, "p_hp": 99}) + [
            Step("inventory", "1"), Step("items", "1"), Step("inventory"),
        ])
        self.assertEqual(state["pot_n"], 0)
        self.assertEqual(state["p_hp"], 100)

    def test_one_potion_per_use_in_every_encounter(self):
        for enemy, caller in enumerate(("cactus", "coyote", "spider", "snake", "camel"), 1):
            with self.subTest(enemy=caller):
                state, _ = self.play(self.combat({"pot_n": 3, "p_hp": 50, "p_max_hp": 101}) + [
                    Step(caller, "2"), Step("items", "1"), Step(caller),
                ], enemy=enemy)
                self.assertEqual(state["pot_n"], 2)
                self.assertEqual(state["p_hp"], 76)

    def test_empty_combat_items_do_not_create_potions_or_heal(self):
        for choice in ("1", "2"):
            with self.subTest(choice=choice):
                state, _ = self.play(self.combat({"p_hp": 50}) + [
                    Step("cactus", "2"), Step("items", choice), Step("cactus"),
                ])
                self.assertEqual(state["pot_n"], 0)
                self.assertEqual(state["p_hp"], 50)

    def test_can_flee_every_encounter(self):
        for enemy, caller in enumerate(("cactus", "coyote", "spider", "snake", "camel"), 1):
            with self.subTest(enemy=caller):
                self.play(self.combat() + [
                    Step(caller, "3"), Step("run", ""),
                    Step("desertmap", "1"), Step("mapmain"),
                ], enemy=enemy)

    def test_killed_enemies_cannot_retaliate(self):
        enemies = (
            ("cactus", "attack_cact", "cactus_dead"),
            ("coyote", "attack_coyo", "coyote_dead"),
            ("spider", "attack_spider", "spider_dead"),
            ("snake", "attack_snake", "snake_dead"),
            ("camel", "attack_camel", "camel_dead"),
        )
        for enemy, (caller, attack, dead) in enumerate(enemies, 1):
            with self.subTest(enemy=caller):
                state, _ = self.play(self.combat({"p_hp": 1, "p_dmg_min": 999, "p_dmg_max": 999}) + [
                    Step(caller, "1"), Step(attack, ""), Step(dead, ""), Step("desertmap"),
                ], enemy=enemy)
                self.assertEqual(state["p_hp"], 1)
                self.assertGreater(state["money"], 0)
                self.assertGreater(state["p_xp"], 0)

    def test_coyote_quest_kill_updates_progress(self):
        state, output = self.play(self.combat({
            "Task": True, "TaskCoyo": True, "ob": 0,
            "p_dmg_min": 999, "p_dmg_max": 999,
        }) + [
            Step("coyote", "1"), Step("attack_coyo", ""),
            Step("coyote_dead", ""), Step("desertmap"),
        ], enemy=2)
        self.assertEqual(state["ob"], 1)
        self.assertIn("collect 1 Coyote Fur", output)

    def test_coyote_quest_can_be_accepted_completed_and_claimed(self):
        state, _ = self.play([
            Step("mapmain", "1", updates={"p_dmg_min": 999, "p_dmg_max": 999}),
            Step("villagemap", "3"), Step("innc", "1"),
            Step("guyi", "2"), Step("guytask", "1"),
            Step("innc", "3", expected={"Task": True, "TaskCoyo": True, "ob": 0},
                 updates={"ob": 7}),
            Step("villagemap", "7"), Step("mapmain", "3"),
            Step("desertmap", "2"), Step("coyote", "1"),
            Step("attack_coyo", ""), Step("coyote_dead", ""),
            Step("desertmap", "1", expected={"ob": 8}), Step("mapmain", "1"),
            Step("villagemap", "3"), Step("innc", "1"), Step("guyi", "2"),
            Step("viewtask", "1"), Step("<module>", ""), Step("innc"),
        ], enemy=2)
        self.assertEqual(state["money"], 340)  # $40 loot plus the advertised $300 reward.
        self.assertFalse(state["Task"])
        self.assertFalse(state["TaskCoyo"])

    def test_experience_surplus_survives_multiple_level_ups(self):
        enemies = (
            ("cactus", "attack_cact", "cactus_dead", 3),
            ("coyote", "attack_coyo", "coyote_dead", 5),
            ("spider", "attack_spider", "spider_dead", 7),
            ("snake", "attack_snake", "snake_dead", 9),
            ("camel", "attack_camel", "camel_dead", 17),
        )
        for enemy, (caller, attack, dead, remainder) in enumerate(enemies, 1):
            with self.subTest(enemy=caller):
                state, _ = self.play(self.combat({
                    "p_xp": 220, "p_dmg_min": 999, "p_dmg_max": 999,
                }) + [
                    Step(caller, "1"), Step(attack, ""), Step(dead, ""),
                    Step("levelup", ""), Step("levelup", ""), Step("desertmap"),
                ], enemy=enemy)
                self.assertEqual(state["p_lvl"], 3)
                self.assertEqual(state["p_statpt"], 6)
                self.assertEqual(state["p_xp_lvl"], 157)
                self.assertEqual(state["p_xp"], remainder)

    def death_steps(self, choice):
        return self.combat({"p_hp": 1, "money": 500}) + [
            Step("cactus", "1"), Step("attack_cact", ""),
            Step("cactushit", ""), Step("defeated", choice),
        ]

    def test_cactus_death_can_quit(self):
        self.play(self.death_steps("2"), exits=True)

    def test_cactus_resurrection_returns_to_world(self):
        state, _ = self.play(self.death_steps("1") + [Step("mapmain")])
        self.assertEqual(state["money"], 250)
        self.assertEqual(state["p_hp"], state["p_max_hp"])
        self.assertFalse(state["desert"])
        self.assertFalse(state["Cactus"])

    def test_shop_reprompts_malformed_quantity_then_charges_correctly(self):
        steps = [Step("mapmain", "1", updates={"money": 100}),
                 Step("villagemap", "2"), Step("shopc", "1")]
        for value in ("1.5", "", "-1", "two", "1e2"):
            steps.extend([Step("buyc", value), Step("<module>", "")])
        steps.extend([Step("buyc", "2"), Step("shopc")])
        state, _ = self.play(steps)
        self.assertEqual(state["money"], 70)
        self.assertEqual(state["pot_n"], 2)

    def test_shop_zero_quantity_cancels_without_spending_money(self):
        state, _ = self.play([
            Step("mapmain", "1", updates={"money": 100}),
            Step("villagemap", "2"), Step("shopc", "1"),
            Step("buyc", "0"), Step("shopc"),
        ])
        self.assertEqual(state["money"], 100)
        self.assertEqual(state["pot_n"], 0)

    def equip(self, category, menu, choice):
        return [Step("inventory", category), Step(menu, choice), Step("<module>", "")]

    def test_equipment_speed_is_idempotent_and_unequips_cleanly(self):
        steps = self.house_inventory({"Slingshot_t": True, "Goggles_t": True})
        steps += self.equip("2", "weaps", "4") * 2
        steps += self.equip("4", "utility", "4") * 2
        steps += [Step("inventory", "4", expected={"p_spd": 16, "p_crit_c": .16}),
                  Step("utility", "1"), Step("<module>", "")]
        steps += self.equip("4", "utility", "1")
        steps += [Step("inventory", "2", expected={"p_spd": 10}),
                  Step("weaps", "1"), Step("<module>", "")]
        steps += self.equip("2", "weaps", "1")
        steps += [Step("inventory")]
        state, _ = self.play(steps)
        self.assertEqual(state["p_spd"], 5)
        self.assertEqual(state["p_crit_c"], .05)

    def test_armor_repeat_does_not_heal_and_stamina_keeps_base_hp_separate(self):
        steps = self.house_inventory({"Chain_t": True, "p_hp": 50, "p_statpt": 1})
        steps += self.equip("3", "arms", "4")
        steps += [Step("inventory", "3", expected={"p_hp": 50, "p_max_hp": 150}),
                  Step("arms", "4"), Step("<module>", "")]
        steps += [Step("inventory", "5", expected={"p_hp": 50}),
                  Step("housec", "3"), Step("statups", "2"),
                  Step("housec", "2", expected={"p_max_hp_b": 105, "p_max_hp": 155})]
        steps += self.equip("3", "arms", "1")
        steps += [Step("inventory")]
        state, _ = self.play(steps)
        self.assertEqual(state["p_stm"], 21)
        self.assertEqual(state["p_max_hp"], 105)
        self.assertLessEqual(state["p_hp"], 105)

    def test_unfinished_farm_returns_without_spending_money(self):
        state, output = self.play([
            Step("mapmain", "2", updates={"money": 100}),
            Step("<module>", ""), Step("mapmain"),
        ])
        self.assertEqual(state["money"], 100)
        self.assertFalse(state["Farm"])
        self.assertIn("never finished", output.lower())

    def test_unfinished_locations_return_to_their_map(self):
        for choice in ("4", "5", "6", "7", "8", "9", "10"):
            with self.subTest(world_choice=choice):
                self.play([
                    Step("mapmain", choice),
                    Step("<module>", "", prompt_contains="never finished"), Step("mapmain"),
                ])
        for choice in ("5", "6"):
            with self.subTest(village_choice=choice):
                self.play([
                    Step("mapmain", "1"), Step("villagemap", choice),
                    Step("<module>", "", prompt_contains="never finished"), Step("villagemap"),
                ])

    def test_active_game_sources_compile_with_warnings_as_errors(self):
        sources = [MAIN, *sorted((ROOT / "SSSDpak").glob("*.py"))]
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            for source in sources:
                with self.subTest(source=source.relative_to(ROOT)):
                    compile(source.read_text(encoding="utf-8"), str(source), "exec")


if __name__ == "__main__":
    unittest.main()
