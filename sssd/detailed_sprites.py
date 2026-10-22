"""Detailed battle and object illustrations, separate from compact menu icons.

The cactus and camel restore their complete original battle silhouettes. The
coyote, spider and snake retain their original bodies with additional setting
or leg detail; those originals were naturally shorter. Their old health text,
statistics and numbered commands are omitted. The other creatures, adventurer
and objects are new drawings. No scaling, repeated characters or blank padding
is used to enlarge a small icon.
"""


PLAYER_ART = r"""
         ______________
        /   _______    \       /\
       /___/  _ _  \___\      /  \
          |  (o o)  |        |  |
          |    >    |        |  |
          \  .___.  /        |  |
       ____\_______/____     |  |
      / ___/|     |\___  \    |  |
     / /   ||_____|   \  \   |  |
    /_/  / | [+] | \  \__\ __|__|__
   (___)/  |_____|  \(___) \______/
     ||   /|=====|\   ||     |__|
     ||  / | / \ | \  ||     |__|
      ' /__|/   \|__\ '      (__)
          | |   | |
          | |   | |
        __|_|   |_|__
       (____/   \____)
""".strip("\n")


ENEMY_ART = {
    "cactus": r"""
             ^^
            <  >
    ^^      <  >      ^^
   <  >     <  >     <  >
   <  >     <  >     <  >
   <  ^^^^^^    ^^^^^^  >
    ^^^^^^^^^  ^^^^^^^^^
            <  >
            <  >
            <  >
            <  >
            <  >
            <  >
            <  >
            <  >
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""".strip("\n"),
    "coyote": r"""
         .                    .
     _          .         .
   _/ \_          _      / \_
 _/     \________/ \____/    \_
                 .     .
                 \ \__/ '
   ______________/ -  - /
  /'             \_ @  /
  | \   \       | /---'
  | /./\ |----- |/|
 /.//  | /      |||
//||  / /       |||
' |_\ \_\       |_\
     .      .         .    .
""".strip("\n"),
    "spider": r"""
  |\          |          /|
  | '\        |        /' |
  |   '\  .---+---.  /'   |
  |-----\' .--+--. '/-----|
  |      \/   |   \/      |
  |      /\   |   /\      |
  |    /'  '-----'  '\    |
     ____
    (0  0)
//// -vv- \\\\
 | | |    | | |
 / / /    \ \ \
/ / /      \ \ \
  /          \
""".strip("\n"),
    "snake": r"""
                 __
        hiss    /..\
                \" /
      ____      / |'
 _,--'____'----' ,'
<_.--'    '-----'
       __       ___      .
  _.-'/__\-._  /___\  \|/
 /___/____\__\/_____\  |
    .     .      .
""".strip("\n"),
    "camel": r"""
          __             --.__
        .'  '.        ..' '   .
      .'      '._____/    .---'
   .-/                   |
 .'                    ./
 |   |\        .  .---'
 |   |.'------| .'
 #\  |        | |.
## \ .        | |.
   ||'       .| |.
  . |.        | |.
  \ \ #       | |.
   \_\ #      |__..
""".strip("\n"),
    "wolf": r"""
                           /\     /\
                  /\      /  \___/  \
            /\___/  \____/  .     .  \
       ____/                 \   /   |
   ___/      /\  /\  /\      (o) (o)  |
 _/         /  \/  \/  \_          __>
/       ___/              \_  \_/  /'
\______/   \                '----'
       |    |   _________    /
       |   /___/        |   /
       |  /  /          |  /\
       | /  /           | /  \
      / /  /           / /  /'
     /_/__/'          /_/__/
     /_/_/            /_/_/
""".strip("\n"),
    "bandit": r"""
            .-----------.
          .'   _______   '.
         /   /'       '\   \
        |   |  _     _  |   |
        |   | (o)   (o) |   |
        |    \========= /   |
       _|_____\_______/_____|_
      /  /  / |       | \  \  \
     /__/__/  |_______|  \__\__\
    /  /   |  |  ___  |  |   \  \
   /__/    |  | / P \ |  |    \__\
  (___)    |  | \___/ |  |    (___)
   | |     |__|_______|__|      |\
   | |      /    |    \        | \
   | |     /____/ \____\       |__>
   |_|     |   |   |   |
          _|___|   |___|_
         (_____/   \_____)
""".strip("\n"),
    "wisp": r"""
                 .
          .     / \      .
         / \   /   \   / \
      .  \  \_/     \_/  /
     / \  \             /   .
     \  \_/   .     .   \__/ \
      \      (o)   (o)       /
       \        ___        /
     .-'        \_/        '-.
    /      .            .     \
    \__   / \    .     / \   __/
       ) /   \  / \   /   \ (
      / /     \/   \_/     \ \
      \/        .           \/
          .    / \    .
               \_/
""".strip("\n"),
    "sentinel": r"""
          .--------.          /\
          |  ____  |         /  \
          | |o__o| |         |  |
          | |____| |         |  |
       ___|________|___      |  |
      /___/   /\   \___\     |  |
     /|  |   /__\   |  |\    |  |
    / |  |  [====]  |  | \   |  |
   /__|__|  [====]  |__|__\  |  |
   [____]|_________|[____] __|__|__
    |  | /|       |\ |  | \______/
    |__|/_|_______|_\|__|   |__|
    (__)  |   |   |  (__\___|__|
          |___|___|          (__)
          [___]___]
          |   |   |
        __|___|___|__
       [______|______]
""".strip("\n"),
    "root_guardian": r"""
   \  \|/    \    |    /    \|/  /
    \  |      \   |   /      |  /
 \___\ |   \___\  |  /___/   | /___/
      \|       \\ | //       |/
       \\   ___\\|//___    //
        \\ /    \|/    \  //
         \|  (o)     (o) |//
     _____|      /\     |_____
    /  ___/\   _/__\_   /\___  \
   /  /    |  |_____|  |    \  \
  /__/     |  || || |  |     \__\
 / /       |  || || |  |       \ \
/ /        | / | || \ |        \ \
\_\       / /  | ||  \ \       /_/
         / /  /  | \  \ \
    ____/ /__/ / |  \__\ \____
   / ____/ ___/ / \___  \____ \
  /_/   /_/    /___\  \_\   \_\
""".strip("\n"),
    "cave_guardian": r"""
          /\          /\
       __/[]\________/[]\__
      /   /  /      \  \   \
     /___/__/ [o][o] \__\___\
     |      |   __   |      |
    _|______|__|__|__|______|_
   /  ___ /  /      \  \ ___  \
  /  /   /__/   /\   \__\   \  \
 /__/   |   /\ /[]\ /\   |   \__\
 [__]   |  /  V____V  \  |   [__]
 |  |   |__\__|____|__/__|   |  |
 |__|    /     /\     \     |__|
 [___]  /_____/  \_____\   [___]
        |  |        |  |
        |__|        |__|
       / /_\        /_\ \
      /_____]      [_____\
    _/______|      |______\_
""".strip("\n"),
    "tide_wraith": r"""
              _______
             /   O   \
          __/_________\__
         /               \
        /   .---------.   \
       |   /  o     o  \   |
       |   |     _     |   |
       |   |    / \    |   |
       |   |   /   \   |   |
      /    |  |     |  |    \
     /    /   |     |   \    \
    /____/   /|     |\   \____\
       /    / |     | \    \
  ~   /____/  |  O  |  \____\   ~
     /    /   |_____|   \    \
 ~~~/____/~~~/  ~  \~~~\____\~~~
   ~     ~~~/   ~   \~~~      ~
 ~~~~~  ~~   ~~~  ~~~   ~~  ~~~~~
""".strip("\n"),
    "storm_drake": r"""
 /\                                    /\
/  \_                                _/  \
\    \_            /\  /\          _/    /
 \     \__        /  \/  \      __/     /
  \  /\   \__   _/ o    o \_  __/   /\ /
   \/  \     \_/  _      _  \_/     /  V
        \      \   \____/   /      /
         \__    \  /vvvv\  /    __/
            \___/\ \^^^/ /\___/
              /  |\____/|  \
         ____/  /|  /\  |\  \____
        /  ____/ | /__\ | \____  \
       /__/      |  /\  |      \__\
        /\       | /__\ |       /\
       /__\     /   /\   \     /__\
             __/   /  \   \__
        ____/  ___/    \___  \____
       /______/            \______\
      /_/_/_/                \_\_\_\
""".strip("\n"),
    "hollow_king": r"""
          \   /\   /\   /           .
           \_/  \_/  \_/           / \
           |  o   o   |            | |
           |__________|            | |
          /  ________  \           | |
         |  /        \  |          | |
         |  |        |  |          | |
         |  \________/  |          | |
       __\______________/__      __|_|__
      /  /|   /\  /\   |\  \     \_____/
     /__/ |  /  \/  \  | \__\      |_|
    /  /  | /   ||   \ |  \  \     |_|
   /__/   |/    ||    \|   \__\   (___)
  (___)  /|=====||=====|\   (___\__|_|
   /|   / |     ||     | \          '
  / |  /  |     ||     |  \
 /__| /___|_____||_____|___\
      |___|     ||     |___|
      |   |     ||     |   |
    __|___|____/  \____|___|__
""".strip("\n"),
}


ITEM_ART = {
    "rusty_sword": r"""
            /\
           /x \
           | /|
           |x |
           | /|
           |x |
       ____|__|____
       \____  ____/
            ||
            ||
           (__)
""".strip("\n"),
    "tunic": r"""
       ___      ___
      /   \____/   \
     /  /\      /\  \
    /__/  |    |  \__\
          | +--|
          | |xx|
          | +--|
          |    |
          |____|
""".strip("\n"),
    "potion": r"""
           .----.
           |====|
           |    |
          /      \
        .'  .--.  '.
       /   / +  \   \
      |    | HP |    |
      |~~~~\____/~~~~|
       \~~~~~~~~~~~~/
        '----------'
""".strip("\n"),
    "antidote": r"""
           ______
          |______|
           |    |
          /      \
         / .----. \
        |  | XX |  |
        |  | \/ |  |
        |~~'----'~~|
         \~~~~~~~~/
          '------'
""".strip("\n"),
    "herb": r"""
       .--.        .--.
      / /  \      /  \ \
     | /    \    /    \ |
      \/__   \  /   __\/
          '._ \/ _.'
       .---. \||/ .---.
      /__ / \\||// \ __\
         '---'||'---'
              ||
             /  \
""".strip("\n"),
    "ore": r"""
             ______
         ___/  /   \_
        /   \ /      \
       /  *  X  /\    \
      |     / \/  \    |
      | *  /   \   \   |
       \__/  *  \__/__/
        \___________/
""".strip("\n"),
    "crystal": r"""
              /\
             /| \
            / |  \
        /\ /  |   \ /\
       /| \   |   //| \
      / |  \  |  // |  \
      \ |  /\ | //\ |  /
       \| /  \|//  \| /
        \/____V_____\/
""".strip("\n"),
    "venom": r"""
           .----.
           |XXXX|
           |    |
           |    |
           |\  /|
           | \/ |
           | /\ |
           |~~~~|
           |~~~~|
           '----'
""".strip("\n"),
    "coyote_pelt": r"""
         /\      /\
        /  \____/  \
        |  o    o  |
      __/    __    \__
     /   \  /__\  /   \
     \_/  '------'  \_/
       | / / / / / |
       |/ / / / / /|
     __/ / / / / / \__
    /____/\____/\_____\
""".strip("\n"),
    "dragon_scale": r"""
           ________
         /'  /\    '\
        /   /  \     \
       /   / /\ \     \
      |   / /  \ \     |
      |  / / /\ \ \    |
       \  / /  \ \    /
        \__/____\____/
         \__________/
""".strip("\n"),
    "iron_sword": r"""
             /\
            /||\
            |  |
            |  |
            |  |
            |  |
        ____|__|____
        \____  ____/
             ||
             ||
            (__)
""".strip("\n"),
    "hunter_bow": r"""
           .--.
         .' |  '\
        /   |    \
       /    |     \
      |     |      |
  ----|-----|----->|
      |     |      |
       \    |     /
        \   |    /
         '. |  .'
           '--'
""".strip("\n"),
    "root_staff": r"""
          __  /\
         /  \/  \
        | () |__/
         \__/|
            ||
         /\ ||
         \_\||
            ||
            |/\
            ||_\
           /__\
""".strip("\n"),
    "dawn_blade": r"""
          .  /\  .
         *  /||\  *
            |**|
            |**|
          . |**| .
       /\___|__|___/\
       \___  /\  ___/
           \_\/_/
             ||
             ||
            (<> )
""".strip("\n"),
    "iron_armor": r"""
        ___      ___
       /___\____/___\
      /|   |    |   |\
     /_|   | /\ |   |_\
       |   |/__\|   |
       |   |====|   |
       |   |====|   |
       |___|____|___|
        /__|____|__\
       /___|____|___\
""".strip("\n"),
    "wanderer_cloak": r"""
          .------.
         /  ____  \
        /  /    \  \
       |  |      |  |
        \__\____/__/\
       /     ()      \
      /      ||       \
     /       ||        \
    /        ||         \
   /________/  \_________\
""".strip("\n"),
    "dusk_armor": r"""
       /\          /\
      /__\________/__\
     / __ /      \ __ \
    /_/  |   /\   |  \_\
         |  /<>\  |
         |  \__/  |
         | [====] |
         |_[====]_|
        / /|____|\ \
       /_/ |____| \_\
""".strip("\n"),
    "ward_charm": r"""
         .--------.
        /          \
        |          |
         \        /
          \  __  /
           \|__|/
          /  /\  \
         |  /<>\  |
         |  \__/  |
          \______/
""".strip("\n"),
    "travel_boots": r"""
      ____        ____
     |====|      |====|
     | xx |      | xx |
     | xx |      | xx |
     | xx |      | xx |
     |    |      |    |
     |    \__    |    \__
     |       \   |       \
     |________|  |________|
     '--------'  '--------'
""".strip("\n"),
    "silver_ring": r"""
            /\
           /<>\
          /____\
        .'  __  '.
       /  .'  '.  \
      |  /      \  |
      |  \      /  |
       \  '.__.'  /
        '.______.'
""".strip("\n"),
}


def render_battle(enemy_id: str, width: int) -> str:
    """Put detailed combatants on the same baseline whenever both bodies fit.

    A four-column gap separates the figures. On intermediate widths the full
    enemy stands alone; below its actual width the established compact renderer
    supplies the encounter. Nothing is clipped out of a detailed silhouette.
    """
    from .sprites import render_battle as compact_battle

    if width < 1:
        raise ValueError("Battle illustration width must be positive.")
    if enemy_id not in ENEMY_ART:
        return compact_battle(enemy_id, width)
    enemy = ENEMY_ART[enemy_id].splitlines()
    enemy_width = max(map(len, enemy))
    if width < enemy_width:
        return compact_battle(enemy_id, width)
    player = PLAYER_ART.splitlines()
    player_width = max(map(len, player))
    together_width = player_width + 4 + enemy_width
    if together_width > width:
        inset = " " * ((width - enemy_width) // 2)
        return "\n".join(inset + line.rstrip() for line in enemy)
    height = max(len(player), len(enemy))
    player = [""] * (height - len(player)) + player
    enemy = [""] * (height - len(enemy)) + enemy
    inset = " " * ((width - together_width) // 2)
    return "\n".join(
        (inset + left.ljust(player_width) + "    " + right).rstrip()
        for left, right in zip(player, enemy)
    )


_ACTION_OBJECTS = {
    "attack": r"""
      /\
     /||\
     |  |
     |  |
  ___|__|___
  \___  ___/
      ||
""".strip("\n"),
    "power": r"""
   .   /\  .
    * /||\ *
      |**|
   .  |**| .
  \___|__|___/
    \______/
       ||
""".strip("\n"),
    "guard": r"""
   .-------.
  / .-----. \
 |  |  +  |  |
 |  | +++ |  |
  \  \ + /  /
   \  \_/  /
    '-----'
""".strip("\n"),
    "mend": r"""
    .  *  .
   / .---. \
  * /  +  \ *
  | | +++ | |
  * \  +  / *
   \ '---' /
    '  *  '
""".strip("\n"),
    "potion": r"""
     ____
    |====|
    /    \
  .'  +   '.
 |~~~ HP ~~~|
  \~~~~~~~~/
   '------'
""".strip("\n"),
    "antidote": r"""
    .----.
    | XX |
   /      \
  |  /\/\  |
  |  \/\/  |
  |~~~~~~~~|
   '------'
""".strip("\n"),
}

_ACTION_CAPTIONS = (
    ("attack", "Attack", "+1 energy"),
    ("power", "Power", "-3 energy"),
    ("guard", "Guard", "+3 energy"),
    ("mend", "Mend", "-4 energy"),
    ("potion", "Potion", "40% health"),
    ("antidote", "Antidote", "Cure poison"),
)


def render_actions(keys: dict[str, str], width: int) -> str:
    """Show six distinct objects with live action keys in a 100-column row.

    The drawing is nine lines tall: seven of object detail and two of captions.
    Smaller windows receive an empty string so the caller can use its compact
    controls. Missing, invalid or oversized keys also request that fallback.
    """
    if width < 100 or not _ACTION_OBJECTS.keys() <= keys.keys():
        return ""
    cell_width = 15
    columns = []
    for action, name, effect in _ACTION_CAPTIONS:
        key = keys[action]
        if not isinstance(key, str) or not key.isascii() or not key.isdecimal():
            return ""
        label = f"[{key}] {name}"
        if len(label) > cell_width:
            return ""
        picture = _ACTION_OBJECTS[action].splitlines()
        # Center the entire object, preserving the columns between its strokes.
        picture_width = max(map(len, picture))
        padding = " " * ((cell_width - picture_width) // 2)
        block = [(padding + line).ljust(cell_width) for line in picture]
        block.extend((label.center(cell_width), effect.center(cell_width)))
        columns.append(block)
    inset = " " * ((width - 100) // 2)
    return "\n".join(
        (inset + "  ".join(column[row] for column in columns)).rstrip()
        for row in range(9)
    )
