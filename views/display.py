import tkinter as tk
from functools import partial
from tkinter import ttk

from utils import ButtonLabel, WidgetType


class DisplayRecord:
    def __init__(self, record: dict, frame: ttk.Frame, is_edit: bool):
        return_variables = {}
        row = 0
        for attr in record:
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
                    tree.insert("", "end", values=sub_content)
                scrollbar = ttk.Scrollbar(sub_frame, command=tree.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                tree.configure(yscrollcommand=scrollbar.set)
                detail_label = ttk.Label(frame, style="detail_label.TLabel")
                tree.bind(
                    "<ButtonRelease-1>",
                    partial(self._treeview_select, label=detail_label),
                )
                tree.bind(
                    "<Escape>",
                    partial(self._treeview_deselect, label=detail_label),
                )
                tree.pack(expand=1, fill=tk.BOTH)
                self._tree = tree
            else:
                raise ValueError(f"c_type '{c_type}' not found in view._display_frame")
            row += 1
        self._return_variables = return_variables
        self.toggle_button = ()

    def get_values(self):
        values = {}
        for key in self._return_variables:
            var = self._return_variables[key].get()
            if var:
                values[key] = var
        tree_values = []
        for item in self._tree.get_children():
            tree_values.append(self._tree.item(item, "values"))
        if tree_values:
            values["tree"] = tree_values
        return values

    def tree_add(self, values: tuple):
        self._tree.insert("", "end", values=values)

    def tree_delete(self):
        item = self._tree.selection()
        if item:
            self._tree.delete(item)
            self._tree.selection_remove(self._tree.selection())
            return True
        return False

    def tree_edit(self, values: tuple, item: str):
        pos = self._tree.index(item)
        self._tree.delete(item)
        self._tree.insert("", pos, values=values)

    def tree_move(self, direction: int):
        item = self._tree.selection()
        if item:
            if direction > 0:
                swap = self._tree.next(item)
            else:
                swap = self._tree.prev(item)
            if swap:
                index = self._tree.index(item)
                self._tree.move(item, "", index + direction)
                self._tree.move(swap, "", index)
                return True
        return False

    def tree_selected(self):
        item = self._tree.selection()
        if item:
            return item, self._tree.item(item, "values")
        return None

    def add_toggle_button(self, button: tuple):
        self.toggle_button = button

    def _treeview_select(self, event: tk.Event, label: ttk.Label):
        select = self._tree.selection()
        if select:
            item = self._tree.item(select, "values")
            label.config(text=item[1])
            label.place(
                anchor=tk.NW,
                x=event.x + self._tree.master.winfo_x(),
                y=event.y + self._tree.master.winfo_y(),
                width=155,
            )
            for button in self.toggle_button:
                button.config(state=tk.NORMAL)

    def _treeview_deselect(self, event: tk.Event, label: ttk.Label):
        self._tree.selection_remove(self._tree.selection())
        label.place_forget()
        for button in self.toggle_button:
            button.config(state=tk.DISABLED)


class DisplayRecordFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame, record: dict, index: int, callbacks: dict):
        # create base frame
        super().__init__(parent, relief=tk.GROOVE, border=10)
        self.columnconfigure(1, weight=1)
        self.grid(column=0, sticky=tk.EW)
        self.record = record
        self.index = index

        # add information
        DisplayRecord(record, self, False)

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
