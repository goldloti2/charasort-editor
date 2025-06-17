import tkinter as tk
from datetime import datetime
from functools import partial
from tkinter import filedialog, messagebox, ttk
from typing import TYPE_CHECKING, Callable, Dict

from utils import ButtonLabel, TabType

from .display import DisplayRecordFrame
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

        tab_control = ttk.Notebook()
        filters_tab_base = VerticalScrolledFrame(tab_control)
        characters_tab_base = VerticalScrolledFrame(tab_control)
        tab_control.add(filters_tab_base, text="Filters")
        tab_control.add(characters_tab_base, text="Characters")
        tab_control.pack(expand=1, fill=tk.BOTH)

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
        is_filter_tab = tab is TabType.FILTERS
        last_index = len(node_list) - 1

        for idx, node in enumerate(node_list):
            is_first = (idx == 0) and is_filter_tab
            is_last = (idx == last_index) and is_filter_tab
            self._build_display_frame(parent, node, idx, callbacks, is_first, is_last)

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
        record: list,
        index: int,
        callbacks: Dict[ButtonLabel, Callable],
        is_first: bool,
        is_last: bool,
    ):
        frame = DisplayRecordFrame(parent, record, index, callbacks)
        frame.disable_move(is_first, is_last)

    def _create_button_callbacks(self, tab: TabType):
        callbacks = {
            ButtonLabel.EDIT: partial(self._button_edit, tab=tab),
            ButtonLabel.DELETE: partial(self._button_delete, tab=tab),
        }
        if tab is TabType.FILTERS:
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

    def _button_edit(self, frame: DisplayRecordFrame, tab: TabType):
        if self.edit_window:
            self.edit_window.focus()
            return

        # TODO: temporary restrict edit button to filter only
        if tab != TabType.FILTERS:
            return

        self.edit_window = EditView(
            self.root,
            frame.record,
            tab,
            partial(self._on_edit_return, index=frame.index, tab=tab),
        )
        self.edit_window.focus()

    def _button_delete(self, frame: DisplayRecordFrame, tab: TabType):
        if not self.edit_window:
            self.controller.delete_record(frame.index, tab)

    def _button_move(self, frame: DisplayRecordFrame, direction: int):
        if not self.edit_window:
            self.controller.move_filter(frame.index, direction)

    def _on_edit_return(self, save: dict, index: int, tab: TabType):
        self.edit_window = None
        if save:
            self.controller.update_record(save, index, tab)


if __name__ == "__main__":
    window = View()
    window.start()
