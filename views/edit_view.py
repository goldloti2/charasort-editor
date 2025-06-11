import tkinter as tk
from tkinter import ttk
from typing import Callable

from .display_record import DisplayRecord


class EditView:
    def __init__(self, root: tk.Tk, record: list, return_callback: Callable):
        self.return_callback = return_callback

        self.window = window = tk.Toplevel(root)
        window.title(f"'{record[0][2]}' editing...")
        window.geometry("600x420")
        window.resizable(False, True)
        window.protocol("WM_DELETE_WINDOW", self._window_close)

        frame = ttk.Frame(window, relief=tk.GROOVE, border=10)
        frame.columnconfigure(0, pad=10)
        frame.columnconfigure(1, weight=1, pad=10)
        frame.columnconfigure(2, pad=10)
        frame.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)

        # add buttons
        button_save = ttk.Button(frame, text="save", command=self._window_save)
        button_save.grid(row=0, column=2)
        button_cancel = ttk.Button(frame, text="cancel", command=self._window_close)
        button_cancel.grid(row=1, column=2)

        frame_edit = ttk.Frame(frame)
        frame_edit.grid(row=4, column=2, sticky=tk.N)
        button_option_add = ttk.Button(
            frame_edit, text="add option", command=self._treeview_add
        )
        button_option_add.pack(fill=tk.X)
        button_option_edit = ttk.Button(
            frame_edit,
            text="edit option",
            command=self._treeview_edit,
            state=tk.DISABLED,
        )
        button_option_edit.pack(fill=tk.X)
        button_option_delete = ttk.Button(
            frame_edit,
            text="delete option",
            command=self._treeview_delete,
            state=tk.DISABLED,
        )
        button_option_delete.pack(fill=tk.X)
        button_option_up = ttk.Button(
            frame_edit,
            text="↑",
            command=lambda: self._treeview_move(-1),
            state=tk.DISABLED,
        )
        button_option_up.pack(fill=tk.X)
        button_option_down = ttk.Button(
            frame_edit,
            text="↓",
            command=lambda: self._treeview_move(1),
            state=tk.DISABLED,
        )
        button_option_down.pack(fill=tk.X)
        self.toggle_button = (
            button_option_edit,
            button_option_delete,
            button_option_up,
            button_option_down,
        )

        # add information
        record_displayer = DisplayRecord(record, frame, True)
        self.return_variables = record_displayer.return_variables
        self.tree = record_displayer.tree
        record_displayer.add_toggle_button(self.toggle_button)

    def focus(self):
        self.window.focus()

    def destroy(self):
        self._window_close()

    def _window_save(self):
        save = {}
        for key in self.return_variables:
            save[key] = self.return_variables[key].get()
        tree_values = []
        for item in self.tree.get_children():
            tree_values.append(self.tree.item(item, "values"))
        save["tree"] = tree_values
        self._window_close(save)

    def _window_close(self, save: dict = None):
        self.window.destroy()
        self.return_callback(save)

    def _treeview_add(self):
        self.tree.insert("", "end", values=("aaa", "bbb"))

    def _treeview_edit(self):
        item = self.tree.selection()
        if item:
            print(self.tree.item(item, "values"))

    def _treeview_delete(self):
        item = self.tree.selection()
        if item:
            print("delete", self.tree.item(item, "values"))
            self.tree.delete(item)
            self.tree.selection_remove(self.tree.selection())
            for button in self.toggle_button:
                button.config(state=tk.DISABLED)

    def _treeview_move(self, direction: int):
        item = self.tree.selection()
        if item:
            index = self.tree.index(item)
            if direction > 0:
                swap = self.tree.next(item)
            else:
                swap = self.tree.prev(item)
            if swap:
                self.tree.move(item, "", index + direction)
                self.tree.move(swap, "", index)
