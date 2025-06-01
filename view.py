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
        self.flt_frames = []
        self.chr_frames = []
        self.controller = controller
    
    def add_filters(self, flt_list: list):
        for flt in flt_list:
            frame = ttk.Frame(self.flt_tab, relief = tk.GROOVE, border = 10)
            lbl = []
            lbl.append(ttk.Label(frame, text = "name:"))
            lbl.append(ttk.Label(frame, text = "key:"))
            lbl.append(ttk.Label(frame, text = "tooltip:"))
            lbl.append(ttk.Label(frame, text = "checked:"))
            txt = []
            txt.append(ttk.Label(frame, text = flt["name"], justify = "left"))
            txt.append(ttk.Label(frame, text = flt["key"], justify = "left"))
            txt.append(ttk.Label(frame, text = flt.get("tooltip", ""),
                      justify = "left"))
            txt.append(ttk.Label(frame, text = flt.get("checked", ""),
                      justify = "left"))
            for i in range(len(lbl)):
                lbl[i].grid(row = i, column = 0)
                txt[i].grid(row = i, column = 1, sticky = "w")
            
            frame.pack(fill = "x")
            self.flt_frames.append(frame)
    
    def destroy_filters(self):
        for frame in self.flt_frames:
            frame.destroy()
    
    def add_characters(self, chr_list: list):
        for chr in chr_list:
            frame = ttk.Frame(self.chr_tab, relief = tk.GROOVE, border = 10)
            lbl = []
            lbl.append(ttk.Label(frame, text = "name:"))
            lbl.append(ttk.Label(frame, text = "img:"))
            txt = []
            txt.append(ttk.Label(frame, text = chr["name"], justify = "left"))
            txt.append(ttk.Label(frame, text = chr["img"], justify = "left"))
            for i in range(len(lbl)):
                lbl[i].grid(row = i, column = 0)
                txt[i].grid(row = i, column = 1, sticky = "w")
            
            frame.pack(fill = "x")
            self.chr_frames.append(frame)
    
    def destroy_characters(self):
        for frame in self.chr_frames:
            frame.destroy()

    def start(self):
        self.root.mainloop()



if __name__ == "__main__":
    window = View()
    window.start()