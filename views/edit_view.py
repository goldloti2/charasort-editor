import tkinter as tk
from tkinter import ttk
from typing import Callable

from .display import DisplayRecord


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
        input_var1 = tk.StringVar()
        input_var2 = tk.StringVar()

        frame.rowconfigure([5, 6, 7], pad=5)
        ttk.Label(frame, textvariable=form_header, justify=tk.CENTER).grid(
            row=5, column=0, columnspan=2, sticky=tk.EW
        )
        ttk.Label(frame, text="name" + ":", justify=tk.CENTER).grid(row=6, column=0)
        ttk.Label(frame, text="key" + ":", justify=tk.CENTER).grid(row=7, column=0)
        entry1 = ttk.Entry(frame, textvariable=input_var1, state=tk.DISABLED)
        entry1.grid(row=6, column=1, sticky=tk.EW)
        entry2 = ttk.Entry(frame, textvariable=input_var2, state=tk.DISABLED)
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
        self.input_var1 = input_var1
        self.input_var2 = input_var2
        self.toggle_form_widgets = (
            entry1,
            entry2,
            button_form_done,
            button_form_cancel,
        )
        self.edit_item = None

        # add information
        record_displayer = DisplayRecord(record, frame, True)
        record_displayer.add_toggle_button(self.toggle_button)
        self.record_displayer = record_displayer

    def focus(self):
        self.window.focus()

    def destroy(self):
        self._window_close()

    def _window_save(self):
        save = self.record_displayer.get_values()
        self._window_close(save)

    def _window_close(self, save: dict = None):
        self.window.destroy()
        self.return_callback(save)

    def _treeview_add(self):
        self.form_header.set("adding...")
        self.input_var1.set("")
        self.input_var2.set("")
        self.edit_item = None
        self._form_toggle(True)

    def _treeview_edit(self):
        item = self.record_displayer.tree_selected()
        if item:
            self.edit_item = item[0]
            values = item[1]
            self.form_header.set("editing...")
            self.input_var1.set(values[0])
            self.input_var2.set(values[1])
            self._form_toggle(True)

    def _treeview_delete(self):
        if self.record_displayer.tree_delete():
            self._form_ending()
            self.form_header.set("deleted!")
            for button in self.toggle_button:
                button.config(state=tk.DISABLED)

    def _treeview_move(self, direction: int):
        if self.record_displayer.tree_move(direction):
            self._form_ending()
            self.form_header.set("moved!")

    def _form_done(self):
        values = (self.input_var1.get(), self.input_var2.get())
        if self.edit_item:
            self.record_displayer.tree_edit(values, self.edit_item)
        else:
            self.record_displayer.tree_add(values)
        self.edit_item = None
        self._form_ending()

    def _form_ending(self):
        self.input_var1.set("")
        self.input_var2.set("")
        self.form_header.set("")
        self._form_toggle(False)

    def _form_toggle(self, toggle: bool):
        if toggle:
            for widget in self.toggle_form_widgets:
                widget.config(state=tk.NORMAL)
        else:
            for widget in self.toggle_form_widgets:
                widget.config(state=tk.DISABLED)
