import logging
import tkinter as tk
from tkinter import ttk
from typing import Callable

from utils.utils import ViewData

from .edit_view import BaseEditView

logger = logging.getLogger(__name__)


class FilterEditView(BaseEditView):
    def __init__(
        self,
        root: tk.Tk,
        view_data: ViewData,
        key_list: dict,
        return_callback: Callable,
        is_new: bool = False,
    ):
        self.input_var2 = tk.StringVar()
        super().__init__(root, view_data, return_callback, is_new)

    def _build_form(self, frame: ttk.Frame, view_data: ViewData, row: int):
        input_var1 = self.input_var1
        input_var2 = self.input_var2
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

        self._build_form_buttons(frame, row)

        self.toggle_widgets = (entry1, entry2) + self.toggle_widgets

    def _form_variable_set(self, values: tuple[str, str]):
        self.input_var1.set(values[0])
        self.input_var2.set(values[1])

    def _on_treeview_add(self):
        super()._on_treeview_add()
        self.input_var2.set("")

    def _get_form_variables(self):
        return (self.input_var1.get(), self.input_var2.get())

    def _on_form_ending(self):
        super()._on_form_ending()
        self.input_var2.set("")
