from tkinter import *

window = Tk()
window.geometry("720x720")
window.title("SudOK")

mainlabel = Label(window, text="Time for sudoku!",font=('Arial',20), fg='#032a5e', padx=5, pady=5)

mainlabel.pack()


def click():
    print(("Youve clicked"))


def submit():
    username = entrybox.get()
    print(f' hi {username}')

button = Button(window, text="SOLVE",command=click)


button.pack()


entrybox = Entry(window, font=("Arial",20))
entrybox.pack()

submitbutton = Button(window, text='submit', command=submit)
submitbutton.pack(side=RIGHT)

def delete():
    entrybox.delete(0,END)

deletebutton = Button(window, text='delete', command=delete)
deletebutton.pack(side=RIGHT)


window.mainloop()

