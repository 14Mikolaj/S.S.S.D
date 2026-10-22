"""Readable, numbered game boards; the grid never relies on color."""

from .presentation import beside


CROW = r'''
           ___
          /   '.
         |  o  >
         |    /  CAW.
      ___/   /   YOUR MOVE.
     /      /|
    /  /   / |
   /  /   /  |
  /__/___/___/
      |   |
    __|___|__
 === THE FENCE ===
'''.strip("\n")


def crow_board(board, width=78, height=24):
    """Keep the whole board visible; give roomy terminals a larger board."""
    large = width >= 100 and height >= 36
    inside = 11 if large else 7
    cross = ["\\   /", " \\ / ", "  X  ", " / \\ ", "/   \\"] if large else ["\\ /", " X ", "/ \\"]
    nought = [" .---. ", "/     \\", "|     |", "\\     /", " '---' "] if large else ["/-\\", "| |", "\\-/"]
    cell_height = len(cross)
    edge = "+" + "+".join(["-" * inside] * 3) + "+"
    rows = [edge]
    for row in range(3):
        for line in range(cell_height):
            cells = []
            for column in range(3):
                index = row * 3 + column
                mark = board[index]
                value = (cross if mark == "X" else nought)[line] if mark in {"X", "O"} else (
                    f"[{index + 1}]" if line == cell_height // 2 else "")
                cells.append(value.center(inside))
            rows.append("|" + "|".join(cells) + "|")
        rows.append(edge)
    grid = "\n".join(rows)
    paired = beside(grid, CROW, gap=7)
    return paired if max(map(len, paired.splitlines())) <= width else grid


def plain_board(board):
    return "\n".join(" | ".join(board[index] if board[index] != " " else str(index + 1)
                                  for index in range(row, row + 3))
                     for row in (0, 3, 6))
