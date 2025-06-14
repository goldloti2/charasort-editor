import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
from typing import TYPE_CHECKING

from .display_record import DisplayRecord
from .edit_view import EditView
from .widgets import VerticalScrolledFrame

if TYPE_CHECKING:
    from control import Controller


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
        self.edit_window = None

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

    def _display_frame(self, record: dict, tab: str) -> ttk.Frame:
        # create base frame
        if tab == "filters":
            frame = ttk.Frame(self.flt_tab, relief=tk.GROOVE, border=10)
        elif tab == "characters":
            frame = ttk.Frame(self.chr_tab, relief=tk.GROOVE, border=10)
        frame.columnconfigure(1, weight=1)
        frame.grid(column=0, sticky=tk.EW)

        # add information
        DisplayRecord(record, frame, False)

        # add buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=0, column=2, rowspan=4, sticky=tk.NW)
        button_edit = ttk.Button(
            button_frame, text="edit", command=lambda: self._button_edit(frame, tab)
        )
        button_edit.pack(fill=tk.X)
        button_delete = ttk.Button(
            button_frame,
            text="delete",
            command=lambda: self._button_delete(frame, tab),
        )
        button_delete.pack(fill=tk.X)
        if tab == "filters":
            button_up = ttk.Button(
                button_frame, text="↑", command=lambda: self._button_move(frame, -1)
            )
            button_up.pack(fill=tk.X)
            button_down = ttk.Button(
                button_frame, text="↓", command=lambda: self._button_move(frame, 1)
            )
            button_down.pack(fill=tk.X)
        return frame

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

    def _button_edit(self, frame: ttk.Frame, tab: str):
        if self.edit_window:
            self.edit_window.focus()
            return

        # temporary restrict edit button to filter only
        if tab != "filters":
            return

        index = frame.grid_info()["row"]
        record = self.controller.get_record(index, tab)

        self.edit_window = EditView(
            self.root, record, lambda save: self._callback_edit_return(save, index, tab)
        )
        self.edit_window.focus()

    def _button_delete(self, frame: ttk.Frame, tab: str):
        if not self.edit_window:
            self.controller.delete_record(frame.grid_info()["row"], tab)

    def _button_move(self, frame: ttk.Frame, direction: int):
        if not self.edit_window:
            self.controller.move_filter(frame.grid_info()["row"], direction)

    def _callback_edit_return(self, save: dict, index: int, tab: str):
        self.edit_window = None
        if save:
            self.controller.update_record(save, index, tab)


if __name__ == "__main__":
    window = View()
    window.start()
