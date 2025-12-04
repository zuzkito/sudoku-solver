# debug_solver.py
from board import SudokuBoard
import copy

def tryout(sudoku):
    grid = SudokuBoard([row.copy() for row in sudoku.board])

    for r in range(9):
        for c in range(9):
            if sudoku.get_value(r, c) == 0:
                poss = ""
                for i in range(1, 10):
                    if sudoku.is_move_valid(r, c, i):
                        poss += str(i)
                grid.set_value(r, c, poss)
            else:
                # KEEP ORIGINAL INTEGER, not a string
                grid.set_value(r, c, sudoku.get_value(r, c))
    return grid


def set_possibilities(grid, sudoku):
    changed = False
    for r in range(9):
        for c in range(9):
            field = grid.get_value(r, c)

            # only strings represent possibilities
            if isinstance(field, str) and len(field) == 1:
                if sudoku.get_value(r, c) == 0:
                    sudoku.set_value(r, c, int(field))
                    changed = True
    return changed

def constraint_solver_verbose(sudoku: SudokuBoard):
    """
    Run repeated single-candidate propagation, printing progress each iteration.
    Stops when no single-candidate cell is found.
    """
    iteration = 0
    while True:
        iteration += 1
        print("\n--- Iteration", iteration, "---")
        grid = tryout(sudoku)
        # OPTIONAL: print grid of possibilities in readable form
        print("Possibilities-grid snapshot (0 means filled cell):")
        for r in range(9):
            row_repr = []
            for c in range(9):
                v = grid.get_value(r, c)
                row_repr.append(str(v))
            print(" ".join(row_repr))

        did_fill = set_possibilities(grid, sudoku)
        print("Board after applying single-candidates:")
        print(sudoku)

        if not did_fill:
            print("No single-candidate fillings found this iteration. Stopping.")
            break

    print("\nFinal board (partial/full):\n", sudoku)


sampleboard = SudokuBoard([ [7, 2, 3, 0, 0, 0, 0, 4, 0],
                                   [0, 0, 9, 1, 0, 0, 0, 0, 0],
                                   [1, 0, 0, 9, 4, 0, 0, 0, 0],
                                   [0, 3, 0, 0, 0, 4, 7, 0, 0],
                                   [6, 1, 0, 0, 3, 0, 0, 9, 4],
                                   [0, 0, 7, 8, 0, 0, 0, 2, 0],
                                   [0, 0, 0, 0, 7, 9, 0, 0, 5],
                                   [0, 0, 0, 0, 0, 1, 9, 0, 0],
                                   [0, 5, 0, 0, 0, 0, 6, 7, 1]])


constraint_solver_verbose(sampleboard)