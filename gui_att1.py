from tkinter import *
from tkinter import messagebox  # idk, but it just didn't work from the previous line only
from board import SudokuBoard
from tkinter import filedialog
from solver_babyversion import solve_backtracking
from solver_constraintpropagation import solve_combined, solve_constraint


window = Tk()
window.minsize(220, 220)
window.title("SudOK")


main_label = Label(window, text="Time for sudoku!", font=('Arial', 20),
                   fg='#032a5e', padx=5, pady=5).grid(row=0, column=2)

# creating grid for inputs

# framing the place the grid will be put
grid_frame = Frame(window)
grid_frame.grid(row=1, column=1, columnspan=3, pady=(0, 10))


# we only want a single digit to be entered (or a space)
def char_validation(new_value):
    """
    Checks whether the entered value makes sense: is a single digit or a space.
    :param new_value:
    :return: True or False, depending on if the value is ok
    """
    if new_value == "":
        return True
    if new_value == " ":
        return True
    if len(new_value) == 1 and new_value.isdigit():  # sudoku is only single digit numbers
        return True
    return False


validationcommand = (window.register(char_validation), "%P")  # will check inputs before displaying them

entryboxes = [[None for i in range(9)] for j in range(9)]  # generate list of lists of right size

for rows in range(9):
    for cols in range(9):  # for each place
        entrybox = Entry(grid_frame, width=2, font=("Arial", 20), justify=CENTER,
                         validate="key", validatecommand=validationcommand)  # create entry box

        padx = (0, 5) if cols in [2,5] else (0,1)  # padding to separate 3x3s
        pady = (0, 5) if rows in [2,5] else (0,1)

        entrybox.grid(row=rows + 1, column=cols + 1, padx=padx, pady=pady)  # find its place on a grid

        entryboxes[rows][cols] = entrybox  # insert box


# buttons and their functionality
def read_grid():
    """
    Reads each number in the Entry boxes on screen and puts them in their place in the list of lists.
    :return: List(List()) of 9x9 sudoku board, with 0 representing empty fields.
    """
    board = [[None for i in range(9)] for j in range(9)]  # generate empty board for input
    for row in range(0, 9):
        for col in range(0, 9):
            num = entryboxes[row][col].get()  # get entered values

            if num not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:  # if number wrong, set to empty
                num = 0
            else:
                num = int(num)  # else convert string to integer

            board[row][col] = num  # put the input in the right place on board

    return SudokuBoard(board)  #  create the SudokuBoard object and return it


def print_board(sudoku: SudokuBoard):
    """
    Returns the solved sudoku board into the grid of cells it was entered to.
    :param sudoku: SudokuBoard object of the playing field.
    """
    for row in range(0, 9):
        for col in range(0, 9):
            entryboxes[row][col].delete(0)  # empties input box
            num = sudoku.get_value(row, col)  # gets value from the object
            entryboxes[row][col].insert(0, num)  # inserts it into the playing field


def click_solve():
    """
    Calls the sudoku solver to solve the sudoku and then returns the solution.
    """
    board = read_grid()  # reads the playing field
    choice = selected_solver.get()
    if choice == "backtracking":
        solved_board = solve_backtracking(board)  # solves board
    elif choice == "constraint":
        solved_board = solve_constraint(board)
    else:
        solved_board = solve_combined(board)
    print(choice)
    print_board(solved_board)  # returns results


def click_validate():
    """
    Performs the validation of the entered sudoku puzzle.
    """
    board = read_grid()  # reads input
    if board.initial_validation():  # checks if solution possible
        messagebox.showinfo("SudOK", "Board is valid!")  # popups with results of validation
    else:
        messagebox.showinfo("SudOK", "Board is invalid! :(")


def click_delete():
    """
    Clears the whole sudoku grid.
    """
    for row in range(0,9):
        for col in range(0,9):
            entryboxes[row][col].delete(0)


button_frame = Frame(window)
button_frame.grid(row=2, column=1, columnspan=3,pady=(0,10), )  # buttons at the bottom

solve_button = Button(button_frame, text="SOLVE", command=click_solve).grid(row=0,column=2)

validate_button = Button(button_frame, text='VALIDATE', command=click_validate).grid(row=0, column=1, padx=(0,10))

delete_button = Button(button_frame, text='CLEAR', command=click_delete).grid(row=0, column=0, padx=(0,10))


# menu time

menubar = Menu(window)

def export_sudoku():
    """
    Saves the current board into a .txt file
    """
    board = read_grid()
    file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    file.write(str(board))  # saves into .txt chosen
    file.close()


def import_sudoku():
    file = filedialog.askopenfile(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    file_contents = file.read()
    file.close()

    lines = file_contents.splitlines()  # splits lines
    grid = []  # place to store the input

    for line in lines:
        nums = [int(x) for x in line.split()]  # extracts the numbers from lines
        grid.append(nums)  # stores in grid

    print_board(SudokuBoard(grid))  # returns onto the playing field
    for row in range(0,9):
        for col in range(0,9):
            if entryboxes[row][col].get() == "0":  # empties boxes that are empty (deletes the printed 0s)
                entryboxes[row][col].delete(0)
    return


fileMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=fileMenu)

fileMenu.add_command(label="Import Sudoku", command=import_sudoku)
fileMenu.add_command(label="Export Sudoku", command=export_sudoku)


def load_sample(sample):  # just loads some stored sample sudoku
    if sample == "sample1":
        sampleboard = SudokuBoard([[5, 3, 0, 0, 7, 0, 0, 0, 0],
                                   [6, 0, 0, 1, 9, 5, 0, 0, 0],
                                   [0, 9, 8, 0, 0, 0, 0, 6, 0],
                                   [8, 0, 0, 0, 6, 0, 0, 0, 3],
                                   [4, 0, 0, 8, 0, 3, 0, 0, 1],
                                   [7, 0, 0, 0, 2, 0, 0, 0, 6],
                                   [0, 6, 0, 0, 0, 0, 2, 8, 0],
                                   [0, 0, 0, 4, 1, 9, 0, 0, 5],
                                   [0, 0, 0, 0, 8, 0, 0, 7, 9]])

    elif sample == "sample2":
        sampleboard = SudokuBoard([[7, 2, 3, 0, 0, 0, 0, 4, 0],
                                   [0, 0, 9, 1, 0, 0, 0, 0, 0],
                                   [1, 0, 0, 9, 4, 0, 0, 0, 0],
                                   [0, 3, 0, 0, 0, 4, 7, 0, 0],
                                   [6, 1, 0, 0, 3, 0, 0, 9, 4],
                                   [0, 0, 7, 8, 0, 0, 0, 2, 0],
                                   [0, 0, 0, 0, 7, 9, 0, 0, 5],
                                   [0, 0, 0, 0, 0, 1, 9, 0, 0],
                                   [0, 5, 0, 0, 0, 0, 6, 7, 1]])

    print_board(sampleboard)  # returns those to the playing field

    for row in range(0,9):
        for col in range(0,9):
            if entryboxes[row][col].get() == "0":  # empty fields are truly empty, not 0
                entryboxes[row][col].delete(0)



sampleMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Sample puzzles", menu=sampleMenu)

sampleMenu.add_command(label="Sample 1", command=lambda: load_sample("sample1"))
sampleMenu.add_command(label="Sample 2", command=lambda: load_sample("sample2"))

solverMenu = Menu(menubar, tearoff=0)

selected_solver = StringVar(value="combined")  # default setting

menubar.add_cascade(label="Solver", menu=solverMenu)

solverMenu.add_radiobutton(label="Backtracking bruteforce", variable=selected_solver,
                           value="backtracking")

solverMenu.add_radiobutton(label="Simple constraint propagation", variable=selected_solver,
                           value="constraint")

solverMenu.add_radiobutton(label="Combined (default)", variable=selected_solver,
                           value="combined")


window.config(menu=menubar)

# get_solver()

window.mainloop()
