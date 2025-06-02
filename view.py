import tkinter as tk
from tkinter import filedialog, ttk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from control import Controller

# https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, *args, **kw):
        super().__init__(parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient = "vertical")
        vscrollbar.pack(fill = "y", side = "right", expand = 0)
        canvas = tk.Canvas(self, bd = 0, highlightthickness = 0,
                           yscrollcommand = vscrollbar.set)
        canvas.pack(side = "left", fill = "both", expand = 1)
        vscrollbar.config(command = canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window = interior,
                                           anchor = "nw")

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion = "0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width = interior.winfo_reqwidth())
        interior.bind("<Configure>", _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width = canvas.winfo_width())
        canvas.bind("<Configure>", _configure_canvas)

        def _on_mousewheel(event):
            delta = (int)(event.delta / 120)
            canvas.yview_scroll(-1 * delta, "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)


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
        flt_tab_base = VerticalScrolledFrame(tabcontrol)
        chr_tab_base = VerticalScrolledFrame(tabcontrol)
        tabcontrol.add(flt_tab_base, text = "Filters")
        tabcontrol.add(chr_tab_base, text = "Characters")
        tabcontrol.pack(expand = 1, fill = "both")

        self.root = root
        self.flt_tab = flt_tab_base.interior
        self.chr_tab = chr_tab_base.interior
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
                c_label = ttk.Label(frame, text = content, justify = "left")
                k_label.grid(row = row, column = 0)
                c_label.grid(row = row, column = 1, sticky = "w")
            elif c_type == "sub_frame":
                sub_frame = ttk.Labelframe(frame, text = label,
                                           relief = tk.GROOVE, border = 10)
                sub_frame.grid(row = row, column = 1, sticky = "w")
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
    
    def refresh_tabs(self, node_list: list, tab: str):
        self.destroy_tabs(tab)
        frames = []
        for node in node_list:
            frames.append(self.create_frame(node, tab))
        if tab == "filter":
            self.flt_frames = frames
        elif tab == "character":
            self.chr_frames = frames
        else:
            raise ValueError(f"tab '{tab}' not found at refresh_tabs")
    
    def destroy_tabs(self, tab: str):
        if tab == "filter":
            destroy = self.flt_frames
            self.flt_frames = []
        elif tab == "character":
            destroy = self.chr_frames
            self.chr_frames = []
        else:
            raise ValueError(f"tab '{tab}' not found at destroy_tabs")
        for frame in destroy:
            frame.destroy()

    def start(self):
        self.root.mainloop()



if __name__ == "__main__":
    window = View()
    window.start()