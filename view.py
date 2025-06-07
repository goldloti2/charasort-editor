import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
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
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=0)
        canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set
        )
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(canvas)
        interior.columnconfigure(0, weight=1)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind("<Configure>", _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind("<Configure>", _configure_canvas)

        def _on_mousewheel(event):
            delta = (int)(event.delta / 120)
            canvas.yview_scroll(-1 * delta, "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)


class View:
    def __init__(self, controller: "Controller"):
        root = tk.Tk()
        root.title("charasort editor")
        root.geometry("600x800")
        root.resizable(False, False)

        menubar = tk.Menu(root)
        menubar.add_command(label="Open", command=self._menu_open)
        menubar.add_command(label="Save", command=self._menu_save)
        menubar.add_command(label="Save To", command=self._menu_save_to)
        root.config(menu=menubar)

        tabcontrol = ttk.Notebook()
        flt_tab_base = VerticalScrolledFrame(tabcontrol)
        chr_tab_base = VerticalScrolledFrame(tabcontrol)
        tabcontrol.add(flt_tab_base, text="Filters")
        tabcontrol.add(chr_tab_base, text="Characters")
        tabcontrol.pack(expand=1, fill=tk.BOTH)

        detail_label_style = ttk.Style()
        detail_label_style.configure(
            "detail_label.TLabel",
            background="white",
            border=1,
            padding=1,
            relief=tk.SOLID,
            wraplength=150,
        )

        self.root = root
        self.flt_tab = flt_tab_base.interior
        self.chr_tab = chr_tab_base.interior
        self.detail_label_style = detail_label_style
        self.controller = controller

    def start(self):
        self.root.mainloop()

    def refresh_tabs(self, node_list: list, tab: str):
        self.destroy_tabs(tab)
        frame = self._display_frame(node_list[0], tab)
        if tab == "filters":
            frame.children["!frame"].children["!button3"].config(state=tk.DISABLED)
        for node in node_list[1:-1]:
            self._display_frame(node, tab)
        if len(node_list) > 1:
            frame = self._display_frame(node_list[-1], tab)
        if tab == "filters":
            frame.children["!frame"].children["!button4"].config(state=tk.DISABLED)

    def destroy_tabs(self, tab: str):
        if tab == "filters":
            destroy = self.flt_tab.winfo_children()
        elif tab == "characters":
            destroy = self.chr_tab.winfo_children()
        else:
            raise ValueError(f"tab '{tab}' not found in view.destroy_tabs")
        if not destroy:
            return
        for frame in destroy:
            frame.destroy()

    def _display_frame(self, object: dict, tab: str) -> ttk.Frame:
        # create base frame
        if tab == "filters":
            frame = ttk.Frame(self.flt_tab, relief=tk.GROOVE, border=10)
        elif tab == "characters":
            frame = ttk.Frame(self.chr_tab, relief=tk.GROOVE, border=10)
        frame.columnconfigure(1, weight=1)
        frame.grid(column=0, sticky=tk.EW)

        # add information
        self._display_object_info(object, frame)

        # add buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=0, column=2, rowspan=4, sticky=tk.NW)
        button_edit = ttk.Button(button_frame, text="edit", command=None)
        button_edit.pack(fill=tk.X)
        button_delete = ttk.Button(
            button_frame,
            text="delete",
            command=lambda: self._button_delete(frame, tab),
        )
        button_delete.pack(fill=tk.X)
        if tab == "filters":
            button_up = ttk.Button(
                button_frame, text="↑", command=lambda: self._button_move_up(frame)
            )
            button_up.pack(fill=tk.X)
            button_down = ttk.Button(
                button_frame, text="↓", command=lambda: self._button_move_down(frame)
            )
            button_down.pack(fill=tk.X)
        return frame

    def _display_object_info(self, object: dict, frame: ttk.Frame):
        row = 0
        for attr in object:
            c_type, label, content = attr
            if c_type == "label":
                k_label = ttk.Label(frame, text=label + ":")
                c_label = ttk.Label(frame, text=content, justify=tk.LEFT)
                k_label.grid(row=row, column=0)
                c_label.grid(row=row, column=1, sticky=tk.W)
            elif c_type == "check":
                k_label = ttk.Label(frame, text=label + ":")
                c_check = tk.Checkbutton(frame, state=tk.DISABLED)
                if content:
                    c_check.select()
                else:
                    c_check.deselect()
                k_label.grid(row=row, column=0)
                c_check.grid(row=row, column=1, sticky=tk.W)
            elif c_type == "sub_frame":
                sub_frame = ttk.Labelframe(
                    frame, text=label, relief=tk.GROOVE, border=10
                )
                sub_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W)
                tree = ttk.Treeview(
                    sub_frame,
                    columns=content[0],
                    height=10,
                    selectmode=tk.BROWSE,
                    show="headings",
                )
                tree.heading("#1", text=content[0][0])
                tree.heading("#2", text=content[0][1])
                for sub_content in content[1:]:
                    tree.insert("", "end", values=sub_content)
                scrollbar = ttk.Scrollbar(sub_frame, command=tree.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                tree.configure(yscrollcommand=scrollbar.set)
                detail_label = ttk.Label(frame, style="detail_label.TLabel")
                tree.bind(
                    "<ButtonRelease-1>",
                    lambda event: self._treeview_select(event, detail_label),
                )
                tree.bind(
                    "<Escape>",
                    lambda event: self._treeview_deselect(event, detail_label),
                )
                tree.pack(expand=1, fill=tk.BOTH)
            else:
                raise ValueError(f"c_type '{c_type}' not found in view._display_frame")
            row += 1

    def _treeview_select(self, event: tk.Event, label: ttk.Label):
        focus = event.widget.focus()
        if focus:
            item = event.widget.item(focus, "values")
            label.config(text=item[1])
            cursor_x = event.x + event.widget.master.winfo_x()
            cursor_y = event.y + event.widget.master.winfo_y()
            label.place(
                anchor=tk.NW,
                x=cursor_x,
                y=cursor_y,
                width=155,
            )

    def _treeview_deselect(self, event: tk.Event, label: ttk.Label):
        event.widget.selection_remove(event.widget.focus())
        label.place_forget()

    def _menu_open(self):
        path = filedialog.askopenfilename(
            initialdir=".", filetypes=[("JavaScript (*.js)", "*.js"), ("all (*)", "*")]
        )
        if path:
            self.destroy_tabs("filters")
            self.destroy_tabs("characters")
            self.controller.open_file(path)

    def _menu_save(self):
        result = messagebox.askyesno(
            "Overwrite", "Do you want to overwrite the old file?"
        )
        if result:
            self.controller.save_file()

    def _menu_save_to(self):
        path = filedialog.asksaveasfilename(
            initialdir=".",
            initialfile=f"{datetime.now().strftime('%Y-%m-%d')}.js",
            defaultextension=".js",
            filetypes=[("JavaScript (*.js)", "*.js"), ("all (*)", "*")],
        )
        if path:
            self.controller.save_file(path)

    def _button_delete(self, frame: ttk.Frame, tab: str):
        self.controller.delete_object(frame.grid_info()["row"], tab)

    def _button_move_up(self, frame: ttk.Frame):
        self.controller.move_filter(frame.grid_info()["row"], "up")

    def _button_move_down(self, frame: ttk.Frame):
        self.controller.move_filter(frame.grid_info()["row"], "down")


if __name__ == "__main__":
    window = View()
    window.start()
