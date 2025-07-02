import logging
import tkinter as tk
from tkinter import ttk
from typing import Callable

from utils import ViewData, bool_to_str, str_to_bool

from .edit_view import BaseEditView

logger = logging.getLogger(__name__)


class CharacterEditView(BaseEditView):
    def __init__(
        self,
        root: tk.Tk,
        view_data: ViewData,
        key_list: dict,
        return_callback: Callable,
        is_new: bool = False,
    ):
        self.keys = [""] + list(key_list.keys())
        self.key_list = {"": None, **key_list}
        self.input_var2 = (tk.StringVar(), tk.BooleanVar())
        super().__init__(root, view_data, return_callback, is_new)

    def _build_form(self, frame: ttk.Frame, view_data: ViewData, row: int):
        input_var1 = self.input_var1
        list_var = self.input_var2[0]
        check_var = self.input_var2[1]

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

        entry1 = ttk.Combobox(
            form_frame, values=self.keys, textvariable=input_var1, state=tk.DISABLED
        )
        entry1.grid(row=0, column=1, sticky=tk.NE)
        input_var1.trace_add("write", self._on_var1_change)
        self.char_combobox = entry1

        entry2_grid_info = dict(row=0, column=3, sticky=tk.NSEW)
        entry2_frame1 = ttk.Frame(form_frame)
        entry2_frame2 = ttk.Frame(form_frame)
        entry2_frame1.grid(**entry2_grid_info)
        entry2_frame2.grid(**entry2_grid_info)
        entry2_frame1.grid_remove()
        entry2_frame2.grid_remove()

        scrollbar = tk.Scrollbar(entry2_frame1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox = tk.Listbox(
            entry2_frame1,
            listvariable=list_var,
            selectmode=tk.MULTIPLE,
            state=tk.DISABLED,
            yscrollcommand=scrollbar,
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.char_listbox = listbox

        checkbuttom = ttk.Checkbutton(
            entry2_frame2, variable=check_var, state=tk.DISABLED
        )
        checkbuttom.pack(side=tk.LEFT)

        self._build_form_buttons(frame, row)

        self.char_form_frames = (entry2_frame1, entry2_frame2)
        self.toggle_widgets = (entry1, listbox, checkbuttom) + self.toggle_widgets

    def _form_variable_set(self, values: tuple[str, str]):
        self.input_var1.set(values[0])
        option_list = self.key_list[values[0]]
        if option_list == "bool":
            variable = str_to_bool(values[1])
            self.input_var2[1].set(variable)
        else:
            selected = values[1].split()
            for item in selected:
                self.char_listbox.select_set(option_list.index(item))

    def _on_treeview_add(self):
        super()._on_treeview_add()
        self.input_var2[0].set("")
        self.input_var2[1].set(False)
        existed_keys = set(item[0] for item in self.record_body.treeview_get_all())
        avaliable_keys = [key for key in self.keys if key not in existed_keys]
        self.char_combobox.config(values=avaliable_keys)

    def _on_treeview_edit(self):
        super()._on_treeview_edit()
        self.char_combobox.config(state=tk.DISABLED)

    def _on_var1_change(self, var, index, mode):
        input_var1 = self.input_var1.get()
        option_list = self.key_list[input_var1]
        if option_list == "bool":
            self.char_form_frames[0].grid_remove()
            self.char_form_frames[1].grid()
        elif isinstance(option_list, list):
            self.input_var2[0].set(option_list)
            self.char_form_frames[0].grid()
            self.char_form_frames[1].grid_remove()
        else:
            self.char_form_frames[0].grid_remove()
            self.char_form_frames[1].grid_remove()

    def _get_form_variables(self):
        input_var1 = self.input_var1.get()
        option_list = self.key_list[input_var1]
        if option_list == "bool":
            input_var2 = bool_to_str(self.input_var2[1].get())
        else:
            selected = self.char_listbox.curselection()
            input_var2 = [option_list[i] for i in selected]
        return (input_var1, input_var2)

    def _on_form_ending(self):
        super()._on_form_ending()
        self.input_var2[0].set("")
        self.input_var2[1].set(False)
