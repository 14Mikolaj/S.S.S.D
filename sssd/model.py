"""Small, explicit game state; equipped bonuses are always derived, never stacked."""

from dataclasses import dataclass, field

from .content import ITEMS


def _quantity(value: int) -> bool:
    return type(value) is int and value > 0


@dataclass
class Player:
    name: str = "Xehspfe"
    level: int = 1
    xp: int = 0
    gold: int = 35
    hp: int = 60
    energy: int = 8
    strength: int = 5
    vitality: int = 5
    agility: int = 5
    stat_points: int = 0
    inventory: dict[str, int] = field(default_factory=lambda: {
        "rusty_sword": 1, "tunic": 1, "potion": 3, "antidote": 1,
    })
    equipment: dict[str, str | None] = field(default_factory=lambda: {
        "weapon": "rusty_sword", "armor": "tunic", "charm": None,
    })
    upgrades: dict[str, int] = field(default_factory=dict)

    def _bonus(self, key: str) -> int:
        return sum(ITEMS.get(item_id, {}).get(key, 0)
                   for item_id in self.equipment.values() if item_id)

    @property
    def max_hp(self) -> int:
        return 30 + self.vitality * 6 + self._bonus("hp")

    @property
    def max_energy(self) -> int:
        return 6 + self.agility // 2 + self._bonus("energy")

    @property
    def attack(self) -> int:
        weapon = self.equipment.get("weapon")
        return 3 + self.strength * 2 + self._bonus("attack") + self.upgrades.get(weapon, 0) * 2

    @property
    def defense(self) -> int:
        armor = self.equipment.get("armor")
        return self.vitality // 3 + self._bonus("defense") + self.upgrades.get(armor, 0)

    @property
    def crit(self) -> float:
        return min(0.35, 0.05 + self.agility * 0.01)

    @property
    def xp_to_next(self) -> int:
        return 35 + 25 * self.level

    def clamp_resources(self) -> None:
        self.hp = max(0, min(self.hp, self.max_hp))
        self.energy = max(0, min(self.energy, self.max_energy))

    def add_item(self, item_id: str, qty: int = 1) -> None:
        if item_id not in ITEMS or not _quantity(qty):
            raise ValueError("Items must exist and quantities must be positive whole numbers.")
        self.inventory[item_id] = self.inventory.get(item_id, 0) + qty

    def remove_item(self, item_id: str, qty: int = 1) -> bool:
        if not _quantity(qty) or self.inventory.get(item_id, 0) < qty:
            return False
        remaining = self.inventory[item_id] - qty
        if remaining == 0 and item_id in self.equipment.values():
            return False
        if remaining:
            self.inventory[item_id] = remaining
        else:
            del self.inventory[item_id]
        return True

    def equip(self, item_id: str) -> list[str]:
        item = ITEMS.get(item_id)
        if item is None or self.inventory.get(item_id, 0) < 1:
            return ["You do not own that item. Imaginary swords have terrible reach."]
        slot = item.get("slot")
        if slot not in self.equipment:
            return ["That cannot be equipped. Please stop wearing the supplies."]
        if self.equipment[slot] == item_id:
            return [f"{item['name']} is already equipped."]
        self.equipment[slot] = item_id
        self.clamp_resources()
        return [f"Equipped {item['name']}."]

    def gain_xp(self, amount: int) -> list[str]:
        if type(amount) is not int or amount < 0:
            raise ValueError("Experience must be a nonnegative whole number.")
        self.xp += amount
        messages = []
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.strength += 1
            self.vitality += 1
            self.agility += 1
            self.stat_points += 3
            self.hp = self.max_hp
            self.energy = self.max_energy
            messages.append(
                f"Level {self.level}! All attributes +1, three points to spend, "
                "health and energy restored. Suspiciously convenient personal growth."
            )
        return messages


@dataclass
class GameState:
    player: Player = field(default_factory=Player)
    location: str = "village"
    day: int = 1
    steps: int = 0
    flags: set[str] = field(default_factory=set)
    quests: dict[str, str] = field(default_factory=dict)
    progress: dict[str, int] = field(default_factory=dict)
    visited: set[str] = field(default_factory=lambda: {"village"})
    harvest_day: int = 0
    ending: str | None = None
    journal: list[str] = field(default_factory=list)
