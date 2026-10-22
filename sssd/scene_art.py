"""Small spatial scenes in the spirit of the original hand-drawn maps.

Each ``{name}`` marks a choice placed in the scene itself. The interface
replaces it with a three-character key such as ``[1]`` or ``[ ]``. No
terminal escapes, rendering rules, or game state belong in this catalogue.
"""


LOCATION_ART = {
    "village": r"""
       _||_                  ) )                     /\
      /____\                _|_|_                 __/__\__
     /______\              /_____\               /________\
     |  []  |              | []  |               | []  [] |
     |__[]__|              |_[]__|               |___[]___|
     {rest} Inn              {smith} Smith             {shop} Jimmy's shop
  o  o           .------------------.                 :
 /|\/|\          | {quests} Jobs board   |        . . . : . . .
 {locals} Locals       '--------||--------'              :
____courtyard______________||___________________ {travel} Road ->
""",
    "farm": r"""
          /\                             .--.       \ | /
         /__\            o              (____)    -- ( ) --
     ___/____\___       /|\                            | \
    /____________\      / \         v v v v v v v v
    | HAY  | BED |   {farmer} Farmer     | | | | | | | |
    |______|__[]_|                 v v v v v v v v
      {rest} Barn bed                 {harvest} Crops / harvest
            :        _              ' ' ' ' ' ' '
     . . . .: . . . |_| . . . . . . . . . . . . .
_____:_______________|____________________ {travel} Road ->
""",
    "desert": r"""
         \ | /                              __
       -- ( ) --             _            /  \_.-.
         / | \           ___/ \___        \_  /   \__
              _      ___/         \___      ||    ||
        _    | |  _                         camel agenda
       | |___| |_| |       {explore} Search the dunes
        \____   __/    . . . . . . . . . . . . .
             | |     .           /\     (  )
__ {travel} Road _|_|____.___________/  \____ )(___
                                 {rest} Camp
""",
    "caves": r"""
       /\          /\                    /\       /\
   ___/  \________/  \____           ____/  \_____/  \___
  /   /\    /\    /\     \_________/     /\    /\       \
 |    \/    \/    \/                     \/    \/       |
 |  *      {explore} Follow crystal tracks     .---------.    |
 |    . . . . . . . . . . . . . . . . .  |  (O)(O) |    |
 |   .         /\                        |  /____\ |    |
 |  .   ( )   /__\                       | COLOSSUS|    |
_|_{travel} Road__ )(__ {rest} Camp ______________ {challenge} Lair ____|_
""",
    "forest": r"""
      8888           888888             888888888
    88888888      88888888888         8888888888888
   8888888888    8888888888888      88888  (o)  88888
       ||             ||               |  ___  |
       ||    {explore} Follow the lanterns    | /   \ |
       ||       . . . . . . . . . .     | |   | |
      /  \     .        /\        .      {challenge} Root gate
              .   ( )  /__\        .    / / | \ \
____ {travel} Road ___ )(__ {rest} Camp _______/ /__|__\ \____
""",
    "sea": r"""
         ~     ~       |\              _||_
                       | \            | () |  drowned
        _______________|__\           |____|  bell tower
        \________________/            | [] |
  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~    |____|
      . . . . . . . . {explore} Walk the shore    {challenge} Bell
     .                            /\          .
    .                    ( )     /__\         .
__ {travel} Road ____________ )(___ {rest} Camp _______.____
""",
    "bridge": r"""
          /\            LAST HONEST BRIDGE             /\
         /__\       |==|==|==|==|==|==|==|            /__\
         |[]|_______|__|__|__|__|__|__|__|____________|[]|
     . . |  |   {explore} Patrol the crossing           |  | . .
    .    |__|____     ____     ____     ____     _____|__|   .
   .             \___/    \___/    \___/    \___/             .
  .       ~  ~  ~       ~  ~   ~    ~   ~      ~              .
 {travel} Road       ~          /\          ~                .
_____________________ ( ) __/__\_____________________________
                       )(__ {rest} Riverside camp
""",
    "plains": r"""
          .--.                          .--.
       .-(    ).        __           .-(    ).
      (________)      _(  )_        (________)
             _         |  |                  _
    v       |_|        |__|        v        |_|
   \|/       |     {explore} Follow the lanterns     |
  . . . . . . . . . . . . . . . . . . . . . . . .
 .                      /\           v           .
 {travel} Road       ( )   /__\         \|/          .
__________________ )(__ {rest} Camp ________________________
""",
    "mountains": r"""
                    /\              /\        _/\_
          /\       /  \     /\     /  \      /    \
         /  \     / /\ \   /  \___/ /\ \___  <o  o>
     ___/ /\ \___/ /  \ \_/            /\     \__/   /\
    /   /    \        {challenge} Drake's nest      \_____/  \
   /          \           . . . . . . .          /    \
  /  {explore} Climb the pass .       /\   .     /\  /      \
 /       . . . . . . . .        /__\   .   /  \/        \
_ {travel} Road _________ ( ) _____ {rest} Camp __________________
                      )(
""",
    "castle": r"""
        |>>>                 /\                  <<<|
      _|_|_|_               /__\                _|_|_|_
      | []  |_______        |()|        ________|  [] |
      |     | |_| |_|_______|__|_______|_| |_|  |     |
      | []  |         THE HOLLOW CROWN          |  [] |
      |     |           .----------.            |     |
      |_____| {explore} Court |  /\  /\  | {challenge} Throne |_____|
          . . . . . .   |  | || |  | . . . . . .
         .       /\     |__|_||_|__|            .
___ {travel} Road __/__\_ {rest} Camp ________________________
""",
}


SCREEN_ART = {
    "locals": r"""
    .---------------- LITTLE JIMMY'S INN ----------------.
    |        ___               ,.,.                _     |
    |     __/___\__           |___|              _|_|_   |
    |       \ o /             (o o)              (o o)   |
    |      _/| |\_           _/| |\_            _/| |\_  |
    |    {kieth} Kieth         {jimmy} Jimmy          {smith} Smith  |
    |====================================================|
    |         ||               ||                 ||     |
    '________/  \_____________/  \_______________/  \____'
""",
    "shop": r"""
            JIMMY'S SHOP: MOSTLY LEGAL, MOSTLY POTIONS
    .------------------------.    .----------------------.
    |  _   _    /\    ___    |    |      YOUR SURPLUS    |
    | (_) (_)   ||   /___\   |    |      .--------.      |
    | /_\ /_\  =||=  |___|   |    |    _/__________\_    |
    |                        |    |   |  o   o   o  |    |
    |    {buy} Buy supplies    |    |   | {sell} Sell    |    |
    '========================'    '===|_____________|===='
""",
    "workshop": r"""
         ( (             THE SMITH'S WORKBENCH            *
          ) )      .-----------------------.            * |
         _|_|_     |  /\    /\    /\    /\ |         ____|____
        /_____\    |  ||    ||    ||    || |        /____|___/
        | (*) |    | =||=  =||=  =||=  =||=|       /     |  /
        |_____|    '-----------------------'      |  ___|_ |
       {craft} Craft       [====== anvil ======]       {upgrade} Upgrade
     _____________          |        |           _______________
""",
    "character": r"""
                  HOW WILL YOU GROW, ADVENTURER?
       _||_                .--------.                __
      (o o)    /\          |  _  _  |             __/ /
      /|_|\    ||          | ( \/ ) |            /_  /
     /_|_|_\  =||=         |  \  /  |           __/ /__
       / \     ||           \  \/  /           /_______/
      /   \                  '----'               . . .
   {strength} Strength          {vitality} Vitality         {agility} Agility
    training dummy          hold the line          light feet
""",
    "ending": r"""
                THE BROKEN CROWN. AN OPEN HAND.
         .   .   .                              . . .
         |\_/|\_/|           ( o )             .  *  .
         |_______|          -- | --             . . .
           / | \              / \             /  |  \
          /  |  \                            /   |   \
   {restore} Restore the wards              {release} Release the binding
         many hands                         room to grow
""",
    "title": r"""
       _____   _____   _____   ____             /\
      / ____| / ____| / ____| |  _ \           /__\
     | (___  | (___  | (___   | | | |       __|[]|__
      \___ \  \___ \  \___ \  | | | |      |  |  |  |
      ____) | ____) | ____) | | |_| |     _|__|__|__|_
     |_____/ |_____/ |_____/  |____/     /    |  |    \
              THE WARDS OF ASSONANCE
          {new} New adventure          {continue} Continue your story
""",
    "journal": r"""
                 .-----------------.-----------------.
                /  THE ROADS       |   THINGS WORTH    \
               /    WE TOOK        |    REMEMBERING    \
              |  . . . . . . .     |   --   --   --    |
              |  .  /\    *  .     |   --   --   --    |
              |  . /__\ . . .      |   --   --         |
              |____________________|___________________|
                                   |
""",
    "prologue": r"""
                  .-------------------------------.
                 /   TO THE ADVENTURER             /|
                /                                 / |
               /   I heard David in the trees.    /  |
              /   Please come home.              /   |
             /                         - Kieth  /    /
            '---------------------------------'    /
             |____________________________________/
""",
    "rest": r"""
                   z          .         *
                     Z              .
            ___________     .
           |  _   _    |                 *
           | (_) (_)   |__________________
           |___________|__________________|
           |           |                  |
              A tactical nap. Doctor's orders.
""",
    "victory": r"""
                   *        /\        *
                       *    ||    *
                  . . . .  =||=  . . . .
                            ||
                         ___||___
                        /________\
                   STILL HERE. STILL STANDING.
""",
    "defeat": r"""
                .--------------------------.
                |     VILLAGE INFIRMARY    |
                |           +              |
                |   ___             ___    |
                |  (x x)___________|   |   |
                |__|_______________|___|___|
                   A setback. Not the end.
""",
}
