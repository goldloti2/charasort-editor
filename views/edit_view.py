import logging
import tkinter as tk
from functools import partial
from tkinter import messagebox, ttk
from typing import Callable

from utils import InputData, TabType, ViewData

from .display import RecordBody

logger = logging.getLogger(__name__)


class EditView:
    def __init__(
        self,
        root: tk.Tk,
        view_data: ViewData,
        key_list: dict,
        tab: TabType,
        return_callback: Callable,
        is_new: bool = False,
    ):
        self.return_callback = return_callback

        self.window = window = tk.Toplevel(root)
        if is_new:
            title = "adding new data..."
        else:
            title = f"'{view_data.name[2]}' editing..."
        window.title(title)
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

        # add input form
        form_row = sum(1 for v in view_data.model_dump().values() if v is not None) + 1
        self.status_text = tk.StringVar()
        self.input_var1 = None
        self.input_var2 = None
        self.toggle_form_widgets = ()
        self.editing_item = ()
        self.toggle_buttons = ()
        self._build_option_buttons(frame, form_row - 2)
        frame.rowconfigure([form_row - 1, form_row, form_row + 1], pad=5)
        ttk.Label(frame, textvariable=self.status_text, justify=tk.CENTER).grid(
            row=form_row - 1, column=0, columnspan=2, sticky=tk.EW
        )
        if tab == TabType.FILTERS:
            self._build_filter_form(frame, view_data, form_row)
        elif tab == TabType.CHARACTERS:
            self._build_character_form(frame, view_data, form_row)

        # add information
        record_body = RecordBody(view_data, frame, True)
        record_body.add_treeview_callbacks(
            partial(self._treeview_toggle, True),
            partial(self._treeview_toggle, False),
        )
        self.record_body = record_body
        logger.info(f"open edit window, '{view_data.name[2]}'")

    def focus(self):
        self.window.focus()

    def destroy(self):
        self.window.destroy()

    def validation_failed(self, err_msg: str):
        messagebox.showwarning("validation failed", err_msg)
        self.focus()

    def _on_window_save(self):
        input_data = self.record_body.get_input_data()
        self._on_window_close(input_data)

    def _on_window_close(self, save: InputData = None):
        self.return_callback(save)

    def _on_treeview_add(self):
        self.status_text.set("adding...")
        self.input_var1.set("")
        self.input_var2.set("")
        self.editing_item = ()
        self._form_toggle(True)

    def _on_treeview_edit(self):
        item = self.record_body.treeview_selected()
        if item:
            self.editing_item = item[0]
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

    def _build_character_form(self, frame: ttk.Frame, view_data: ViewData, row: int):
        input_var1 = tk.StringVar()
        input_var2 = tk.StringVar()

        form_frame = ttk.Frame(frame)
        form_frame.columnconfigure([0, 1, 2], pad=10)
        form_frame.columnconfigure(3, weight=1, pad=10)
        form_frame.grid(row=row, column=0, rowspan=2, columnspan=2, sticky=tk.NSEW)
        ttk.Label(
            form_frame, text=view_data.opts[2][0][0] + ":", justify=tk.CENTER
        ).grid(row=0, column=0, sticky=tk.NE)
        ttk.Label(
            form_frame, text=view_data.opts[2][0][1] + ":", justify=tk.CENTER
        ).grid(row=0, column=2, sticky=tk.NE)
        entry1 = ttk.Combobox(form_frame, state=tk.DISABLED)
        entry1.grid(row=0, column=1, sticky=tk.NE)
        entry2 = tk.Listbox(form_frame, state=tk.DISABLED)
        entry2.grid(row=0, column=3, sticky=tk.NSEW)
        button_form_done = ttk.Button(
            frame,
            text="done",
            # command=self._on_form_done,
            state=tk.DISABLED,
        )
        button_form_done.grid(row=row, column=2, sticky=tk.NW)
        button_form_cancel = ttk.Button(
            frame,
            text="cancel",
            # command=self._on_form_ending,
            state=tk.DISABLED,
        )
        button_form_cancel.grid(row=row + 1, column=2, sticky=tk.NW)

        self.input_var1 = input_var1
        self.input_var2 = input_var2
        self.toggle_form_widgets = (
            entry1,
            entry2,
            button_form_done,
            button_form_cancel,
        )

    def _build_filter_form(self, frame: ttk.Frame, view_data: ViewData, row: int):
        input_var1 = tk.StringVar()
        input_var2 = tk.StringVar()
        ttk.Label(frame, text=view_data.sub[2][0][0] + ":", justify=tk.CENTER).grid(
            row=row, column=0
        )
        ttk.Label(frame, text=view_data.sub[2][0][1] + ":", justify=tk.CENTER).grid(
            row=row + 1, column=0
        )
        entry1 = ttk.Entry(frame, textvariable=input_var1, state=tk.DISABLED)
        entry1.grid(row=row, column=1, sticky=tk.EW)
        entry2 = ttk.Entry(frame, textvariable=input_var2, state=tk.DISABLED)
        entry2.grid(row=row + 1, column=1, sticky=tk.EW)
        button_form_done = ttk.Button(
            frame,
            text="done",
            command=self._on_form_done,
            state=tk.DISABLED,
        )
        button_form_done.grid(row=row, column=2)
        button_form_cancel = ttk.Button(
            frame,
            text="cancel",
            command=self._on_form_ending,
            state=tk.DISABLED,
        )
        button_form_cancel.grid(row=row + 1, column=2)

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
        if not (values[0] and values[1]):
            messagebox.showwarning("warning", "fields cannot be empty")
            self.focus()
            return
        if self.editing_item:
            self.record_body.treeview_edit(self.editing_item, values)
        else:
            self.record_body.treeview_add(values)
        self.editing_item = ()
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
