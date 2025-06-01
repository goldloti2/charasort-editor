import tkinter as tk
from tkinter import filedialog
from tkinter.constants import CENTER

import controls

option_list = []


def init(title = "charasort editor"):
    window = tk.Tk()
    window.title(title)
    window.geometry("600x800")
    window.resizable(False, False)

    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar)
    filemenu.add_command(label = "Open", command = menu_open)
    filemenu.add_command(label = "Save")
    filemenu.add_command(label = "Save As")
    menubar.add_cascade(label = "File", menu = filemenu)
    window.config(menu = menubar)
    
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side = "right", fill = "y")
    return window

def menu_open():
    controls.open_file("test.js")


if __name__ == "__main__":
    window = init()
    window.mainloop()