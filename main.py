"""
The GUI that lets the user run the sudoku solver program, with all its functionalities.
"""

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from random import randint
from board import SudokuBoard
from solvers import solve_backtracking, solve_combined, solve_constraint


# creating a window
window = Tk()
window.title("SudOK")
window.resizable(False, False)
icon = PhotoImage(file="images/sud.png")
window.iconphoto(True, icon)


# sudoku time banner
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
    :param new_value: Whatever string the user tries to type into the input fields.
    :return: True or False, depending on if the value is ok
    """
    if new_value == "":
        return True
    elif new_value == " ":
        return True
    elif len(new_value) == 1 and new_value.isdigit():  # sudoku is only single digit numbers
        return True
    else:
        return False


validationcommand = (window.register(char_validation), "%P")  # will check inputs before displaying them

entryboxes = [[None for i in range(0, 9)] for j in range(0, 9)]  # generate list of lists of right size

for rows in range(0, 9):  # creating and placing input boxes
    for cols in range(0, 9):  # for each place in the list
        entrybox = Entry(grid_frame, width=2, font=("Arial", 20), justify=CENTER,
                         validate="key", validatecommand=validationcommand)  # create entry box

        padx = (0, 5) if cols in [2, 5] else (0, 1)  # padding to separate 3x3s
        pady = (0, 5) if rows in [2, 5] else (0, 1)

        entrybox.grid(row=rows + 1, column=cols + 1, padx=padx, pady=pady)  # find its place on the grid

        entryboxes[rows][cols] = entrybox  # insert box


# buttons and their functionality
def read_grid():
    """
    Reads each number in the Entry boxes on screen and puts them in their place in the list of lists.
    :return: SudokuBoard object including the input board.
    """
    board = [[None for i in range(0, 9)] for j in range(0, 9)]  # generate empty board for input

    for row in range(0, 9):
        for col in range(0, 9):
            num = entryboxes[row][col].get()  # get entered values

            if num not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:  # if number wrong, set to empty
                num = 0  # honestly just an extra insurance, because the characters should get validated
            else:
                num = int(num)  # else convert string to integer

            board[row][col] = num  # put the input in the right place on board

    return SudokuBoard(board)  # create the SudokuBoard and return it


def print_board(sudoku: SudokuBoard):
    """
    Returns the solved sudoku board into the grid of cells it was entered to for the user to see.
    :param sudoku: SudokuBoard object of the playing field.
    :return: None
    """
    for row in range(0, 9):
        for col in range(0, 9):
            entryboxes[row][col].delete(0)  # empties input box
            num = sudoku.get_value(row, col)  # gets value from the object
            entryboxes[row][col].insert(0, num)  # inserts it into the playing field
    return


def remove_zeroes():
    """
    Helper function, that removes zeroes from the playing field and leaves the boxes empty.
    :return: None
    """
    for row in range(0, 9):
        for col in range(0, 9):
            if entryboxes[row][col].get() == "0":  # if box contains 0
                entryboxes[row][col].delete(0)  # empty it
    return


def click_solve():
    """
    Calls the sudoku solver to solve the sudoku and then returns the solution.
    :return: None
    """
    board = read_grid()  # reads the playing field

    if not board.initial_validation():  # checks if board is ok
        messagebox.showinfo("SudOK", "Board is not valid!")  # pops up in case of invalid board

    else:  # call the wanted solver and solve
        choice = selected_solver.get()

        if choice == "backtracking":
            solved_board = solve_backtracking(board)  # solves board
        elif choice == "constraint":
            solved_board = solve_constraint(board)
        else:
            solved_board = solve_combined(board)

        print_board(solved_board)  # returns results
        remove_zeroes()
    return


def validation_result_message(message):
    """
    Shows quiet popup with the results of the validation.
    :param message: The message in the window displayed.
    :return: None
    """
    window = Toplevel()
    window.title("SudOK")
    window.geometry("220x100")
    window.resizable(False, False)

    Label(window, text=message, padx=20, pady=15).pack()
    Button(window, text="OK", command=window.destroy).pack(pady=(0, 10))
    return


def click_validate():
    """
    Performs the validation of the entered sudoku puzzle, shows a popup window with results.
    :return: None
    """
    board = read_grid()  # reads input

    if board.initial_validation():
        validation_result_message("Board is valid!")
    else:
        validation_result_message("Board is invalid! :(")
    return



def click_delete():
    """
    Clears the whole sudoku grid.
    :return: None
    """
    for row in range(0, 9):
        for col in range(0, 9):
            entryboxes[row][col].delete(0)
    return


# the buttons themselves
button_frame = Frame(window)
button_frame.grid(row=2, column=1, columnspan=3, pady=(0, 10), )  # buttons at the bottom

solve_button = Button(button_frame, text="SOLVE", command=click_solve).grid(row=0, column=2)
validate_button = Button(button_frame, text='VALIDATE', command=click_validate).grid(row=0, column=1, padx=(0, 10))
delete_button = Button(button_frame, text='CLEAR', command=click_delete).grid(row=0, column=0, padx=(0, 10))


# menu time
menubar = Menu(window)  # creates the menu bar


# file manipulation functionality and menu
def export_sudoku():
    """
    Lets the user save the current board into a .txt file.
    :return: None
    """
    board = read_grid()
    file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text file (.txt)", "*.txt")])
    file.write(str(board))  # saves into .txt chosen
    file.close()
    return


def import_sudoku():
    """
    Lets the user import a sudoku from a correctly formatted .txt file.
    :return: None
    """
    file = filedialog.askopenfile(defaultextension=".txt", filetypes=[("Text file (.txt)", "*.txt")])
    file_contents = file.read()
    file.close()

    lines = file_contents.splitlines()  # splits lines
    grid = []  # place to store the input

    for line in lines:
        nums = [int(x) for x in line.split()]  # extracts the numbers from lines
        grid.append(nums)  # stores in grid

    print_board(SudokuBoard(grid))  # returns onto the playing field
    remove_zeroes()
    return


# the menu cascade itself
fileMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=fileMenu)

fileMenu.add_command(label="Import sudoku", command=import_sudoku)
fileMenu.add_command(label="Export sudoku", command=export_sudoku)


def load_sample(sample):
    """
    Loads a stored sample sudoku of user's choice.
    :param sample: str  Which sample should be loaded.
    :return: None
    """
    if sample == "sample1":
        sampleboard = SudokuBoard([
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ])

    elif sample == "sample2":
        sampleboard = SudokuBoard([
            [7, 2, 3, 0, 0, 0, 0, 4, 0],
            [0, 0, 9, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 9, 4, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 4, 7, 0, 0],
            [6, 1, 0, 0, 3, 0, 0, 9, 4],
            [0, 0, 7, 8, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 7, 9, 0, 0, 5],
            [0, 0, 0, 0, 0, 1, 9, 0, 0],
            [0, 5, 0, 0, 0, 0, 6, 7, 1]
        ])

    elif sample == "sample3":
        sampleboard = SudokuBoard([
            [0, 0, 0, 0, 0, 0, 8, 0, 2],
            [0, 0, 0, 6, 0, 0, 1, 0, 0],
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 7, 0, 0, 0, 9, 0],
            [0, 0, 0, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 8, 5, 0, 0],
            [0, 0, 9, 0, 0, 0, 0, 3, 0],
            [4, 0, 0, 0, 9, 0, 0, 0, 0]
        ])

    elif sample == "sample4":
        sampleboard = SudokuBoard([
            [0, 0, 9, 0, 0, 0, 2, 0, 0],
            [0, 8, 0, 5, 0, 0, 0, 1, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 6],
            [0, 0, 6, 0, 9, 0, 0, 0, 0],
            [0, 5, 0, 8, 0, 0, 3, 0, 0],
            [4, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 9],
            [0, 3, 0, 0, 1, 0, 0, 8, 0],
            [0, 0, 0, 2, 0, 0, 5, 0, 0]
        ])

    print_board(sampleboard)  # returns those to the playing field
    remove_zeroes()
    return


# the menu cascade for handling the sample puzzles
sampleMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Sample puzzles", menu=sampleMenu)

sampleMenu.add_command(label="Sample 1", command=lambda: load_sample("sample1"))
sampleMenu.add_command(label="Sample 2", command=lambda: load_sample("sample2"))
sampleMenu.add_command(label="Sample 3 (hard)", command=lambda: load_sample("sample3"))
sampleMenu.add_command(label="Sample 4 (extreme)", command=lambda: load_sample("sample4"))

# menu with choices of solver algorithms

solverMenu = Menu(menubar, tearoff=0)

selected_solver = StringVar(value="combined")  # default setting

menubar.add_cascade(label="Solver", menu=solverMenu)

solverMenu.add_radiobutton(label="Backtracking bruteforce", variable=selected_solver, value="backtracking")
solverMenu.add_radiobutton(label="Simple constraint propagation", variable=selected_solver, value="constraint")
solverMenu.add_radiobutton(label="Combined (default)", variable=selected_solver, value="combined")


# help button and the manual
def open_help_window():
    """
    Opens a simple help window with instructions.
    :return: None
    """
    help_window = Toplevel()  # configure the window
    help_window.title("Help")
    help_window.geometry("400x300")
    help_window.resizable(False, False)

    help_text = (
        "Sudoku Solver Help\n\n"
        "Basic usage: \n"
        "• Click a cell and type a number to enter its value.\n"
        "• Click SOLVE to run the sudoku solver.\n"
        "• Click VALIDATE to check if the board breaks any rules.\n"
        "• Click CLEAR button to empty the board.\n\n"
        "More functions:\n"
        "• Load/save a Sudoku file using File → Import/export.\n"
        "• Enjoy some puzzle samples from the Sample puzzles menu.\n"
        "• Change solver algorithm in the Solver menu.\n"
        "• Enjoy what is hidden under the bonus button (her name is Briseis).\n"
        "\n\n"
        "But most importantly... Have fun!\n")  # the text in the manual

    label = Label(help_window, text=help_text, justify="left", anchor="nw")
    label.pack(fill="both", expand=True, padx=10, pady=10)


menubar.add_command(label="Help", command=open_help_window)


# bonus material
image_list = ["brus1.jpeg", "brus2.jpeg", "brus3.jpeg", "brus4.jpeg", "brus5.jpeg", "brus6.jpeg", "brus7.jpeg",
              "brus8.jpeg", "brus9.jpeg"]


def open_bonus():
    """
    Opens a new window with a randomized bonus picture.
    :return: None
    """
    index = randint(0, len(image_list) - 1)  # pick index of random image
    filename = "images/"+image_list[index]

    bonus_window = Toplevel()  # open window and configure it
    bonus_window.title(f"Random Bonus")
    bonus_window.resizable(False, False)

    img = Image.open(filename)  # load the image
    img = img.resize((300, 500))  # resize image
    tk_img = ImageTk.PhotoImage(img)

    bonus_window.img = tk_img  # store image reference
    Label(bonus_window, image=tk_img).pack()  # place image
    return


menubar.add_command(label="Bonus", command=open_bonus)

window.config(menu=menubar)

window.mainloop()  # puts the whole thing on screen
