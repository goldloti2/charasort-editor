import logging
import tkinter as tk
from abc import ABC, abstractmethod
from functools import partial
from tkinter import messagebox, ttk
from typing import Callable

from utils.utils import InputData, ViewData

from .display import RecordBody

logger = logging.getLogger(__name__)


class BaseEditView(ABC):
    def __init__(
        self,
        root: tk.Tk,
        view_data: ViewData,
        return_callback: Callable,
        title: str,
    ):
        self.return_callback = return_callback

        self.window = window = tk.Toplevel(root)
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
        frame.rowconfigure([form_row - 1, form_row, form_row + 1], pad=5)
        self.status_text = tk.StringVar()
        self.input_var1 = tk.StringVar()
        self.editing_item: tuple[str] = ()
        self.toggle_widgets: tuple[ttk.Widget] = ()
        self.toggle_buttons: tuple[ttk.Button] = ()
        self._build_option_buttons(frame, form_row - 2)
        ttk.Label(frame, textvariable=self.status_text, justify=tk.CENTER).grid(
            row=form_row - 1, column=0, columnspan=2, sticky=tk.EW
        )
        self._build_form(frame, view_data, form_row)

        # add information
        record_body = RecordBody(view_data, frame, True)
        record_body.add_treeview_callbacks(
            partial(self._treeview_toggle, True),
            partial(self._treeview_toggle, False),
        )
        self.record_body = record_body
        logger.info(
            f"open edit window, '{view_data.name[2]}', {self.__class__.__name__}"
        )

    def focus(self):
        self.window.focus()

    def destroy(self):
        self.window.destroy()

    def validation_failed(self, err_msg: str):
        messagebox.showwarning("validation failed", err_msg)
        self.focus()

    @abstractmethod
    def _build_form(self, frame: ttk.Frame, view_data: ViewData, row: int):
        raise NotImplementedError(
            f"{self.__class__.__name__} not implement '_build_form'"
        )

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

    def _build_form_buttons(self, frame: ttk.Frame, row: int):
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=row, column=2, rowspan=2, sticky=tk.N)
        button_form_done = ttk.Button(
            button_frame,
            text="done",
            command=self._on_form_done,
            state=tk.DISABLED,
        )
        button_form_done.pack(fill=tk.X, expand=1)
        button_form_cancel = ttk.Button(
            button_frame,
            text="cancel",
            command=self._on_form_ending,
            state=tk.DISABLED,
        )
        button_form_cancel.pack(fill=tk.X, expand=1)

        self.toggle_widgets = (
            button_form_done,
            button_form_cancel,
        )

    def _form_toggle(self, enable: bool):
        if enable:
            for widget in self.toggle_widgets:
                widget.config(state=tk.NORMAL)
        else:
            for widget in self.toggle_widgets:
                widget.config(state=tk.DISABLED)

    @abstractmethod
    def _form_variable_set(self, values: tuple[str, str]):
        raise NotImplementedError(
            f"{self.__class__.__name__} not implement '_form_variable_set'"
        )

    def _treeview_toggle(self, enable: bool):
        if enable:
            for button in self.toggle_buttons:
                button.config(state=tk.NORMAL)
        else:
            for button in self.toggle_buttons:
                button.config(state=tk.DISABLED)

    def _on_window_save(self):
        input_data = self.record_body.get_input_data()
        self._on_window_close(input_data)

    def _on_window_close(self, save: InputData = None):
        self.return_callback(save)

    # extended by children class
    def _on_treeview_add(self):
        self.editing_item = ()
        self._form_toggle(True)
        self.status_text.set("adding...")
        self.input_var1.set("")

    # extended by CharacterEditView
    def _on_treeview_edit(self):
        item = self.record_body.treeview_selected()
        if item:
            self.editing_item = item[0]
            values = item[1]
            self.status_text.set("editing...")
            self._form_toggle(True)
            self._form_variable_set(values)

    def _on_treeview_delete(self):
        if self.record_body.treeview_delete():
            self._on_form_ending()
            self.status_text.set("deleted!")
            self._treeview_toggle(False)

    def _on_treeview_move(self, direction: int):
        if self.record_body.treeview_move(direction):
            self._on_form_ending()
            self.status_text.set("moved!")

    @abstractmethod
    def _get_form_variables(self) -> tuple:
        raise NotImplementedError(
            f"{self.__class__.__name__} not implement '_get_form_variables'"
        )

    def _on_form_done(self):
        values = self._get_form_variables()
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

    # extended by children class
    def _on_form_ending(self):
        self._form_toggle(False)
        self.status_text.set("")
        self.input_var1.set("")
