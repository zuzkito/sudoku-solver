"""
Basic bruteforce backtracking algorithm.
"""
from board import *

def solve_backtracking(sudoku):
        """
        Checks if valid and tries to solve the sudoku.
        :param sudoku: A sudoku playing field (SudokuBoard object) to be solved.
        :return: True in case it is solved, False if not valid, edits the SudokuBoard
        """

        if sudoku.initial_validation() == False:
                print("The entered sudoku board is not valid.")
                return False

        empty = sudoku.find_empty() # make sure it is not solved yet
        if empty == None:
                return sudoku  # sudoku solved fully
        # print(f"{sudoku} \n")

        row, col = empty
        for i in range(1,10):
                if sudoku.is_move_valid(row,col, i):
                        sudoku.set_value(row, col, i)

                        solved = solve_backtracking(sudoku)
                        if solved:  # all that's not fase is kind of true
                                return solved  # this needed for the sudoku to get returned all the way up


                        sudoku.set_value(row, col, 0)  # if not, we're setting back to 0 and backtracking
