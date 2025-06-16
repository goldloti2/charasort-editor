import tkinter as tk
from datetime import datetime
from functools import partial
from tkinter import filedialog, messagebox, ttk
from typing import TYPE_CHECKING

from utils import ButtonLabel, TabType

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
        callbacks = self._create_button_callbacks(tab)
        is_filter_tab = tab == TabType.FILTERS
        last_index = len(node_list) - 1

        for idx, node in enumerate(node_list):
            is_first = (idx == 0) and is_filter_tab
            is_last = (idx == last_index) and is_filter_tab
            self._build_display_frame(parent, node, is_first, is_last, callbacks)

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

    def _build_display_frame(
        self,
        parent: ttk.Frame,
        record: dict,
        is_first: bool,
        is_last: bool,
        callbacks: dict,
    ):
        frame = DisplayFrame(parent, record, callbacks)
        frame.disable_move(is_first, is_last)
        return frame

    def _create_button_callbacks(self, tab: TabType):
        callbacks = {
            ButtonLabel.EDIT: partial(self._button_edit, tab=tab),
            ButtonLabel.DELETE: partial(self._button_delete, tab=tab),
        }
        if tab == TabType.FILTERS:
            callbacks[ButtonLabel.MOVEUP] = partial(self._button_move, direction=-1)
            callbacks[ButtonLabel.MOVEDOWN] = partial(self._button_move, direction=1)
        return callbacks

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


class DisplayFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame, record: dict, callbacks: dict):
        # create base frame
        super().__init__(parent, relief=tk.GROOVE, border=10)
        self.columnconfigure(1, weight=1)
        self.grid(column=0, sticky=tk.EW)

        # add information
        DisplayRecord(record, self, False)

        # add buttons
        self.button_up = None
        self.button_down = None
        button_frame = ttk.Frame(self)
        button_frame.grid(row=0, column=2, rowspan=4, sticky=tk.NW)
        for label, callback in callbacks.items():
            button = ttk.Button(
                button_frame, text=label.value, command=partial(callback, frame=self)
            )
            button.pack(fill=tk.X)
            if label == ButtonLabel.MOVEUP:
                self.button_up = button
            elif label == ButtonLabel.MOVEDOWN:
                self.button_down = button

    def disable_move(self, is_first: bool, is_last: bool):
        if self.button_up and is_first:
            self.button_up.config(state=tk.DISABLED)
        if self.button_down and is_last:
            self.button_down.config(state=tk.DISABLED)


if __name__ == "__main__":
    window = View()
    window.start()
