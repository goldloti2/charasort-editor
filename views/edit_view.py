import tkinter as tk
from tkinter import ttk
from typing import Callable

from .display_record import DisplayRecord


class EditView:
    def __init__(self, root: tk.Tk, record: list, return_callback: Callable):
        self.return_callback = return_callback

        self.window = window = tk.Toplevel(root)
        window.title(f"'{record[0][2]}' editing...")
        window.geometry("600x500")
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

        # add input form
        form_header = tk.StringVar()
        imput_var1 = tk.StringVar()
        imput_var2 = tk.StringVar()

        frame.rowconfigure([5, 6, 7], pad=5)
        ttk.Label(frame, textvariable=form_header, justify=tk.CENTER).grid(
            row=5, column=0, columnspan=2, sticky=tk.EW
        )
        ttk.Label(frame, text="name" + ":", justify=tk.CENTER).grid(row=6, column=0)
        ttk.Label(frame, text="key" + ":", justify=tk.CENTER).grid(row=7, column=0)
        entry1 = ttk.Entry(frame, textvariable=imput_var1, state=tk.DISABLED)
        entry1.grid(row=6, column=1, sticky=tk.EW)
        entry2 = ttk.Entry(frame, textvariable=imput_var2, state=tk.DISABLED)
        entry2.grid(row=7, column=1, sticky=tk.EW)
        button_form_done = ttk.Button(
            frame,
            text="done",
            command=self._form_done,
            state=tk.DISABLED,
        )
        button_form_done.grid(row=6, column=2)
        button_form_cancel = ttk.Button(
            frame,
            text="cancel",
            command=self._form_ending,
            state=tk.DISABLED,
        )
        button_form_cancel.grid(row=7, column=2)

        self.form_header = form_header
        self.imput_var1 = imput_var1
        self.imput_var2 = imput_var2
        self.toggle_form_widgets = (
            entry1,
            entry2,
            button_form_done,
            button_form_cancel,
        )
        self.edit_item = None

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
        self.form_header.set("adding...")
        self.imput_var1.set("")
        self.imput_var2.set("")
        self.edit_item = None
        self._toggle_form(True)

    def _treeview_edit(self):
        item = self.tree.selection()
        if item:
            self.form_header.set("editing...")
            value = self.tree.item(item, "values")
            self.imput_var1.set(value[0])
            self.imput_var2.set(value[1])
            self.edit_item = item
            self._toggle_form(True)

    def _treeview_delete(self):
        item = self.tree.selection()
        if item:
            self.form_header.set("deleted!")
            self._toggle_form(False)
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
                self.form_header.set("moved!")
                self._toggle_form(False)
                self.tree.move(item, "", index + direction)
                self.tree.move(swap, "", index)

    def _form_done(self):
        value = (self.imput_var1.get(), self.imput_var2.get())
        pos = "end"
        if self.edit_item:
            pos = self.tree.index(self.edit_item)
            self.tree.delete(self.edit_item)
        self.tree.insert("", pos, values=value)
        self.edit_item = None
        self._form_ending()

    def _form_ending(self):
        self.imput_var1.set("")
        self.imput_var2.set("")
        self.form_header.set("")
        self._toggle_form(False)

    def _toggle_form(self, toggle: bool):
        if toggle:
            for widget in self.toggle_form_widgets:
                widget.config(state=tk.NORMAL)
        else:
            for widget in self.toggle_form_widgets:
                widget.config(state=tk.DISABLED)
