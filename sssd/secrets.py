"""Optional roadside nonsense and a real, deterministic game against a crow."""


SECRETS = {
    "village": {
        "id": "well_echo",
        "title": "The Suspiciously Opinionated Well",
        "description": (
            "An old bucket hangs above the village well. Someone has scratched "
            "PLEASE DO NOT FEED THE ECHO into the winch. The echo has added PLEASE DO."
        ),
        "actions": (
            ("listen", "Listen to the well"),
            ("kappa", "Whisper: 'All hail the great one'"),
        ),
        "responses": {
            "listen": (
                "You lean over the stones. 'HELLO?'",
                "'hello,' says the well. 'also, Jimmy owes me three buckets.'",
                "The bucket rises by itself, carrying a dusty healing potion and a strongly worded invoice.",
            ),
            "kappa": (
                "The well whispers 'kappa' back. Then, after a thoughtful pause: 'kappa kappa.'",
                "Somewhere beneath Assonance, an ancient and completely unhelpful tradition continues.",
            ),
        },
        "reward_action": "listen", "reward": {"potion": 1},
    },
    "farm": {
        "id": "crow_board",
        "title": "Noughts and Crows",
        "description": (
            "A crow in a stolen waistcoat guards a three-by-three board scratched into a crate. "
            "A sign promises NO WAGERS, NO REFUNDS, VERY LIMITED MATHEMATICS."
        ),
        "actions": (
            ("crow", "Play Noughts and Crows"),
            ("rules", "Read the crow's extremely official rules"),
            ("scarecrow", "Inspect the scarecrow's complaint box"),
        ),
        "responses": {
            "crow": (
                "The crow pushes nine wooden squares toward you. 'You are X. I am O. "
                "This arrangement has been approved by a bird.'",
            ),
            "rules": (
                "Put three X marks in a row, column, or diagonal. The crow plays O after each turn.",
                "A full board without a line is a draw. Your first win OR draw earns 12 gold and 2 herbs.",
                "Playing is free. Further games are for bragging rights; the crow has a strict biscuit budget.",
            ),
            "scarecrow": (
                "Every complaint says 'birds'. Every signature is a small drawing of a bird.",
                "The farmer pays you one herb for conducting this important workplace investigation.",
            ),
        },
        "reward_action": "scarecrow", "reward": {"herb": 1},
    },
    "desert": {
        "id": "cactus_permit",
        "title": "Department of Aggressive Vegetation",
        "description": (
            "A cactus behind a tiny desk wears a tie. Its notice reads: "
            "HOSTILITY PERMIT REQUIRED. QUEUE ON THE LEFT. It is the only cactus in the queue."
        ),
        "actions": (
            ("stamp", "Request a hostility permit"),
            ("appeal", "Appeal the queue"),
        ),
        "responses": {
            "stamp": (
                "The cactus stamps your form with its forehead. The stamp says OUCH.",
                "It hands you a lump of iron ore as an official paperweight. You are licensed to look annoyed.",
            ),
            "appeal": (
                "Your appeal is denied because it was submitted before your complaint about the appeal.",
                "The cactus looks smug. You have never wanted to fight office furniture more.",
            ),
        },
        "reward_action": "stamp", "reward": {"ore": 1},
    },
    "forest": {
        "id": "knocking_tree",
        "title": "The Tree That Knocks Back",
        "description": (
            "Three knocks sound from inside a hollow trunk. A carved face asks: "
            "'I answer when called, but I have no mouth. What am I?' Below it: NO, NOT THE MAYOR."
        ),
        "actions": (
            ("echo", "Answer: an echo"),
            ("mayor", "Answer: definitely the mayor"),
            ("tree", "Answer: a suspiciously talkative tree"),
        ),
        "responses": {
            "echo": (
                "'An echo,' you say. 'An echo,' says the hollow. 'Correct,' says the tree. 'Show-off.'",
                "A small echo crystal drops into your hand. A voice inside whispers, 'We practiced this.'",
            ),
            "mayor": (
                "'The mayor has a mouth,' says the tree. 'Several hours of one, according to the pigeons.'",
                "The carved face waits. You can try again.",
            ),
            "tree": (
                "'I have a mouth. You are looking at it,' says the tree, offended on a technicality.",
                "It insists this is a perfectly fair riddle. You can try again.",
            ),
        },
        "reward_action": "echo", "reward": {"crystal": 1},
    },
    "sea": {
        "id": "bottle_note",
        "title": "A Message from a Much Smaller Adventure",
        "description": (
            "A green bottle rolls ashore. Inside is a folded note headed READ ME, "
            "written by someone whose plans were much larger than their handwriting."
        ),
        "actions": (
            ("read", "Read the old note"),
            ("reply", "Send a reply out to sea"),
        ),
        "responses": {
            "read": (
                "'Things to do: finish the farm, make the castle work, stop the cactus killing everyone.'",
                "Below, in smaller letters: 'It worked yesterday. Probably.'",
                "The note is old, earnest, and full of crossed-out ideas. You keep it dry. "
                "There is still room at the bottom for the next adventure.",
                "A sealed potion was tucked beneath the paper. The expiry date just says EVENTUALLY.",
            ),
            "reply": (
                "You write: 'The roads go somewhere now. The cactus is still an absolute bastard.'",
                "You send the bottle back. A gull reads it over your shoulder and nods solemnly.",
            ),
        },
        "reward_action": "read", "reward": {"potion": 1},
    },
}


SECRET_FLAGS = frozenset(
    {prefix + secret["id"] for secret in SECRETS.values()
     for prefix in ("secret:", "secret_reward:")}
    | {"crow_prize"}
)
SECRET_PROGRESS = frozenset({"crow:played", "crow:won", "crow:drawn"})

_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
          (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def _has_line(board: list[str], mark: str) -> bool:
    return any(all(board[cell] == mark for cell in line) for line in _LINES)


class CrowGame:
    """A transient tic-tac-toe board. X starts; a deterministic crow plays O.

    The board and result properties are read-only views. The game engine also
    verifies ownership of the session and replays its move history before any
    reward, so a caller cannot turn an arbitrary result string into free gold.
    """

    def __init__(self):
        self._board = [" "] * 9
        self._moves: list[int] = []
        self._result: str | None = None

    @property
    def board(self) -> list[str]:
        return list(self._board)

    @property
    def finished(self) -> bool:
        return self._result is not None

    @property
    def result(self) -> str | None:
        return self._result

    def _settle(self) -> bool:
        if _has_line(self._board, "X"):
            self._result = "win"
        elif _has_line(self._board, "O"):
            self._result = "loss"
        elif " " not in self._board:
            self._result = "draw"
        return self.finished

    def _crow_move(self) -> int:
        empty = [cell for cell, mark in enumerate(self._board) if mark == " "]
        for mark in ("O", "X"):
            for cell in empty:
                candidate = list(self._board)
                candidate[cell] = mark
                if _has_line(candidate, mark):
                    return cell
        # Win, block, then prefer the middle and corners. Clever, not omniscient.
        return next(cell for cell in (4, 0, 8, 2, 6, 1, 3, 5, 7) if cell in empty)

    def play(self, cell: int) -> list[str]:
        if self.finished:
            return ["This game is over. The crow offers a rematch and denies everything."]
        if type(cell) is not int or not 1 <= cell <= 9:
            return ["Choose a square from 1 to 9. The crow refuses imaginary numbers."]
        if self._board[cell - 1] != " ":
            return ["That square is occupied. 'Nice try,' says the crow."]
        self._moves.append(cell)
        self._board[cell - 1] = "X"
        messages = [f"You place X in square {cell}."]
        if not self._settle():
            crow_cell = self._crow_move()
            self._board[crow_cell] = "O"
            messages.append(f"The crow pecks O into square {crow_cell + 1}. 'Agricultural genius.'")
            self._settle()
        if self.result == "win":
            messages.append("Three Xs! You win. The crow requests an independent bird audit.")
        elif self.result == "loss":
            messages.append("Three Os. The crow wins and immediately puts 'champion' on its sign.")
        elif self.result == "draw":
            messages.append("A draw! 'Mutual intellectual magnificence,' declares the crow.")
        return messages

    def verified_result(self) -> str | None:
        """Confirm that the displayed result came from a complete legal game."""
        if not self.finished:
            return None
        replay = CrowGame()
        for cell in self._moves:
            if replay.finished:
                return None
            before = len(replay._moves)
            replay.play(cell)
            if len(replay._moves) != before + 1:
                return None
        if replay.board != self.board or replay.result != self.result:
            return None
        return replay.result
