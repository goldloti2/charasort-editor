import tkinter as tk
from datetime import datetime
from functools import partial
from tkinter import filedialog, messagebox, ttk
from typing import TYPE_CHECKING

from utils import TabType

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

        menu = self._build_menu(root)
        root.config(menu=menu)

        tabcontrol = ttk.Notebook()
        filters_tab_base = VerticalScrolledFrame(tabcontrol)
        characters_tab_base = VerticalScrolledFrame(tabcontrol)
        tabcontrol.add(filters_tab_base, text="Filters")
        tabcontrol.add(characters_tab_base, text="Characters")
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

        self.controller = controller
        self.root = root
        self.tabs = {
            TabType.FILTERS: filters_tab_base.interior,
            TabType.CHARACTERS: characters_tab_base.interior,
        }
        self.detail_label_style = detail_label_style
        self.edit_window = None

    def start(self):
        self.root.mainloop()

    def refresh_tabs(self, node_list: list, tab: TabType):
        self.destroy_tabs(tab)
        parent = self.tabs[tab]
        callbacks = [
            ("edit", partial(self._button_edit, tab=tab)),
            ("delete", partial(self._button_delete, tab=tab)),
        ]
        if tab == TabType.FILTERS:
            callbacks.extend(
                [
                    ("↑", partial(self._button_move, direction=-1)),
                    ("↓", partial(self._button_move, direction=1)),
                ]
            )
        frame = DisplayFrame(parent, node_list[0], callbacks)
        if tab == TabType.FILTERS:
            frame.disable_up()
        for node in node_list[1:-1]:
            DisplayFrame(parent, node, callbacks)
        if len(node_list) > 1:
            frame = DisplayFrame(parent, node_list[-1], callbacks)
        if tab == TabType.FILTERS:
            frame.disable_down()

    def destroy_tabs(self, tab: TabType):
        destroy = self.tabs[tab].winfo_children()
        if not destroy:
            return
        for frame in destroy:
            frame.destroy()

    def _build_menu(self, root: tk.Tk):
        menu = tk.Menu(root)
        menu_specs = [
            ("Open", self._menu_open),
            ("Save", self._menu_save),
            ("Save To", self._menu_save_to),
        ]
        for label, command in menu_specs:
            menu.add_command(label=label, command=command)

        return menu

    def _menu_open(self):
        path = filedialog.askopenfilename(
            initialdir=".", filetypes=[("JavaScript (*.js)", "*.js"), ("all (*)", "*")]
        )
        if path:
            self.destroy_tabs(TabType.FILTERS)
            self.destroy_tabs(TabType.CHARACTERS)
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

    def _button_edit(self, frame: ttk.Frame, tab: TabType):
        if self.edit_window:
            self.edit_window.focus()
            return

        # temporary restrict edit button to filter only
        if tab != TabType.FILTERS:
            return

        index = frame.grid_info()["row"]
        record = self.controller.get_record(index, tab)

        self.edit_window = EditView(
            self.root, record, lambda save: self._on_edit_return(save, index, tab)
        )
        self.edit_window.focus()

    def _button_delete(self, frame: ttk.Frame, tab: TabType):
        if not self.edit_window:
            self.controller.delete_record(frame.grid_info()["row"], tab)

    def _button_move(self, frame: ttk.Frame, direction: int):
        if not self.edit_window:
            self.controller.move_filter(frame.grid_info()["row"], direction)

    def _on_edit_return(self, save: dict, index: int, tab: TabType):
        self.edit_window = None
        if save:
            self.controller.update_record(save, index, tab)


class DisplayFrame:
    def __init__(self, parent: ttk.Frame, record: dict, callbacks: list):
        # create base frame
        frame = ttk.Frame(parent, relief=tk.GROOVE, border=10)
        frame.columnconfigure(1, weight=1)
        frame.grid(column=0, sticky=tk.EW)

        # add information
        DisplayRecord(record, frame, False)

        # add buttons
        self.button_up = None
        self.button_down = None
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=0, column=2, rowspan=4, sticky=tk.NW)
        for label, callback in callbacks:
            button = ttk.Button(
                button_frame, text=label, command=partial(callback, frame=frame)
            )
            button.pack(fill=tk.X)
            if label == "↑":
                self.button_up = button
            elif label == "↓":
                self.button_down = button

        self.frame = frame

    def disable_up(self):
        if self.button_up:
            self.button_up.config(state=tk.DISABLED)

    def disable_down(self):
        if self.button_down:
            self.button_down.config(state=tk.DISABLED)


if __name__ == "__main__":
    window = View()
    window.start()
