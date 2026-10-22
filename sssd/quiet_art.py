"""Larger still-life scenes for reading, arriving, and recovering."""

def _journal():
    left = r'''
       THE ROAD AHEAD

           .----.
           | () |
     /\    |____|    /\
    /__\     ||     /__\
    |[]|_____||_____|[]|
    |___|   HOME   |___|
              :
              : . . . .
                      :
       /\            /\
      /  \          /  \
     /_/\_\        /_/\_\

   Here be poor decisions.
'''.strip("\n").splitlines()
    right = r'''
    THINGS TO REMEMBER

   THE WARDS OF ASSONANCE

     ROOT   STONE   TIDE
      /\      /\     ~
     /||\    /  \   ~ ~
     \||/    \  /    ~
      \/      \/    ~ ~

   ________________________
   _____________________
   ________________________

   _____________________
   ________________________
'''.strip("\n").splitlines()
    rows = ["    ." + "-" * 29 + "." + "-" * 29 + ".",
            "   /" + " " * 30 + "|" + " " * 30 + "\\",
            "  /" + "_" * 31 + "|" + "_" * 31 + "\\"]
    for a, b in zip(left, right):
        rows.append("  |" + a.ljust(31) + "|" + b.ljust(31) + "|")
    rows += ["  |" + "_" * 31 + "|" + "_" * 31 + "|",
             "   \\" + "_" * 30 + "|" + "_" * 30 + "/",
             "    \\" + "_" * 29 + "|" + "_" * 29 + "/",
             "                                  |   |",
             "                                  |   |",
             "                                  | /\\|",
             "                                  |/"]
    return "\n".join(rows)


JOURNAL = _journal()

PROLOGUE = r'''
      .--------------------------------------------------.
     /    ___________________________________________     \
    |    /                                           \     |
    |    |                                           |     |
     \___|       TO THE ADVENTURER                    |____/
         |                                           |
         |                                           |
         |       I heard David in the trees.         |
         |                                           |
         |       Please come home.                   |
         |                                           |
         |                                           |
         |                          - Kieth          |
         |                                           |
         |                 .-------.                 |
         |               .'  /\ /\  '.               |
         |              (    | K |    )              |
         |               '.  \___/  .'               |
         |                 '-------'                 |
         |                  / | \                    |
      ___|                 /__|__\                   |____
     /   |___________________________________________|    \
    |    \___________________________________________/     |
     \____________________________________________________/
           A LONG WAY HOME. A VERY SHORT SET OF DIRECTIONS.
'''.strip("\n")

DEFEAT = r'''
     .---------------- VILLAGE INFIRMARY ----------------.
     |                      _____                       |
     |                     |     |                      |
     |                  ___|     |___                   |
     |                 |             |                  |
     |                 |___       ___|                  |
     |                     |     |                      |
     |                     |_____|                      |
     |                                                  |
     |   .--------.                       .--------.    |
     |   |        |        z              |        |    |
     |   |   _____|_____      Z           |        |    |
     |   |  /     _     \_________________|        |    |
     |   | (    -   -    )                        ||    |
     |   |  \___________/_________________________||    |
     |   |  |_____________________________________||    |
     |   |__|                                     ||    |
     |___|__|_____________________________________|_|___|
          A setback. The bed charges no interest.
'''.strip("\n")


def _desk(book, title):
    """Place a whole book, candle, ink bottle and quill on one continuous desk."""
    candle = r'''
          (
         ( )
          V
        .---.
        |   |
        |   |
        |   |
        |   |
      __|___|__
     /_________\

                  ___
                /   /
               /   /
              /  _/
             / _/
            /_/
           /
          /
     .---/---.
     |  INK  |
     |_______|
'''.strip("\n").splitlines()
    pages = book.splitlines()
    rows = ["           " + title,
            "  ." + "-" * 108 + ".", "  |" + " " * 108 + "|"]
    for index in range(max(len(pages), len(candle))):
        left = pages[index] if index < len(pages) else ""
        right = candle[index] if index < len(candle) else ""
        body = "    " + left.ljust(74) + right
        rows.append("  |" + body.ljust(108) + "|")
    rows += ["  |" + "_" * 108 + "|", "  /" + "_" * 108 + "/",
             "     ||                                                                                                ||",
             "     ||                                                                                                ||"]
    return "\n".join(rows)


SCREEN_ART = {"journal": JOURNAL, "prologue": PROLOGUE, "defeat": DEFEAT}
WIDE_SCREEN_ART = {
    "journal": _desk(JOURNAL, "THE TRAVELLER'S DESK. EVERY GREAT PLAN STARTS WITH A QUESTIONABLE MAP."),
    "prologue": _desk(PROLOGUE, "ONE LETTER. A WHOLE WORLD OF UNFINISHED BUSINESS."),
}
