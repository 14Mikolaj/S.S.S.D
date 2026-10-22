"""Turn-based encounters with readable intentions and no reward side effects."""

import random

from .content import ENEMIES
from .model import Player


class Battle:
    """An encounter owns temporary poison/guard state, not the player's rewards."""

    ACTIONS = {"attack", "power", "guard", "mend", "potion", "antidote", "flee"}

    def __init__(self, player: Player, enemy_id: str, rng: random.Random | None = None):
        self.player = player
        self.enemy_id = enemy_id
        self.enemy = dict(ENEMIES[enemy_id])
        self.enemy_hp = self.enemy["hp"]
        self.rng = rng if rng is not None else random.Random()
        self.turn = 0
        self.finished = player.hp <= 0
        self.result = "defeat" if self.finished else None
        self.poison_turns = 0
        self.enemy_guarding = False

    @property
    def intent(self) -> str:
        if self.finished:
            return "The encounter is over."
        return {
            "attack": "Preparing an ordinary attack.",
            "heavy": "Winding up a HEAVY strike. Guarding will blunt it.",
            "poison": "Preparing a poisonous attack. An antidote may come in handy.",
            "guard": "Preparing to guard; its next defense will be stronger.",
        }.get(self._enemy_action(), "Preparing an ordinary attack.")

    def _enemy_action(self) -> str:
        pattern = self.enemy.get("pattern") or ["attack"]
        return pattern[self.turn % len(pattern)]

    def _finish(self, result: str) -> None:
        self.result = result
        self.finished = True
        self.poison_turns = 0
        self.player.clamp_resources()

    def act(self, action: str) -> list[str]:
        if self.finished:
            return ["This encounter is already over."]
        if action not in self.ACTIONS:
            return ["Choose attack, power, guard, mend, potion, antidote, or flee."]
        player = self.player
        if action == "power" and player.energy < 3:
            return ["Power strike needs 3 energy. Attack or guard to recover some."]
        if action == "mend" and player.energy < 4:
            return ["Mend needs 4 energy. Attack or guard to recover some."]
        if action in {"potion", "mend"} and player.hp >= player.max_hp:
            return ["You are already at full health."]
        if action == "antidote" and not self.poison_turns:
            return ["You are not poisoned. Save the suspicious medicine."]
        if action in {"potion", "antidote"} and player.inventory.get(action, 0) < 1:
            return [f"You have no {action}s left."]

        messages = []
        enemy_action = self._enemy_action()
        guarding = action == "guard"
        if action in {"attack", "power"}:
            if action == "power":
                player.energy -= 3
                multiplier = 1.6
            else:
                player.energy = min(player.max_energy, player.energy + 1)
                multiplier = 1.0
            critical = self.rng.random() < player.crit
            raw_damage = round(player.attack * multiplier) + self.rng.randint(-2, 2)
            damage = max(1, raw_damage - self.enemy.get("defense", 0))
            if critical:
                damage = max(1, round(damage * 1.5))
            if self.enemy_guarding:
                damage = max(1, round(damage * 0.4))
                messages.append("The enemy's guard absorbs part of your blow.")
            self.enemy_guarding = False
            self.enemy_hp = max(0, self.enemy_hp - damage)
            move = "Power strike" if action == "power" else "Attack"
            messages.append(f"{move}{' CRITICAL' if critical else ''}: {damage} damage.")
        elif action == "guard":
            player.energy = min(player.max_energy, player.energy + 3)
            messages.append("You brace for impact and recover 3 energy.")
        elif action == "mend":
            player.energy -= 4
            amount = min(player.max_hp - player.hp, max(1, player.max_hp // 4))
            player.hp += amount
            messages.append(f"Mend restores {amount} health. Your organs accept the apology.")
        elif action == "potion":
            player.remove_item("potion")
            amount = min(player.max_hp - player.hp, max(1, player.max_hp * 2 // 5))
            player.hp += amount
            messages.append(f"One potion restores {amount} health.")
        elif action == "antidote":
            player.remove_item("antidote")
            self.poison_turns = 0
            messages.append("The antidote clears the poison.")
        elif action == "flee":
            chance = 0.45 if self.enemy.get("boss") else 0.65
            if self.rng.random() < chance:
                self.turn += 1
                self._finish("fled")
                return ["You escape. Tactical cowardice remains an essential life skill."]
            messages.append("Your escape is blocked!")

        if self.enemy_hp <= 0:
            self.turn += 1
            self._finish("victory")
            return [*messages, f"{self.enemy['name']} is defeated!"]

        if enemy_action == "guard":
            self.enemy_guarding = True
            messages.append(f"{self.enemy['name']} raises its guard.")
        else:
            multiplier = 1.6 if enemy_action == "heavy" else 1.0
            raw_damage = round(self.enemy["attack"] * multiplier) + self.rng.randint(-1, 1)
            damage = max(1, raw_damage - player.defense)
            if guarding:
                damage = max(1, round(damage * 0.3))
            player.hp = max(0, player.hp - damage)
            move = "heavy strike" if enemy_action == "heavy" else "attack"
            messages.append(f"{self.enemy['name']}'s {move} deals {damage} damage.")
            if enemy_action == "poison" and player.hp > 0:
                self.poison_turns = 3
                messages.append("Poison will sting for three turns. Antidote removes it.")

        if self.poison_turns and player.hp > 0:
            damage = max(1, player.max_hp // 20)
            player.hp = max(0, player.hp - damage)
            self.poison_turns -= 1
            messages.append(f"Poison deals {damage} damage ({self.poison_turns} turns remain).")
        self.turn += 1
        player.clamp_resources()
        if player.hp <= 0:
            self._finish("defeat")
            messages.append("You fall. The village healer has seen worse. Probably.")
        return messages
