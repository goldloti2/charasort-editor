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
        filemenu.add_command(label = "Open", command = self.menu_open)
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
    
    def menu_open(self):
        path = filedialog.askopenfilename(initialdir = ".",
                                          filetypes = [("JavaScript (*.js)", "*.js"),
                                                       ("all (*)", "*")])
        if path != "":
            self.controller.open_file(path)
    
    def create_frame(self, object: dict, parent: str) -> ttk.Frame:
        if parent == "filter":
            frame = ttk.Frame(self.flt_tab, relief = tk.GROOVE, border = 10)
        elif parent == "character":
            frame = ttk.Frame(self.chr_tab, relief = tk.GROOVE, border = 10)
        else:
            raise ValueError(f"parent '{parent}' not found at create_frame")
        row = 0
        for attr in object:
            c_type, label, content = attr
            if c_type == "label":
                k_label = ttk.Label(frame, text = label)
                c_label = ttk.Label(frame, text = content)
                k_label.grid(row = row, column = 0)
                c_label.grid(row = row, column = 1, sticky = "w")
            elif c_type == "sub_frame":
                sub_frame = ttk.Labelframe(frame, text = label,
                                           relief = tk.GROOVE, border = 10)
                sub_frame.grid(row = row, column = 0,
                               columnspan = 2, sticky = "w")
                widget = ttk.Label(sub_frame, text = content[0][0])
                widget.grid(row = 0, column = 0)
                widget = ttk.Label(sub_frame, text = content[0][1])
                widget.grid(row = 0, column = 2)
                sub_row = 1
                for sub_content in content[1:]:
                    widget = ttk.Label(sub_frame, text = sub_content[0])
                    widget.grid(row = sub_row, column = 1, sticky = "w")
                    widget = ttk.Label(sub_frame, text = sub_content[1])
                    widget.grid(row = sub_row, column = 3, sticky = "w")
                    sub_row += 1
            else:
                raise ValueError(f"c_type '{c_type}' not found at create_frame")
            row += 1
        frame.pack(fill = "x")
        return frame
    
    def refresh_filters(self, flt_list: list):
        self.destroy_filters()
        for flt in flt_list:
            self.flt_frames.append(self.create_frame(flt, "filter"))
    
    def destroy_filters(self):
        for frame in self.flt_frames:
            frame.destroy()
        self.flt_frames = []
    
    def refresh_characters(self, chr_list: list):
        self.destroy_characters()
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
        self.chr_frames = []

    def start(self):
        self.root.mainloop()



if __name__ == "__main__":
    window = View()
    window.start()