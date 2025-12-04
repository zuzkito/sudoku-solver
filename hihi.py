from tkinter import *

window = Tk()
window.title("SudOK")
window.minsize(400, 400)

# -------------------------------------------------
# 1. Make the main grid resizable
# -------------------------------------------------
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)

# Title
main_label = Label(window, text="Time for sudoku!", font=('Arial', 20), fg='#032a5e')
main_label.grid(row=0, column=1, pady=10)

# -------------------------------------------------
# 2. Sudoku grid inside a resizable frame
# -------------------------------------------------
grid_frame = Frame(window)
grid_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

# Make the 9×9 grid resizable
for i in range(9):
    grid_frame.grid_rowconfigure(i, weight=1)
    grid_frame.grid_columnconfigure(i, weight=1)

entryboxes = [[None]*9 for _ in range(9)]
cell_font = ("Arial", 14)

for r in range(9):
    for c in range(9):
        padx = (0,5) if c in [2,5] else 1
        pady = (0,5) if r in [2,5] else 1

        e = Entry(grid_frame, justify="center", font=cell_font)
        e.grid(row=r, column=c, padx=padx, pady=pady, sticky="nsew")

        entryboxes[r][c] = e

# -------------------------------------------------
# 3. Buttons at the bottom
# -------------------------------------------------
def click_solve(): pass
def click_validate(): pass
def click_clear(): pass

button_frame = Frame(window)
button_frame.grid(row=2, column=1, pady=10)

Button(button_frame, text="CLEAR", command=click_clear).pack(side=LEFT, padx=10)
Button(button_frame, text="VALIDATE", command=click_validate).pack(side=LEFT, padx=10)
Button(button_frame, text="SOLVE", command=click_solve).pack(side=LEFT, padx=10)

# -------------------------------------------------
# 4. Auto-scale fonts on resize
# -------------------------------------------------
def scale_fonts(event):
    size = max(8, int(window.winfo_height() / 45))
    new_font = ("Arial", size)
    for r in range(9):
        for c in range(9):
            entryboxes[r][c].config(font=new_font)

window.bind("<Configure>", scale_fonts)

window.mainloop()
