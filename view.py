import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.constants import CENTER

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from control import Controller


class View:
    def __init__(self, controller: 'Controller'):
        root = tk.Tk()
        root.title("charasort editor")
        root.geometry("600x800")
        root.resizable(False, False)

        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label = "Open", command = controller.open_file)
        filemenu.add_command(label = "Save")
        filemenu.add_command(label = "Save As")
        menubar.add_cascade(label = "File", menu = filemenu)
        root.config(menu = menubar)

        tabcontrol = ttk.Notebook()
        flt_tab = ttk.Frame(tabcontrol)
        chr_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(flt_tab, text = "Filters")
        tabcontrol.add(chr_tab, text = "Characters")
        tabcontrol.pack(expand = 1, fill = "both")

        ttk.Scrollbar(flt_tab).pack(side = "right", fill = "y")
        ttk.Scrollbar(chr_tab).pack(side = "right", fill = "y")

        self.root = root
        self.flt_tab = flt_tab
        self.chr_tab = chr_tab
        self.flt_frame = []
        self.chr_frame = []
        self.controller = controller
    
    def add_filter(self, flt):
        frame = ttk.Frame(self.flt_tab, relief = tk.GROOVE, border = 10)
        label = ttk.Label(frame, text = flt)
        label.pack()
        frame.pack(fill = "x")
        self.flt_frame.append(frame)

    def start(self):
        self.root.mainloop()



if __name__ == "__main__":
    window = View()
    window.start()