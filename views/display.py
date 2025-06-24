import tkinter as tk
from functools import partial
from tkinter import ttk
from typing import Callable, Dict

from utils import ButtonLabel, InputData, ViewData, WidgetType


class RecordBody:
    def __init__(self, view_data: ViewData, frame: ttk.Frame, is_edit: bool):
        return_variables = {}
        row = 0
        for _, attr in view_data.model_dump().items():
            if attr is None:
                continue
            frame.rowconfigure(row, pad=5)
            c_type, label, content = attr
            if c_type is WidgetType.LABEL:
                k_label = ttk.Label(frame, text=label + ":")
                if is_edit:
                    var = tk.StringVar(value=content)
                    c_label = tk.Entry(frame, textvariable=var)
                    return_variables[label] = var
                else:
                    c_label = ttk.Label(frame, text=content, justify=tk.LEFT)
                k_label.grid(row=row, column=0)
                c_label.grid(row=row, column=1, sticky=tk.EW)
            elif c_type is WidgetType.CHECK:
                k_label = ttk.Label(frame, text=label + ":")
                var = tk.BooleanVar(value=content)
                state = tk.NORMAL if is_edit else tk.DISABLED
                c_check = ttk.Checkbutton(frame, variable=var, state=state)
                c_check.var = var
                return_variables[label] = var
                k_label.grid(row=row, column=0)
                c_check.grid(row=row, column=1, sticky=tk.W)
            elif c_type is WidgetType.SUB_FRAME:
                sub_frame = ttk.Labelframe(
                    frame, text=label, relief=tk.GROOVE, border=10
                )
                sub_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW)
                height = 11 if len(content) > 10 else len(content)
                tree = ttk.Treeview(
                    sub_frame,
                    columns=content[0],
                    height=height,
                    selectmode=tk.BROWSE,
                    show="headings",
                )
                tree.heading("#1", text=content[0][0])
                tree.column("#1", minwidth=20, width=100)
                tree.heading("#2", text=content[0][1])
                tree.column("#2", minwidth=20)
                for sub_content in content[1:]:
                    if isinstance(sub_content[1], bool):
                        insert = (sub_content[0], "✅" if sub_content[1] else "☐")
                    else:
                        insert = sub_content
                    tree.insert("", tk.END, values=insert)
                scrollbar = ttk.Scrollbar(sub_frame, command=tree.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                tree.configure(yscrollcommand=scrollbar.set)
                detail_label = ttk.Label(frame, style="detail_label.TLabel")
                tree.bind(
                    "<ButtonRelease-1>",
                    partial(self._on_treeview_select, label=detail_label),
                )
                tree.bind(
                    "<Escape>",
                    partial(self._on_treeview_deselect, label=detail_label),
                )
                tree.pack(expand=1, fill=tk.BOTH)
                self.tree = tree
            else:
                raise ValueError(f"c_type '{c_type}' not found in view._display_frame")
            row += 1
        self.return_variables = return_variables
        self.treeview_select_callback = []
        self.treeview_deselect_callback = []

    def get_input_data(self):
        input_data = InputData()
        for key in self.return_variables:
            var = self.return_variables[key].get()
            if var:
                input_data[key] = var
        tree_values = []
        for item in self.tree.get_children():
            tree_values.append(self.tree.item(item, "values"))
        if tree_values:
            input_data["tree"] = tree_values
        return input_data

    def treeview_add(self, values: tuple):
        self.tree.insert("", tk.END, values=values)

    def treeview_delete(self):
        item = self.tree.selection()
        if item:
            self.tree.delete(item)
            self.tree.selection_remove(self.tree.selection())
            return True
        return False

    def treeview_edit(self, item: tuple, values: tuple):
        pos = self.tree.index(item)
        self.tree.delete(item)
        self.tree.insert("", pos, values=values)

    def treeview_move(self, direction: int):
        item = self.tree.selection()
        if item:
            if direction > 0:
                swap = self.tree.next(item)
            else:
                swap = self.tree.prev(item)
            if swap:
                index = self.tree.index(item)
                self.tree.move(item, "", index + direction)
                self.tree.move(swap, "", index)
                return True
        return False

    def treeview_selected(self):
        item = self.tree.selection()
        if item:
            return item, self.tree.item(item, "values")
        return None

    def add_treeview_callbacks(
        self, select_callback: Callable, deselect_callback: Callable
    ):
        if select_callback:
            self.treeview_select_callback.append(select_callback)
        if deselect_callback:
            self.treeview_deselect_callback.append(deselect_callback)

    def _on_treeview_select(self, event: tk.Event, label: ttk.Label):
        select = self.tree.selection()
        if select:
            item = self.tree.item(select, "values")
            label.config(text=item[1])
            label.place(
                anchor=tk.NW,
                x=event.x + self.tree.master.winfo_x(),
                y=event.y + self.tree.master.winfo_y(),
                width=155,
            )
            for callback in self.treeview_select_callback:
                callback()

    def _on_treeview_deselect(self, event: tk.Event, label: ttk.Label):
        self.tree.selection_remove(self.tree.selection())
        label.place_forget()
        for callback in self.treeview_deselect_callback:
            callback()


class RecordFrame(ttk.Frame):
    def __init__(
        self,
        parent: ttk.Frame,
        view_data: ViewData,
        index: int,
        callbacks: Dict[ButtonLabel, Callable],
    ):
        # create base frame
        super().__init__(parent, relief=tk.GROOVE, border=10)
        self.columnconfigure(1, weight=1)
        self.grid(column=0, sticky=tk.EW)
        self.view_data = view_data
        self.index = index

        # add information
        RecordBody(view_data, self, False)

        # add buttons
        self.button_up = None
        self.button_down = None
        button_frame = ttk.Frame(self)
        button_frame.grid(row=0, column=2, rowspan=4, sticky=tk.NW)
        for label, callback in callbacks.items():
            button = ttk.Button(
                button_frame, text=label.value, command=partial(callback, frame=self)
            )
            button.pack(fill=tk.X)
            if label is ButtonLabel.MOVEUP:
                self.button_up = button
            elif label is ButtonLabel.MOVEDOWN:
                self.button_down = button

    def disable_move(self, is_first: bool, is_last: bool):
        if self.button_up and is_first:
            self.button_up.config(state=tk.DISABLED)
        if self.button_down and is_last:
            self.button_down.config(state=tk.DISABLED)
