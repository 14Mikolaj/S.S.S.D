"""World rules and progression, independent of terminal input and save files."""

from functools import wraps
import random

from .combat import Battle
from .content import DIALOGUE, ENEMIES, ITEMS, LOCATIONS, QUESTS, RECIPES, STORY_BEATS
from .model import GameState
from .secrets import CrowGame, SECRETS


SHOP_STOCK = ("potion", "antidote", "iron_sword", "iron_armor", "hunter_bow",
              "wanderer_cloak", "travel_boots", "silver_ring")
SEALS = ("seal_root", "seal_stone", "seal_tide")


def world_action(method):
    """World services cannot bypass an encounter or resurrect a combatant."""
    @wraps(method)
    def guarded(self, *args, **kwargs):
        if self.battle is not None:
            return ["Finish the encounter or flee before doing that."]
        return method(self, *args, **kwargs)
    return guarded


class Game:
    def __init__(self, state=None, seed=None):
        self.state = state if state is not None else GameState()
        self.rng = random.Random(seed)
        self.battle = None
        self._crow_game = None

    @property
    def player(self):
        return self.state.player

    def _advance(self, steps=1):
        self.state.steps += steps
        self.state.day = 1 + self.state.steps // 6

    def _note(self, message):
        self.state.journal.append(message)
        self.state.journal = self.state.journal[-50:]

    def _count(self, key, amount=1):
        self.state.progress[key] = self.state.progress.get(key, 0) + amount

    @staticmethod
    def _quantity(qty):
        return type(qty) is int and 1 <= qty <= 99

    @world_action
    def investigate(self):
        secret = SECRETS.get(self.state.location)
        if secret is None:
            return ["Nothing unusual catches your eye here. Unusual by Assonance's standards, anyway."]
        flag = "secret:" + secret["id"]
        messages = [secret["title"], secret["description"]]
        if flag not in self.state.flags:
            self.state.flags.add(flag)
            self._note("Discovered: " + secret["title"] + ".")
            messages.append("A small discovery, safely tucked into your journal.")
        return messages

    @world_action
    def secret_action(self, choice):
        secret = SECRETS.get(self.state.location)
        if secret is None or not isinstance(choice, str) or choice not in dict(secret["actions"]):
            return ["That curiosity is not here. The world declines your creative interpretation of geography."]
        messages = self.investigate()
        messages.extend(secret["responses"][choice])
        if choice == secret.get("reward_action"):
            flag = "secret_reward:" + secret["id"]
            if flag in self.state.flags:
                messages.append("You already collected this little keepsake. The joke, unfortunately, is renewable.")
            else:
                self.state.flags.add(flag)
                for item, quantity in secret.get("reward", {}).items():
                    self.player.add_item(item, quantity)
                    messages.append(f"Received {quantity} x {ITEMS[item]['name']}.")
                self._note("Solved the curiosity: " + secret["title"] + ".")
        return messages

    def start_crow_game(self):
        """Return a fresh transient board only while safely at the farm."""
        if self.battle is not None or self.state.location != "farm":
            return None
        self.investigate()
        self._crow_game = CrowGame()
        return self._crow_game

    @world_action
    def claim_crow_prize(self, session):
        if self.state.location != "farm":
            return ["The crow's prize table is at the farm."]
        if not isinstance(session, CrowGame) or session is not self._crow_game:
            return ["The crow needs to see a game played at this table. A confident claim is not a scorecard."]
        result = session.verified_result()
        if result is None:
            return ["Finish a legal game before collecting a prize."]
        self._crow_game = None
        self._count("crow:played")
        if result == "loss":
            return ["No prize this time, but no money lost. The crow offers another free game."]
        self._count("crow:won" if result == "win" else "crow:drawn")
        if "crow_prize" in self.state.flags:
            return ["Another fine game! Your first-win-or-draw prize is already collected. "
                    "The crow pays you in slightly resentful respect."]
        self.state.flags.add("crow_prize")
        self.player.gold += 12
        self.player.add_item("herb", 2)
        self._note("Matched wits with the farm crow and earned its one-time prize.")
        return ["The crow counts out 12 gold and 2 herbs. 'Promotional budget,' it mutters.",
                "First win or draw prize collected! Further games are free, for bragging rights."]

    def objective_progress(self, objective):
        if objective.startswith("own:"):
            return self.player.inventory.get(objective.split(":", 1)[1], 0)
        return self.state.progress.get(objective, 0)

    def _quarry(self, enemies):
        """Follow useful quest tracks instead of making early jobs an RNG grind."""
        for quest_id, status in self.state.quests.items():
            if status != "active":
                continue
            for key, total in QUESTS[quest_id]["objectives"].items():
                if self.objective_progress(key) >= total:
                    continue
                kind, target = key.split(":", 1)
                if kind == "kill" and target in enemies:
                    return target
                if kind == "own":
                    for enemy_id in enemies:
                        if target in ENEMIES[enemy_id].get("loot", {}):
                            return enemy_id
        return None

    @world_action
    def move(self, destination):
        location = LOCATIONS[self.state.location]
        if destination not in location["neighbors"]:
            return ["There is no road there from here. Even heroic shortcuts need a road."]
        if destination == "castle" and not all(seal in self.state.flags for seal in SEALS):
            missing = [seal.removeprefix("seal_") for seal in SEALS if seal not in self.state.flags]
            return ["The castle gate is sealed. Recover the " + ", ".join(missing) + " seals first."]
        self.state.location = destination
        self.state.visited.add(destination)
        self._advance()
        place = LOCATIONS[destination]
        return [f"You arrive at {place['name']}.", place["description"]]

    @world_action
    def explore(self):
        place_id = self.state.location
        place = LOCATIONS[place_id]
        if place_id == "village":
            return ["Kieth has news at the inn. The smith, shop, and quest board are open."]
        if place_id == "farm":
            return self.harvest()
        self._advance()
        self._count("explore:" + place_id)
        messages = [f"You explore {place['name']}."]
        resources = place.get("resources", {})
        if resources:
            item_id = self.rng.choice(list(resources))
            amount = resources[item_id]
            self.player.add_item(item_id, amount)
            messages.append(f"Found {amount} x {ITEMS[item_id]['name']}.")
        if place.get("boss") and self.state.progress["explore:" + place_id] == 2:
            discovery = f"A path to {ENEMIES[place['boss']]['name']} is open at {place['name']}."
            messages.append(discovery + " Use Challenge when ready.")
            self._note(discovery)
        enemies = place.get("enemies", [])
        if enemies and self.rng.random() < .70:
            quarry = self._quarry(enemies)
            enemy_id = quarry or self.rng.choice(enemies)
            if quarry:
                messages.append("You follow tracks toward an unfinished village job.")
            self.battle = Battle(self.player, enemy_id, self.rng)
            messages += [f"Encounter: {ENEMIES[enemy_id]['name']}!", ENEMIES[enemy_id]["description"]]
        else:
            messages.append(self.rng.choice([
                "You find old bootprints beside claw marks. At least someone brought shoes.",
                "For a moment, the wind sounds like David humming the old ward-song.",
                "A weathered milestone points toward Assonance. Someone has added 'probably'.",
                "The road is quiet. You regain 2 energy and appreciate the suspicious lack of danger.",
            ]))
            self.player.energy = min(self.player.max_energy, self.player.energy + 2)
        return messages

    @world_action
    def challenge(self):
        place = LOCATIONS[self.state.location]
        enemy_id = place.get("boss")
        if not enemy_id:
            return ["There is no guardian here. The locals decline your dramatic challenge."]
        if "boss:" + enemy_id in self.state.flags:
            return ["This guardian is already defeated. The road remembers what you did."]
        if "story_started" not in self.state.flags:
            return ["Speak to Kieth in the village first. He knows why the guardians are waking."]
        if self.state.progress.get("explore:" + self.state.location, 0) < 2:
            return ["Explore this region twice to find the guardian's refuge."]
        self.battle = Battle(self.player, enemy_id, self.rng)
        return [f"You face {ENEMIES[enemy_id]['name']}.", ENEMIES[enemy_id]["description"]]

    def combat(self, action):
        if self.battle is None:
            return ["There is nothing to fight here. Your shadow is not accepting challenges."]
        encounter = self.battle
        messages = encounter.act(action)
        if not encounter.finished:
            return messages
        self.battle = None
        if encounter.result == "victory":
            enemy = encounter.enemy
            self.player.gold += enemy["gold"]
            self._count("kill:" + encounter.enemy_id)
            messages.append(f"Earned {enemy['gold']} gold and {enemy['xp']} experience.")
            for item_id, amount in enemy.get("loot", {}).items():
                self.player.add_item(item_id, amount)
                messages.append(f"Loot: {amount} x {ITEMS[item_id]['name']}.")
            messages += self.player.gain_xp(enemy["xp"])
            if LOCATIONS[self.state.location].get("boss") == encounter.enemy_id:
                self.state.flags.add("boss:" + encounter.enemy_id)
                seal = LOCATIONS[self.state.location].get("seal")
                if seal:
                    self.state.flags.add(seal)
                    messages += STORY_BEATS[seal]
                    self._note(f"Recovered the {seal.removeprefix('seal_')} seal.")
                elif encounter.enemy_id == "storm_drake":
                    messages += STORY_BEATS["storm_drake"]
                    self._note("The storm drake's watch has ended. The mountains are quiet.")
                elif encounter.enemy_id == "hollow_king":
                    self.state.flags.add("finale_ready")
                    messages += STORY_BEATS["finale"]
                    self._note("The Hollow King has fallen. David's fate is in your hands.")
        elif encounter.result == "defeat":
            lost = self.player.gold // 10
            self.player.gold -= lost
            self.state.location = "village"
            self._advance(6)
            self.player.hp = self.player.max_hp
            self.player.energy = self.player.max_energy
            messages += [f"You wake in the village. Rescue cost {lost} gold; your gear and progress are safe.",
                         "Jimmy calls it a tactical nap. Kieth has already put it on the noticeboard."]
        return messages

    @world_action
    def rest(self):
        self._advance(6)
        if self.state.location in {"village", "farm"}:
            self.player.hp = self.player.max_hp
            self.player.energy = self.player.max_energy
            return [f"Day {self.state.day}: a proper night's rest restores all health and energy.",
                    "The bed is free. Jimmy says your survival is good for repeat business."]
        self.player.hp = min(self.player.max_hp, self.player.hp + max(1, self.player.max_hp * 3 // 10))
        self.player.energy = min(self.player.max_energy, self.player.energy + max(1, self.player.max_energy // 2))
        return [f"Day {self.state.day}: camp restores 30% health and half your energy.",
                "Nothing attacks your tent. Its structural integrity does that job for free."]

    @world_action
    def talk(self, npc="kieth"):
        available = {"village": {"kieth", "jimmy", "smith"}, "farm": {"farmer"}}
        if npc not in available.get(self.state.location, set()):
            return ["That person is not here."]
        messages = list(DIALOGUE[npc])
        if npc == "kieth" and "story_started" not in self.state.flags:
            self.state.flags.add("story_started")
            messages += STORY_BEATS["warning"]
            self._note("Kieth asked me to find David's three seals in the forest, caves, and sea.")
            if "trail_watch" not in self.state.quests:
                self.state.quests["trail_watch"] = "active"
                messages.append("Quest accepted: " + QUESTS["trail_watch"]["name"] + ". Check your journal.")
        elif npc == "kieth":
            messages += self._next_objective()
        return messages

    @world_action
    def harvest(self):
        if self.state.location != "farm":
            return ["The farm is the place for harvesting. Pavement soup is not a recipe."]
        if self.state.harvest_day >= self.state.day:
            return ["Today's herbs are gathered. Rest or travel until another day before harvesting again."]
        self.state.harvest_day = self.state.day
        self.player.add_item("herb", 3)
        return ["You help the farmer weed the beds and receive 3 herbs.",
                "He warns that some weeds bite. You have met the cacti; you believe him."]

    @world_action
    def accept_quest(self, quest_id):
        if self.state.location != "village":
            return ["Visit the village noticeboard to take a job."]
        if quest_id not in QUESTS:
            return ["That job is not on the noticeboard."]
        if quest_id in self.state.quests:
            return ["You have already taken or completed that job."]
        self.state.quests[quest_id] = "active"
        quest = QUESTS[quest_id]
        return [f"Quest accepted: {quest['name']}.", quest["description"]]

    @world_action
    def claim_quest(self, quest_id):
        if self.state.location != "village":
            return ["Return to the village to hand in a quest."]
        if self.state.quests.get(quest_id) != "active":
            return ["That quest is not awaiting a reward."]
        quest = QUESTS[quest_id]
        if any(self.objective_progress(key) < amount for key, amount in quest["objectives"].items()):
            return ["That job is not finished yet. Check the journal for your progress."]
        for key, amount in quest["objectives"].items():
            if key.startswith("own:"):
                self.player.remove_item(key.split(":", 1)[1], amount)
        self.state.quests[quest_id] = "complete"
        reward = quest["reward"]
        self.player.gold += reward.get("gold", 0)
        messages = [f"Completed: {quest['name']}. Earned {reward.get('gold', 0)} gold and {reward.get('xp', 0)} XP."]
        messages += self.player.gain_xp(reward.get("xp", 0))
        for item_id, amount in reward.get("items", {}).items():
            self.player.add_item(item_id, amount)
            messages.append(f"Reward: {amount} x {ITEMS[item_id]['name']}.")
        self._note("Completed " + quest["name"] + ".")
        return messages

    @world_action
    def buy(self, item_id, qty=1):
        if self.state.location != "village":
            return ["The shop is in the village."]
        if item_id not in SHOP_STOCK or not self._quantity(qty):
            return ["Choose an item in stock and a quantity from 1 to 99."]
        item = ITEMS[item_id]
        cost = item["price"] * qty
        if self.player.gold < cost:
            return [f"That costs {cost} gold. You have {self.player.gold}."]
        self.player.gold -= cost
        self.player.add_item(item_id, qty)
        return [f"Bought {qty} x {item['name']} for {cost} gold."]

    @world_action
    def sell(self, item_id, qty=1):
        if self.state.location != "village":
            return ["The village shop buys surplus supplies."]
        if item_id not in ITEMS or not self._quantity(qty):
            return ["Choose an owned item and a quantity from 1 to 99."]
        if not self.player.remove_item(item_id, qty):
            return ["You do not have enough spare copies. Unequip gear before selling the last copy."]
        value = max(1, ITEMS[item_id]["price"] // 2) * qty
        self.player.gold += value
        if item_id not in self.player.inventory:
            self.player.upgrades.pop(item_id, None)
        return [f"Sold {qty} x {ITEMS[item_id]['name']} for {value} gold."]

    @world_action
    def equip(self, item_id):
        if item_id.startswith("unequip:"):
            slot = item_id.split(":", 1)[1]
            if slot not in self.player.equipment:
                return ["That equipment slot does not exist."]
            self.player.equipment[slot] = None
            self.player.clamp_resources()
            return [f"Unequipped {slot}."]
        return self.player.equip(item_id)

    @world_action
    def use(self, item_id):
        if item_id == "antidote":
            return ["You are not poisoned outside combat. Keep the antidote for a fight."]
        if item_id != "potion" or self.player.inventory.get(item_id, 0) < 1:
            return ["There is no usable potion in your pack."]
        if self.player.hp >= self.player.max_hp:
            return ["You are already at full health."]
        self.player.remove_item("potion")
        healing = min(self.player.max_hp - self.player.hp, max(1, self.player.max_hp * 2 // 5))
        self.player.hp += healing
        return [f"One potion restores {healing} health."]

    @world_action
    def craft(self, recipe_id):
        if self.state.location != "village":
            return ["Use the smith's workbench in the village."]
        if recipe_id not in RECIPES:
            return ["That recipe is not known."]
        recipe = RECIPES[recipe_id]
        if self.player.gold < recipe["gold"]:
            return [f"Crafting needs {recipe['gold']} gold."]
        for item_id, amount in recipe["ingredients"].items():
            spare = self.player.inventory.get(item_id, 0) - int(item_id in self.player.equipment.values())
            if spare < amount:
                return [f"Need {amount} spare {ITEMS[item_id]['name']}. Unequip ingredients before crafting."]
        for item_id, amount in recipe["ingredients"].items():
            self.player.remove_item(item_id, amount)
            if item_id not in self.player.inventory:
                self.player.upgrades.pop(item_id, None)
        self.player.gold -= recipe["gold"]
        self.player.add_item(recipe["produces"], recipe["quantity"])
        return [f"Crafted {recipe['quantity']} x {ITEMS[recipe['produces']]['name']}."]

    @world_action
    def upgrade(self, item_id):
        if self.state.location != "village":
            return ["The village smith handles upgrades."]
        if item_id not in ITEMS or ITEMS[item_id]["kind"] not in {"weapon", "armor"}:
            return ["Choose a weapon or armour to upgrade."]
        if not self.player.inventory.get(item_id):
            return ["You do not own that equipment."]
        tier = self.player.upgrades.get(item_id, 0) + 1
        if tier > 3:
            return ["That item is already at its maximum upgrade (+3)."]
        crystals = 1 if tier > 1 else 0
        if (self.player.gold < 20 * tier or self.player.inventory.get("ore", 0) < tier
                or self.player.inventory.get("crystal", 0) < crystals):
            return [f"Upgrade +{tier} needs {20 * tier} gold, {tier} ore and {crystals} crystal."]
        self.player.gold -= 20 * tier
        self.player.remove_item("ore", tier)
        if crystals:
            self.player.remove_item("crystal", crystals)
        self.player.upgrades[item_id] = tier
        return [f"{ITEMS[item_id]['name']} is now +{tier}."]

    @world_action
    def train(self, stat):
        if stat not in {"strength", "vitality", "agility"}:
            return ["Choose strength, vitality, or agility."]
        if self.player.stat_points < 1:
            return ["Earn a level to gain more attribute points."]
        old_hp, old_energy = self.player.max_hp, self.player.max_energy
        setattr(self.player, stat, getattr(self.player, stat) + 1)
        self.player.stat_points -= 1
        self.player.hp += self.player.max_hp - old_hp
        self.player.energy += self.player.max_energy - old_energy
        self.player.clamp_resources()
        return [f"{stat.title()} increased to {getattr(self.player, stat)}."]

    @world_action
    def finish(self, ending):
        if ending not in {"restore", "release"}:
            return ["Choose restore or release."]
        if "finale_ready" not in self.state.flags or self.state.location != "castle":
            return ["Your story has not reached that decision yet."]
        if self.state.ending is not None:
            return ["Your choice is already part of Assonance's history. The roads remain open."]
        self.state.ending = ending
        self.state.flags.add("ended")
        self._note("Chose to " + ending + " David's wards. The story is complete.")
        return [*STORY_BEATS["ending_" + ending],
                "THE END — for now. You can keep exploring and finish any remaining jobs."]

    def _next_objective(self):
        if self.state.ending:
            return ["The story is complete. Explore freely or finish the remaining village jobs."]
        if "story_started" not in self.state.flags:
            return ["Next: speak with Kieth at the village inn about David's disappearance."]
        if "finale_ready" in self.state.flags:
            return ["Next: return to the castle and choose whether to restore the wards or release David."]
        missing = [("seal_root", "forest"), ("seal_stone", "caves"), ("seal_tide", "sea")]
        targets = [LOCATIONS[place]["name"] for flag, place in missing if flag not in self.state.flags]
        if targets:
            return ["Next: explore twice and challenge the wardens at " + ", ".join(targets) + ".",
                    "Train, upgrade your gear, and take village jobs if a guardian is too strong."]
        return ["Next: cross the bridge to the castle. Explore twice, then face the Hollow King."]

    def journal(self):
        messages = self._next_objective()
        recovered = [seal.removeprefix("seal_") for seal in SEALS if seal in self.state.flags]
        messages.append("Seals recovered: " + (", ".join(recovered) if recovered else "none") + ".")
        for quest_id, status in self.state.quests.items():
            quest = QUESTS[quest_id]
            messages.append(f"[{status}] {quest['name']}: {quest['description']}")
            if status == "active":
                for key, total in quest["objectives"].items():
                    kind, target = key.split(":", 1)
                    catalog = ITEMS if kind == "own" else ENEMIES if kind == "kill" else LOCATIONS
                    name = catalog[target]["name"]
                    messages.append(f"  {kind.title()} {name}: {min(self.objective_progress(key), total)}/{total}")
        if self.state.journal:
            messages.append("Recent memories:")
            messages.extend(self.state.journal[-6:])
        return messages
