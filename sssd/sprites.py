"""Small ASCII illustrations, independent of game rules and terminal input.

The cactus, coyote, spider, snake, and camel adapt the original silhouettes in
SSSDpak's five battle modules. Their height is shortened for modern battle
screens; the remaining creatures, adventurer, and item illustrations are new.
"""


PLAYER_ART = r"""
      .-.
     /o o\     /
     \ - /    /
   ___|_|___ /
  / /|___|\_X
 /_/ |___|  |
     / | \
    /__|__\
""".strip("\n")


ENEMY_ART = {
    "cactus": r"""
          ^^
  ^^     <  >     ^^
 <  >    <  >    <  >
 <  ^^^^^    ^^^^^  >
  ^^^^^^^^  ^^^^^^^^
         <  >
         <  >
^^^^^^^^^^^^^^^^^^^^^^
""".strip("\n"),
    "coyote": r"""
                .    .
                \ \_/'
  ______________/- - /
 /'             \_@ /
 | \  \       | /--'
 | /.\ |------|/|
/.// | /      |||
'|_\ \_\      |_\
""".strip("\n"),
    "spider": r"""
       ____
      (0  0)
  //// -vv- \\\\
 / / /      \ \ \
""".strip("\n"),
    "snake": r"""
              __
      hiss   /..\
             \" /
     ____    / |'
_,--'____'--' ,'
<_.--'   '----'
""".strip("\n"),
    "camel": r"""
      __           --.__
    .'  '.      ..' '  .
  .'      '.___/  .----'
.-/               |
|  |\      . .---'
|  |.'----|.'
 \ |      | |
  \_\     |__.
""".strip("\n"),
    "wolf": r"""
                 /\_/\
             ___/ o o\
      /\____/       _ >
     /            /'
    /  /----/  __/
   /__/    /__/\\
    ||      || ||
   _||_    _||_||_
""".strip("\n"),
    "bandit": r"""
       .------.
      /  _  _  \
     |  [o][o]  |
     |  ======  |
  ___/`--------'\__
 / __|   /\/\   | \__
/_/  |___\__/___|__/_>
     /__/  \__\
""".strip("\n"),
    "wisp": r"""
           .
        .-~~~-.   .
      .'  o o  '.
     /     ~     \
  .  '._       _.'
        )  ~  (
     .-'  .    '-.
        ~  ~  ~
""".strip("\n"),
    "sentinel": r"""
      ___       /\
     [o_o]      ||
   __|___|__    ||
  /| [===] |\   ||
 /_| [===] |_\  ||
   |_______|  \_||
    | | | |     ||
   [_|] [_|]    ||
""".strip("\n"),
    "root_guardian": r"""
 \\\  \|/  ///    \|/
  \\\ [o o] ///   /\
   \_\_===_/_/___/ /
      /|||\\_____/
     / ||| \
    /  |||  \
  _/__/ | \__\_
 /_/  /_|_\  \_\
""".strip("\n"),
    "cave_guardian": r"""
        /\  /\
     __/[]\/[]\__
    /  [ o  o ]  \
   / /|[  ==  ]|\ \
  /_/ |[______]| \_\
 [__] / []  [] \ [__]
     /__/    \__\
    [___]    [___]
""".strip("\n"),
    "tide_wraith": r"""
       .--.
  ~~~ /o  o\ ~~~
     |  __  |
     | /  \ |      ~
  ~ _/ |  | \_
   / __|  |__ \ ~
 ~~\/  /~~\  \/~~
~~~~~~~    ~~~~~~~
""".strip("\n"),
    "storm_drake": r"""
 /\                 /\
/  \_    /\_/\    _/  \
\    \__/ o o \__/    /
 \___   \_ ^ _/   ___/
     \__/| V |\__/
        /|___|\
    ___/ /   \ \___
   <____/     \____>
""".strip("\n"),
    "hollow_king": r"""
       \_/\_/\_/
        |____|
       / o  o \
       \  __  /
     ___|____|___
    / /| /\/\ |\ \
   /_/ |/ || \| \_\
      /___||___\
""".strip("\n"),
}


COMPACT_ENEMY_ART = {
    "cactus": r"""
 _ \|/ _
 \__|__/
    |
""".strip("\n"),
    "coyote": r"""
 /\_/\
 ( o >
 /|_|\
""".strip("\n"),
    "spider": r"""
 //(oo)\\
  / vv \
""".strip("\n"),
    "snake": r"""
  __
 /oo\___
 \__/\___>
""".strip("\n"),
    "camel": r"""
  __    __
 /  \__/o>
 |_|  |_|
""".strip("\n"),
    "wolf": r"""
 /\___/\
< o   o >
 \__^__/
""".strip("\n"),
    "bandit": r"""
 .----.
 |o==o|
 /_XX_\
""".strip("\n"),
    "wisp": r"""
 .~.
(~o~)
 ~~~
""".strip("\n"),
    "sentinel": r"""
 [o_o]
 /[=]\
 _| |_
""".strip("\n"),
    "root_guardian": r"""
 \|/ \|/
  [o_o]
  /_|_\
""".strip("\n"),
    "cave_guardian": r"""
  /\/\
  [oo]
 [_][_]
""".strip("\n"),
    "tide_wraith": r"""
 ~(oo)~
 ~~\/~~
""".strip("\n"),
    "storm_drake": r"""
<\ /o\ />
 \_W_/
""".strip("\n"),
    "hollow_king": r"""
 \_W_/
 (o_o)
 /|_|\
""".strip("\n"),
}


ITEM_ART = {
    "rusty_sword": r"""
   /x/
  /x/
 ==X==
   /
""".strip("\n"),
    "tunic": r"""
 __    __
/  \__/  \
\_      _/
  |____|
""".strip("\n"),
    "potion": r"""
   __
  _||_
 / +  \
 \____/
""".strip("\n"),
    "antidote": r"""
   []
  /--\
 | \/ |
  \__/
""".strip("\n"),
    "herb": r"""
  _   _
 ( \|/ )
  \ | /
   \|/
""".strip("\n"),
    "ore": r"""
    /\
  _/  \_
 /_/\/\_\
 \______/
""".strip("\n"),
    "crystal": r"""
    /\
   /| \
   \| /
    \/
""".strip("\n"),
    "venom": r"""
   __
  /||\
 | xx |
  \__/
""".strip("\n"),
    "coyote_pelt": r"""
 /\/\__/\/\
 |  .  .  |
 \  /\/\  /
  \/    \/
""".strip("\n"),
    "dragon_scale": r"""
   /^^\
  / /\ \
  \ \/ /
   \__/
""".strip("\n"),
    "iron_sword": r"""
   /|
  / |
 ==X==
   |
""".strip("\n"),
    "hunter_bow": r"""
  /)
 / |---->
 \ |
  \)
""".strip("\n"),
    "root_staff": r"""
  @@@
 @ | @
   |
  /|
""".strip("\n"),
    "dawn_blade": r"""
  . + .
    /\
  ==||==
    ||
""".strip("\n"),
    "iron_armor": r"""
 _[____]_
/ [====] \
\_|[==]|_/
  |____|
""".strip("\n"),
    "wanderer_cloak": r"""
   .--.
 / /  \ \
 |/    \|
 /______\
""".strip("\n"),
    "dusk_armor": r"""
 _[ /\ ]_
/ [*==*] \
\_|[##]|_/
  |____|
""".strip("\n"),
    "ward_charm": r"""
 \     /
  \___/
  ( + )
   \_/
""".strip("\n"),
    "travel_boots": r"""
 | | | |
 | |_| |_
 |___|___|
""".strip("\n"),
    "silver_ring": r"""
   /\
 .-||-.
(      )
 '----'
""".strip("\n"),
}


_UNKNOWN_ART = r"""
   .-.
  ( ? )
   \_/
""".strip("\n")


def render_battle(enemy_id: str, width: int) -> str:
    """Keep an encounter illustrated even when the terminal is narrow.

    At 58 columns both figures fit side by side, aligned at their feet.
    From 28 columns the full enemy stands alone. Smaller terminals get a
    compact silhouette. Positive widths below 20 also receive a clipped,
    nonempty compact drawing instead of overflowing the terminal.
    """
    if width < 1:
        raise ValueError("Battle illustration width must be positive.")
    if width < 28:
        art = COMPACT_ENEMY_ART.get(enemy_id, _UNKNOWN_ART)
        if width < 20:
            return "\n".join(line.lstrip()[:width] for line in art.splitlines())
    else:
        art = ENEMY_ART.get(enemy_id, _UNKNOWN_ART)
    enemy = art.splitlines()
    enemy_width = max(map(len, enemy))
    if width < 58:
        padding = " " * ((width - enemy_width) // 2)
        return "\n".join(padding + line.rstrip() for line in enemy)

    player = PLAYER_ART.splitlines()
    player_width = max(map(len, player))
    height = max(len(player), len(enemy))
    player = [""] * (height - len(player)) + player
    enemy = [""] * (height - len(enemy)) + enemy
    gap = " " * (width - player_width - enemy_width - 4)
    return "\n".join(
        ("  " + left.ljust(player_width) + gap + right).rstrip()
        for left, right in zip(player, enemy)
    )
