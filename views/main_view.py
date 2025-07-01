import logging
import tkinter as tk
from datetime import datetime
from functools import partial
from tkinter import filedialog, messagebox, ttk
from typing import TYPE_CHECKING, Callable, Dict

from utils import ButtonLabel, InputData, TabType, ViewData

from .character_edit import CharacterEditView
from .display import RecordFrame
from .filter_edit import FilterEditView
from .widgets import VerticalScrolledFrame

if TYPE_CHECKING:
    from control import Controller


logger = logging.getLogger(__name__)


class View:
    def __init__(self, controller: "Controller"):
        self.controller = controller
        self.root = root = tk.Tk()
        root.title("charasort editor")
        root.geometry("600x800")
        root.resizable(False, False)

        menu = self._build_menu()
        root.config(menu=menu)

        tab_control = ttk.Notebook()
        filters_base, filters_inter = self._build_tab(tab_control, TabType.FILTERS)
        characters_base, characters_inter = self._build_tab(
            tab_control, TabType.CHARACTERS
        )
        tab_control.add(filters_base, text="Filters")
        tab_control.add(characters_base, text="Characters")
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

        self.tabs = {
            TabType.FILTERS: filters_inter,
            TabType.CHARACTERS: characters_inter,
        }
        self.detail_label_style = detail_label_style
        self.edit_window = None
        self.is_running = False
        logger.info("initialized")

    def start(self):
        self.is_running = True
        self.root.mainloop()

    def refresh_tabs(self, view_list: list[ViewData], tab: TabType):
        self.destroy_tabs(tab)

        parent = self.tabs[tab]
        callbacks = self._create_button_callbacks(tab)
        is_filter_tab = tab is TabType.FILTERS
        last_index = len(view_list) - 1

        for idx, view_data in enumerate(view_list):
            is_first = (idx == 0) and is_filter_tab
            is_last = (idx == last_index) and is_filter_tab
            try:
                self._build_display_frame(
                    parent, view_data, idx, callbacks, is_first, is_last
                )
            except (TypeError, IndexError, KeyError, ValueError, AttributeError) as e:
                logger.error(e)
                logger.debug("", exc_info=e)
                self.show_error(f"Error occured when trying to show {tab.value} #{idx}")
            else:
                logger.debug(
                    f"new record frame, {tab.value} #{idx}, {view_data.name[2]}"
                )

    def destroy_tabs(self, tab: TabType):
        destroy = self.tabs[tab].winfo_children()
        if not destroy:
            return
        for frame in destroy:
            frame.destroy()

    def show_error(self, message: str):
        messagebox.showerror("Error", message)

    def _build_menu(self):
        menu = tk.Menu(self.root)
        menu_specs = [
            ("Open", self._on_menu_open),
            ("Save", self._on_menu_save),
            ("Save To", self._on_menu_save_to),
        ]
        for label, command in menu_specs:
            menu.add_command(label=label, command=command)
        return menu

    def _build_tab(self, parent: ttk.Notebook, tab: TabType):
        tab_base = ttk.Frame(parent)
        scrolled_frame = VerticalScrolledFrame(tab_base)
        scrolled_frame.pack(fill=tk.BOTH, expand=1)
        button_frame = ttk.Frame(tab_base, relief=tk.RIDGE, border=5)
        button_frame.pack(fill=tk.X)
        new_button = ttk.Button(
            button_frame,
            text="Add New Data",
            command=partial(self._on_button_add, tab=tab),
        )
        new_button.pack(fill=tk.X, padx=15, pady=5, ipady=5)
        return tab_base, scrolled_frame.interior

    def _build_display_frame(
        self,
        parent: ttk.Frame,
        view_data: ViewData,
        index: int,
        callbacks: Dict[ButtonLabel, Callable],
        is_first: bool,
        is_last: bool,
    ):
        frame = RecordFrame(parent, view_data, index, callbacks)
        frame.disable_move(is_first, is_last)

    def _create_button_callbacks(self, tab: TabType):
        callbacks = {
            ButtonLabel.EDIT: partial(self._on_button_edit, tab=tab),
            ButtonLabel.DELETE: partial(self._on_button_delete, tab=tab),
        }
        if tab is TabType.FILTERS:
            callbacks[ButtonLabel.MOVEUP] = partial(self._on_button_move, direction=-1)
            callbacks[ButtonLabel.MOVEDOWN] = partial(self._on_button_move, direction=1)
        return callbacks

    def _on_menu_open(self):
        path = filedialog.askopenfilename(
            initialdir=".", filetypes=[("JavaScript (*.js)", "*.js"), ("all (*)", "*")]
        )
        if path:
            self.destroy_tabs(TabType.FILTERS)
            self.destroy_tabs(TabType.CHARACTERS)
            self.controller.open_file(path)

    def _on_menu_save(self):
        result = messagebox.askyesno(
            "Overwrite", "Do you want to overwrite the old file?"
        )
        if result:
            self.controller.save_file()

    def _on_menu_save_to(self):
        path = filedialog.asksaveasfilename(
            initialdir=".",
            initialfile=f"{datetime.now().strftime('%Y-%m-%d')}.js",
            defaultextension=".js",
            filetypes=[("JavaScript (*.js)", "*.js"), ("all (*)", "*")],
        )
        if path:
            self.controller.save_file(path)

    def _on_button_add(self, tab: TabType):
        if self.edit_window:
            self.edit_window.focus()
            return

        view_data = self.controller.get_empty_record(tab)

        if tab == TabType.FILTERS:
            self.edit_window = FilterEditView(
                self.root,
                view_data,
                partial(self._on_add_return, tab=tab),
                True,
            )
        elif tab == TabType.CHARACTERS:
            key_list = self.controller.get_filter_keys()
            self.edit_window = CharacterEditView(
                self.root,
                view_data,
                key_list,
                partial(self._on_add_return, tab=tab),
                True,
            )
        else:
            return
        self.edit_window.focus()

    def _on_button_edit(self, frame: RecordFrame, tab: TabType):
        if self.edit_window:
            self.edit_window.focus()
            return

        if tab == TabType.FILTERS:
            self.edit_window = FilterEditView(
                self.root,
                frame.view_data,
                partial(self._on_edit_return, index=frame.index, tab=tab),
                False,
            )
        elif tab == TabType.CHARACTERS:
            key_list = self.controller.get_filter_keys()
            self.edit_window = CharacterEditView(
                self.root,
                frame.view_data,
                key_list,
                partial(self._on_edit_return, index=frame.index, tab=tab),
                False,
            )
        else:
            return
        self.edit_window.focus()

    def _on_button_delete(self, frame: RecordFrame, tab: TabType):
        if not self.edit_window:
            self.controller.delete_record(frame.index, tab)

    def _on_button_move(self, frame: RecordFrame, direction: int):
        if not self.edit_window:
            self.controller.move_filter(frame.index, direction)

    def _on_add_return(self, save: InputData, tab: TabType):
        if save is not None:
            try:
                self.controller.add_record(save, tab)
            except ValueError as e:
                err_msg = "\n".join([f"{i['loc']}: {i['msg']}" for i in e.errors()])
                self.edit_window.validation_failed(err_msg)
                return
        self.edit_window.destroy()
        self.edit_window = None

    def _on_edit_return(self, save: InputData, index: int, tab: TabType):
        if save is not None:
            try:
                self.controller.update_record(save, index, tab)
            except ValueError as e:
                err_msg = "\n".join([f"{i['loc']}: {i['msg']}" for i in e.errors()])
                self.edit_window.validation_failed(err_msg)
                return
        self.edit_window.destroy()
        self.edit_window = None


if __name__ == "__main__":
    window = View()
    window.start()
