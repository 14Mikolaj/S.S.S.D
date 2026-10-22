"""Original words, world data, and terrible cactus jokes for S.S.S.D.

The old game's names and eccentric fantasy tone are deliberate. Content is
plain data so the rules and terminal interface can use the same source.
"""

ITEMS = {
    "rusty_sword": {
        "name": "Reliably Rusty Sword", "kind": "weapon", "slot": "weapon",
        "price": 8, "attack": 2,
        "description": "Your old sword. Mostly iron; partly a historical document.",
    },
    "tunic": {
        "name": "Patchwork Tunic", "kind": "armor", "slot": "armor",
        "price": 6, "defense": 1,
        "description": "Jimmy repaired the holes. The patches have little ducks on them.",
    },
    "potion": {
        "name": "Healing Potion", "kind": "consumable", "slot": None,
        "price": 16,
        "description": "Restores 40% of maximum health. Tastes like heroic cough syrup.",
    },
    "antidote": {
        "name": "Antidote", "kind": "consumable", "slot": None,
        "price": 12,
        "description": "Cures poison. The label says NOT SOUP in three languages.",
    },
    "herb": {
        "name": "Greenwhisper Herb", "kind": "material", "slot": None,
        "price": 3,
        "description": "A healing plant that quietly objects to being picked.",
    },
    "ore": {
        "name": "Iron Ore", "kind": "material", "slot": None,
        "price": 5,
        "description": "Useful metal patiently waiting to become something pointy.",
    },
    "crystal": {
        "name": "Echo Crystal", "kind": "material", "slot": None,
        "price": 9,
        "description": "A shard of old ward-magic. Hold it close and hear rain.",
    },
    "venom": {
        "name": "Sealed Venom Vial", "kind": "material", "slot": None,
        "price": 5,
        "description": "For antidotes and research. Please do not lick the research.",
    },
    "coyote_pelt": {
        "name": "Coyote Pelt", "kind": "material", "slot": None,
        "price": 7,
        "description": "Warm enough for the mountain road and Jimmy's draughty inn.",
    },
    "dragon_scale": {
        "name": "Storm Drake Scale", "kind": "material", "slot": None,
        "price": 45,
        "description": "It remembers lightning. The forge can make it remember dawn.",
    },
    "iron_sword": {
        "name": "Proper Iron Sword", "kind": "weapon", "slot": "weapon",
        "price": 65, "attack": 7,
        "description": "The smith insists that being straight is a major improvement.",
    },
    "hunter_bow": {
        "name": "Hunter's Bow", "kind": "weapon", "slot": "weapon",
        "price": 80, "attack": 6, "energy": 2,
        "description": "Light and balanced. Grants extra energy for combat techniques.",
    },
    "root_staff": {
        "name": "Living Root Staff", "kind": "weapon", "slot": "weapon",
        "price": 105, "attack": 9, "hp": 8,
        "description": "A willing branch of Thenttkil, still warm with summer sap.",
    },
    "dawn_blade": {
        "name": "Dawn Blade", "kind": "weapon", "slot": "weapon",
        "price": 230, "attack": 17, "energy": 1,
        "description": "Forged from a storm. Its light makes the dark reconsider.",
    },
    "iron_armor": {
        "name": "Mended Iron Armor", "kind": "armor", "slot": "armor",
        "price": 65, "defense": 4,
        "description": "An honest set of plates, with only a little embarrassing squeak.",
    },
    "wanderer_cloak": {
        "name": "Wanderer's Cloak", "kind": "armor", "slot": "armor",
        "price": 85, "defense": 3, "energy": 2,
        "description": "Room for tricks, snacks, and an unnecessarily dramatic turn.",
    },
    "dusk_armor": {
        "name": "Duskguard Armor", "kind": "armor", "slot": "armor",
        "price": 155, "defense": 8, "hp": 10,
        "description": "Crystal-lined armor that holds its wearer together after sunset.",
    },
    "ward_charm": {
        "name": "Shared Ward Charm", "kind": "charm", "slot": "charm",
        "price": 90, "defense": 2, "hp": 15,
        "description": "A small promise: protection should be something people share.",
    },
    "travel_boots": {
        "name": "Definitely Adventuring Boots", "kind": "charm", "slot": "charm",
        "price": 45, "energy": 2,
        "description": "Dry socks, firm footing, and extra energy. Truly legendary.",
    },
    "silver_ring": {
        "name": "Jimmy's Lucky Ring", "kind": "charm", "slot": "charm",
        "price": 70, "attack": 2, "hp": 6,
        "description": "Jimmy calls it lucky because the previous owner paid their tab.",
    },
}


ENEMIES = {
    "cactus": {
        "name": "Deeply Offended Cactus", "hp": 24, "attack": 5,
        "defense": 1, "xp": 12, "gold": 9,
        "pattern": ["attack", "guard", "heavy"],
        "description": "It has no arms, yet somehow it is squaring up.",
        "loot": {"herb": 1},
    },
    "coyote": {
        "name": "Dust Coyote", "hp": 33, "attack": 7,
        "defense": 1, "xp": 16, "gold": 12,
        "pattern": ["attack", "attack", "heavy"],
        "description": "Ward-sickness has driven it from the hills to the road.",
        "loot": {"coyote_pelt": 1},
    },
    "spider": {
        "name": "Unreasonably Large Spider", "hp": 32, "attack": 6,
        "defense": 1, "xp": 16, "gold": 10,
        "pattern": ["poison", "attack", "guard"],
        "description": "Its web includes a tiny sign reading PRIVATE PROPERTY.",
        "loot": {"venom": 1},
    },
    "snake": {
        "name": "Glassfang Snake", "hp": 38, "attack": 8,
        "defense": 2, "xp": 20, "gold": 13,
        "pattern": ["attack", "poison", "attack", "heavy"],
        "description": "A beautiful shimmer, followed by a very practical problem.",
        "loot": {"venom": 1},
    },
    "camel": {
        "name": "Camel With An Agenda", "hp": 52, "attack": 10,
        "defense": 3, "xp": 25, "gold": 18,
        "pattern": ["guard", "heavy", "attack"],
        "description": "Nobody knows its agenda. Everyone suspects it involves spitting.",
        "loot": {"herb": 2},
    },
    "wolf": {
        "name": "Briar Wolf", "hp": 55, "attack": 11,
        "defense": 3, "xp": 27, "gold": 18,
        "pattern": ["attack", "heavy", "attack", "guard"],
        "description": "Black thorns grow through the shadows beneath its fur.",
        "loot": {"herb": 1},
    },
    "bandit": {
        "name": "Self-Appointed Toll Collector", "hp": 60, "attack": 12,
        "defense": 3, "xp": 30, "gold": 28,
        "pattern": ["attack", "guard", "heavy"],
        "description": "Their official badge is a potato with OFFICIAL scratched on it.",
        "loot": {"potion": 1},
    },
    "wisp": {
        "name": "Lost Echo", "hp": 46, "attack": 12,
        "defense": 2, "xp": 29, "gold": 20,
        "pattern": ["poison", "attack", "heavy", "guard"],
        "description": "A memory without a person, lashing out because it cannot sleep.",
        "loot": {"crystal": 1},
    },
    "sentinel": {
        "name": "Broken Ward Sentinel", "hp": 82, "attack": 15,
        "defense": 5, "xp": 42, "gold": 30,
        "pattern": ["guard", "heavy", "attack", "heavy"],
        "description": "It still protects the realm. It has forgotten from whom.",
        "loot": {"ore": 2, "crystal": 1},
    },
    "root_guardian": {
        "name": "The Grieving Root", "hp": 108, "attack": 14,
        "defense": 4, "xp": 85, "gold": 55, "boss": True,
        "pattern": ["guard", "heavy", "poison", "attack"],
        "description": "Thenttkil's oldest root clenches around a familiar druid's voice.",
        "loot": {"crystal": 2, "herb": 3, "root_staff": 1},
    },
    "cave_guardian": {
        "name": "The Unfinished Colossus", "hp": 128, "attack": 16,
        "defense": 6, "xp": 100, "gold": 65, "boss": True,
        "pattern": ["attack", "guard", "heavy", "heavy"],
        "description": "Its stone heart beats around the second fragment of David's ward.",
        "loot": {"ore": 4, "crystal": 2},
    },
    "tide_wraith": {
        "name": "The Drowned Bell", "hp": 148, "attack": 18,
        "defense": 4, "xp": 120, "gold": 80, "boss": True,
        "pattern": ["poison", "guard", "heavy", "attack", "heavy"],
        "description": "Each toll carries a promise that someone was too afraid to keep.",
        "loot": {"crystal": 4, "potion": 2},
    },
    "storm_drake": {
        "name": "Crownless Storm Drake", "hp": 195, "attack": 22,
        "defense": 7, "xp": 155, "gold": 110, "boss": True,
        "pattern": ["attack", "heavy", "guard", "heavy", "poison"],
        "description": "A mountain-sized temper in a merely enormous dragon. Optional.",
        "loot": {"dragon_scale": 1, "crystal": 3},
    },
    "hollow_king": {
        "name": "The Hollow King", "hp": 250, "attack": 25,
        "defense": 8, "xp": 230, "gold": 180, "boss": True,
        "pattern": ["guard", "heavy", "poison", "attack", "heavy"],
        "description": "A crown on an empty suit of armor, speaking with stolen voices.",
        "loot": {"crystal": 5},
    },
}


LOCATIONS = {
    "village": {
        "name": "Little Jimmy's Village", "level": 1,
        "description": "The inn's crooked sign creaks above warm windows. Kieth waits "
        "by the well; the smith's forge still rings. Here, at least, the lamps stay lit.",
        "neighbors": ["farm", "desert", "forest", "bridge"],
        "enemies": [], "resources": {},
    },
    "farm": {
        "name": "The Extremely Normal Farm", "level": 1,
        "description": "Beet rows run toward a suspiciously mobile cactus. The farmer "
        "is trying to grow food in a world increasingly interested in growing teeth.",
        "neighbors": ["village", "plains"],
        "enemies": ["cactus", "coyote"], "resources": {"herb": 2},
    },
    "desert": {
        "name": "The Impolite Desert", "level": 1,
        "description": "Red dunes swallow the old caravan road. Cacti glare, snakes "
        "glitter, and a camel appears to be organizing some sort of resistance.",
        "neighbors": ["village", "caves"],
        "enemies": ["cactus", "coyote", "snake", "camel"],
        "resources": {"herb": 1, "ore": 1},
    },
    "caves": {
        "name": "The Echoing Caves", "level": 3,
        "description": "Old mining tracks descend into blue crystal light. Your "
        "footsteps return a moment late, followed by a second pair that is not yours.",
        "neighbors": ["desert", "mountains"],
        "enemies": ["spider", "snake", "sentinel"],
        "resources": {"ore": 2, "crystal": 1},
        "boss": "cave_guardian", "seal": "seal_stone",
    },
    "forest": {
        "name": "Thenttkil, the Living Forest", "level": 2,
        "description": "The trees lean close to hear your name. Once David's home, "
        "Thenttkil now dreams in thorns; a lantern hangs where no hand can reach it.",
        "neighbors": ["village", "plains"],
        "enemies": ["spider", "wolf", "wisp"],
        "resources": {"herb": 2, "crystal": 1},
        "boss": "root_guardian", "seal": "seal_root",
    },
    "sea": {
        "name": "The Bellglass Shore", "level": 4,
        "description": "The tide has gone out and forgotten how to return. A drowned "
        "bell tower stands in the exposed sand, tolling beneath a windless sky.",
        "neighbors": ["bridge"], "enemies": ["bandit", "wisp", "snake"],
        "resources": {"crystal": 2, "herb": 1},
        "boss": "tide_wraith", "seal": "seal_tide",
    },
    "bridge": {
        "name": "The Last Honest Bridge", "level": 2,
        "description": "An old stone bridge spans the river below the castle. The "
        "bridge is honest. Its many competing toll collectors are another matter.",
        "neighbors": ["village", "sea", "castle"],
        "enemies": ["bandit", "coyote", "sentinel"],
        "resources": {"ore": 1},
    },
    "plains": {
        "name": "The Lantern Plains", "level": 2,
        "description": "Abandoned watch-lanterns dot the grass like fallen stars. "
        "Wind carries the smell of rain and, from somewhere uphill, singed sheep.",
        "neighbors": ["farm", "forest", "mountains"],
        "enemies": ["coyote", "wolf", "bandit"],
        "resources": {"herb": 2, "ore": 1},
    },
    "mountains": {
        "name": "The Stormspine Mountains", "level": 5,
        "description": "The air tastes of copper. Broken sentinels patrol the pass, "
        "and a drake circles the summit with the confidence of unpaid rent.",
        "neighbors": ["caves", "plains"], "enemies": ["wolf", "sentinel"],
        "resources": {"ore": 3, "crystal": 1}, "boss": "storm_drake",
    },
    "castle": {
        "name": "The Castle of the Hollow Crown", "level": 6,
        "description": "Three ward-signs bar the gate. Beyond them lies a court with "
        "no people, a feast of dust, and a king who mistakes silence for peace.",
        "neighbors": ["bridge"], "enemies": ["sentinel", "wisp"],
        "resources": {"crystal": 2}, "boss": "hollow_king",
    },
}


QUESTS = {
    "trail_watch": {
        "name": "Roads Are For Walking", "giver": "Kieth",
        "description": "Drive off two hostile cacti and one dust coyote so the "
        "village can receive supplies. Search the desert road to find them.",
        "objectives": {"kill:cactus": 2, "kill:coyote": 1},
        "reward": {"gold": 35, "xp": 35, "items": {"potion": 2}},
    },
    "farm_supplies": {
        "name": "Something Still Grows", "giver": "Farmer",
        "description": "Bring three Greenwhisper Herbs for the farmer's sick crops. "
        "Explore the farm to gather them; delivery uses the herbs.",
        "objectives": {"own:herb": 3},
        "reward": {"gold": 25, "xp": 25, "items": {"potion": 2}},
    },
    "coyote_furs": {
        "name": "No More Draughty Jimmy", "giver": "Little Jimmy",
        "description": "Deliver three coyote pelts to insulate the inn. Jimmy swears "
        "the name of this job was Kieth's idea. Delivery uses the pelts.",
        "objectives": {"own:coyote_pelt": 3},
        "reward": {"gold": 40, "xp": 40, "items": {"travel_boots": 1}},
    },
    "venom_study": {
        "name": "Very Definitely Not Soup", "giver": "Smith",
        "description": "Bring two venom vials from spiders or snakes. The smith is "
        "making antidotes for the road crews. Delivery uses the vials.",
        "objectives": {"own:venom": 2},
        "reward": {"gold": 30, "xp": 40, "items": {"antidote": 3}},
    },
    "lost_echoes": {
        "name": "A Voice Between The Trees", "giver": "Kieth",
        "description": "Explore Thenttkil twice and the caves twice. David left "
        "traces in both places; Kieth needs to know his friend was really there.",
        "objectives": {"explore:forest": 2, "explore:caves": 2},
        "reward": {"gold": 45, "xp": 65, "items": {"ward_charm": 1}},
    },
    "mountain_watch": {
        "name": "Who Watches The Watchers?", "giver": "Kieth",
        "description": "Disable two broken ward sentinels. They haunt the bridge, "
        "caves, and mountain pass. Their orders ended long before their patrols did.",
        "objectives": {"kill:sentinel": 2},
        "reward": {"gold": 65, "xp": 80, "items": {"crystal": 2, "potion": 2}},
    },
}


RECIPES = {
    "potion": {
        "name": "Brew Healing Potion", "ingredients": {"herb": 2},
        "produces": "potion", "quantity": 1, "gold": 2,
    },
    "antidote": {
        "name": "Distill Antidote", "ingredients": {"herb": 1, "venom": 1},
        "produces": "antidote", "quantity": 2, "gold": 3,
    },
    "iron_sword": {
        "name": "Forge Proper Iron Sword", "ingredients": {"ore": 4},
        "produces": "iron_sword", "quantity": 1, "gold": 20,
    },
    "dusk_armor": {
        "name": "Forge Duskguard Armor",
        "ingredients": {"ore": 6, "crystal": 3, "coyote_pelt": 2},
        "produces": "dusk_armor", "quantity": 1, "gold": 45,
    },
    "ward_charm": {
        "name": "Bind Shared Ward Charm",
        "ingredients": {"crystal": 3, "herb": 2},
        "produces": "ward_charm", "quantity": 1, "gold": 25,
    },
    "dawn_blade": {
        "name": "Forge Dawn Blade",
        "ingredients": {"dragon_scale": 1, "ore": 5, "crystal": 4},
        "produces": "dawn_blade", "quantity": 1, "gold": 65,
    },
}


PROLOGUE = [
    "The realm of Assonance is having a bad month. The roads have grown teeth, "
    "the sea has misplaced its tide, and the cacti have become openly confrontational.",
    "You are Xehspfe, once a lost child of the druid order, now the proud owner "
    "of a rusty sword and several unanswered questions. David, the druid who "
    "raised you beneath Thenttkil's branches, vanished when the ward-lights failed.",
    "A letter brings you back to Little Jimmy's inn. Kieth has written only: "
    "'I heard David in the trees. Please come home.' Underneath, Jimmy has added: "
    "'Your room is ready. The duck-pattern repairs are complimentary.'",
    "Beyond the village, the castle windows burn with a cold, borrowed light. "
    "Whatever took David is still there. First, though, someone has to deal with "
    "the cactus blocking the vegetable cart.",
]


DIALOGUE = {
    "kieth": [
        "Kieth rubs a thumb over David's old compass. 'He used to get lost on "
        "purpose. Said the interesting things were never on the sensible roads.'",
        "'The castle gate needs three seals: root, stone, and tide. Look in "
        "Thenttkil, the caves, and the shore. Explore each place before challenging "
        "its guardian. We need you alive more than we need you impressive.'",
        "'The wards once belonged to every settlement. Then everyone let David "
        "handle them. I called that trust. I am starting to think it was easier "
        "than admitting how much work we were leaving him.'",
        "'I've put the village jobs in your journal. Bring finished work back "
        "here and claim the rewards. And Xehspfe? Coming home counts as progress.'",
    ],
    "jimmy": [
        "Little Jimmy is taller than the door. Nobody has explained this, and "
        "you have learned the value of leaving some mysteries alone.",
        "'A hot meal and a bed put your health and energy right. Heroic "
        "sleep deprivation is still sleep deprivation. I've checked.'",
        "'David always paid for two breakfasts. Said you might come back hungry. "
        "I've been keeping his account open. Feels wrong to close it.'",
        "'If the world ends, tell it to wipe its boots. I have just done the floor.'",
    ],
    "smith": [
        "The smith studies your sword. 'Ah. Archaeology.'",
        "'Ore makes a proper blade. Crystal strengthens armor and wards. Bring "
        "materials and a few coins to the forge; the recipe board has exact costs.'",
        "'The storm drake sheds scales when it loses a fight. One of those "
        "would make a remarkable sword. Entirely optional. I am enthusiastic, "
        "not your medical adviser.'",
        "'Read an enemy's next move. Guard before a heavy strike. Save your "
        "strongest attacks for an opening. A sharp sword is good; paying attention is cheaper.'",
    ],
    "farmer": [
        "The farmer points at a cactus. 'That was a beet yesterday. I am "
        "trying very hard to remain a reasonable person about this.'",
        "'The green herbs still grow if you explore the fields. Bring some "
        "back for the sick crops. There are people who need feeding while you "
        "sort out the big ominous castle business.'",
        "'David helped plant the first windbreak here. Never asked for a coin. "
        "I should have asked whether he needed anything in return.'",
    ],
}


STORY_BEATS = {
    "warning": [
        "Kieth unfolds a sketch of the castle gate: three dark circles, a root, "
        "a stone, and a wave. His notes name the places their seals were lost: "
        "Thenttkil, the Echoing Caves, and the Bellglass Shore.",
        "'A hollow voice spoke through those bars,' he says. 'All is well. No one "
        "need change anything.' Somehow that is worse than a threat.",
    ],
    "seal_root": [
        "The great root loosens. Thorns fall like dead stitches, revealing "
        "David's lantern with its flame still green. A warm seal settles into your palm.",
        "An echo opens around you: David kneeling beneath the oldest tree, "
        "one hand on its bark. 'They are frightened,' he tells the forest. "
        "'Let me carry it a little longer.'",
        "Thenttkil speaks in leaf-rustle: 'He did not abandon you, little "
        "wanderer. He stayed until staying became a prison.' The path behind "
        "you smells, for the first time, of ordinary rain.",
    ],
    "seal_stone": [
        "The colossus kneels, finally relieved of a task it could not finish. "
        "Inside its chest, the stone seal turns like a small, patient heart.",
        "A crystal shows David at the castle forge, dividing the failing ward "
        "into three anchors. The king's empty armor stands behind him. "
        "'One guardian,' it whispers. 'One will. No more uncertainty.'",
        "David had built a tool to protect Assonance. Years of fear and "
        "unshared responsibility taught it to protect everything from change. "
        "The Hollow King is that command, still obeying itself.",
    ],
    "seal_tide": [
        "The drowned bell cracks. Water rushes into the old channels, lifting "
        "boats that had nearly forgotten they were boats. The tide seal shines "
        "in the wet sand.",
        "David's voice comes clearly now: 'Xehspfe. I tried to make a place "
        "where nothing could hurt you. Then I kept making it smaller.'",
        "'The seals can open the crown. After that, the wards can be rebuilt "
        "and their work shared, or the binding can end. I cannot choose for "
        "everyone again. Please bring me a future I did not plan.'",
    ],
    "storm_drake": [
        "The storm drake folds its wings. Its thunder dwindles to a rather "
        "embarrassed rumble, and a bright scale falls at your feet.",
        "It was nesting around a broken ward-spire, trying to silence the "
        "painful note that only dragons could hear. With the spire shattered, "
        "it rises into clear air. Somewhere below, a sheep breathes easier.",
        "The scale is warm enough to forge. The smith is going to be "
        "absolutely unbearable about this.",
    ],
    "finale": [
        "The Hollow King's crown breaks. Every stolen voice escapes at once, "
        "then the throne room becomes wonderfully, imperfectly quiet.",
        "David stands inside a lattice of roots and light. Older than you "
        "remember. Smaller than the person you needed him to be. Still David.",
        "'I am sorry,' he says. No prophecy. No explanation large enough to "
        "hide inside. Just that. You take his hand through the light.",
        "The three seals can restore the wards, with their burden divided "
        "among Assonance's settlements. Or you can release David and Thenttkil "
        "from the binding entirely, letting wild magic return to the realm. "
        "Neither future can promise that nothing will ever hurt.",
    ],
    "ending_restore": [
        "You place the seals around the broken crown, leaving its center "
        "empty. No throne. No single keeper. The light branches outward: "
        "to the village well, the farm's windbreak, the shore, the mountain road.",
        "When the roots loosen, David nearly falls. You catch him. Keeping "
        "the wards will take ordinary work from many people now: tending "
        "lanterns, mending anchors, listening before a small hurt becomes a monster.",
        "Kieth organizes the first watch. The farmer argues successfully "
        "for meal breaks. Jimmy writes FREE BREAKFAST FOR WARD KEEPERS and "
        "then adds WITHIN REASON. David signs up for one shift a week.",
        "At sunset, you walk beneath Thenttkil together. The forest is still "
        "strange, but the path is open. For once, the person who raised you "
        "does not walk ahead. He walks beside you.",
        "ENDING: MANY HANDS, ONE HOME. Assonance endures because its people "
        "choose, again and again, to look after it. Your adventures can continue.",
    ],
    "ending_release": [
        "You open your hand. The seals break into seeds, pebbles, and salt "
        "water. The binding unravels across Assonance like a breath held for years.",
        "David steps free. Behind him, Thenttkil's roots slip from the "
        "castle foundations. The forest belongs to itself again. Magic runs "
        "with the rivers, strange and bright and no longer taking orders.",
        "The coming months are untidy. Paths move. A village fountain "
        "briefly dispenses pears. Kieth maps safe crossings; the farmer learns "
        "which crops like moonlight. People help their neighbors because no "
        "invisible wall can promise to do it for them.",
        "David leaves his old staff at Jimmy's inn and buys walking boots. "
        "'I thought I had to hold the whole world still,' he says. You ask "
        "where he wants to go. For the first time, he does not know. He smiles.",
        "ENDING: ROOM TO GROW. Assonance becomes a place no one can fully "
        "control, and everyone can help discover. Your adventures can continue.",
    ],
}


ART = {
    "title": r"""
   _____   _____   _____   ____
  / ____| / ____| / ____| |  _ \
 | (___  | (___  | (___   | | | |
  \___ \  \___ \  \___ \  | | | |
  ____) | ____) | ____) | | |_| |
 |_____/ |_____/ |_____/  |____/
       THE WARDS OF ASSONANCE
""",
    "map": """
                     [MOUNTAINS]
                       /     \\
                  [CAVES]  [PLAINS]
                     |      /    \\
                 [DESERT] [FARM] [FOREST]
                       \\    |    /
                         [VILLAGE]
                             |
                          [BRIDGE]---[CASTLE]
                             |
                           [SEA]
""",
}
