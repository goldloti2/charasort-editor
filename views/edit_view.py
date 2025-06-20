import tkinter as tk
from functools import partial
from tkinter import ttk
from typing import Callable

from utils import InputData, TabType, ViewData

from .display import RecordBody


class EditView:
    def __init__(
        self, root: tk.Tk, view_data: ViewData, tab: TabType, return_callback: Callable
    ):
        self.return_callback = return_callback

        self.window = window = tk.Toplevel(root)
        window.title(f"'{view_data.name[2]}' editing...")
        window.geometry("600x500")
        window.resizable(False, True)
        window.protocol("WM_DELETE_WINDOW", self._on_window_close)

        frame = ttk.Frame(window, relief=tk.GROOVE, border=10)
        frame.columnconfigure(0, pad=10)
        frame.columnconfigure(1, weight=1, pad=10)
        frame.columnconfigure(2, pad=10)
        frame.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)

        # add buttons
        button_save = ttk.Button(frame, text="save", command=self._on_window_save)
        button_save.grid(row=0, column=2)
        button_cancel = ttk.Button(frame, text="cancel", command=self._on_window_close)
        button_cancel.grid(row=1, column=2)

        tree_row = 4
        self.toggle_buttons = ()
        self._build_option_buttons(frame, tree_row)

        # add input form
        frame.rowconfigure([i for i in range(tree_row + 1, tree_row + 3)], pad=5)
        self.status_text = None
        self.input_var1 = None
        self.input_var2 = None
        self.toggle_form_widgets = ()
        self.edit_item = ()
        self._build_filter_form(frame)

        # add information
        record_body = RecordBody(view_data, frame, True)
        record_body.add_treeview_callbacks(
            partial(self._treeview_toggle, True),
            partial(self._treeview_toggle, False),
        )
        self.record_body = record_body

    def focus(self):
        self.window.focus()

    def destroy(self):
        self._on_window_close()

    def _on_window_save(self):
        input_data = self.record_body.get_input_data()
        self._on_window_close(input_data)

    def _on_window_close(self, save: InputData = None):
        self.window.destroy()
        self.return_callback(save)

    def _on_treeview_add(self):
        self.status_text.set("adding...")
        self.input_var1.set("")
        self.input_var2.set("")
        self.edit_item = ()
        self._form_toggle(True)

    def _on_treeview_edit(self):
        item = self.record_body.treeview_selected()
        if item:
            self.edit_item = item[0]
            values = item[1]
            self.status_text.set("editing...")
            self.input_var1.set(values[0])
            self.input_var2.set(values[1])
            self._form_toggle(True)

    def _on_treeview_delete(self):
        if self.record_body.treeview_delete():
            self._on_form_ending()
            self.status_text.set("deleted!")
            self._treeview_toggle(False)

    def _on_treeview_move(self, direction: int):
        if self.record_body.treeview_move(direction):
            self._on_form_ending()
            self.status_text.set("moved!")

    def _treeview_toggle(self, enable: bool):
        if enable:
            for button in self.toggle_buttons:
                button.config(state=tk.NORMAL)
        else:
            for button in self.toggle_buttons:
                button.config(state=tk.DISABLED)

    def _build_filter_form(self, frame: ttk.Frame):
        status_text = tk.StringVar()
        input_var1 = tk.StringVar()
        input_var2 = tk.StringVar()

        ttk.Label(frame, textvariable=status_text, justify=tk.CENTER).grid(
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
            command=self._on_form_done,
            state=tk.DISABLED,
        )
        button_form_done.grid(row=6, column=2)
        button_form_cancel = ttk.Button(
            frame,
            text="cancel",
            command=self._on_form_ending,
            state=tk.DISABLED,
        )
        button_form_cancel.grid(row=7, column=2)

        self.status_text = status_text
        self.input_var1 = input_var1
        self.input_var2 = input_var2
        self.toggle_form_widgets = (
            entry1,
            entry2,
            button_form_done,
            button_form_cancel,
        )

    def _on_form_done(self):
        values = (self.input_var1.get(), self.input_var2.get())
        if self.edit_item:
            self.record_body.treeview_edit(self.edit_item, values)
        else:
            self.record_body.treeview_add(values)
        self.edit_item = ()
        self._on_form_ending()

    def _on_form_ending(self):
        self.input_var1.set("")
        self.input_var2.set("")
        self.status_text.set("")
        self._form_toggle(False)

    def _form_toggle(self, enable: bool):
        if enable:
            for widget in self.toggle_form_widgets:
                widget.config(state=tk.NORMAL)
        else:
            for widget in self.toggle_form_widgets:
                widget.config(state=tk.DISABLED)

    def _build_option_buttons(self, frame: ttk.Frame, start_row: int):
        frame_edit = ttk.Frame(frame)
        frame_edit.grid(row=start_row, column=2, sticky=tk.N)
        button_option_add = ttk.Button(
            frame_edit, text="add option", command=self._on_treeview_add
        )
        button_option_add.pack(fill=tk.X)
        button_option_edit = ttk.Button(
            frame_edit,
            text="edit option",
            command=self._on_treeview_edit,
            state=tk.DISABLED,
        )
        button_option_edit.pack(fill=tk.X)
        button_option_delete = ttk.Button(
            frame_edit,
            text="delete option",
            command=self._on_treeview_delete,
            state=tk.DISABLED,
        )
        button_option_delete.pack(fill=tk.X)
        button_option_up = ttk.Button(
            frame_edit,
            text="↑",
            command=partial(self._on_treeview_move, -1),
            state=tk.DISABLED,
        )
        button_option_up.pack(fill=tk.X)
        button_option_down = ttk.Button(
            frame_edit,
            text="↓",
            command=partial(self._on_treeview_move, 1),
            state=tk.DISABLED,
        )
        button_option_down.pack(fill=tk.X)
        self.toggle_buttons = (
            button_option_edit,
            button_option_delete,
            button_option_up,
            button_option_down,
        )
