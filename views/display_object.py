import tkinter as tk
from tkinter import ttk


class DisplayObject:
    def __init__(self, object: dict, frame: ttk.Frame):
        row = 0
        for attr in object:
            frame.rowconfigure(row, pad=5)
            c_type, label, content = attr
            if c_type == "label":
                k_label = ttk.Label(frame, text=label + ":")
                c_label = ttk.Label(frame, text=content, justify=tk.LEFT)
                k_label.grid(row=row, column=0)
                c_label.grid(row=row, column=1, sticky=tk.EW)
            elif c_type == "check":
                k_label = ttk.Label(frame, text=label + ":")
                var = tk.BooleanVar(value=content)
                c_check = ttk.Checkbutton(frame, variable=var, state=tk.DISABLED)
                c_check.var = var
                k_label.grid(row=row, column=0)
                c_check.grid(row=row, column=1, sticky=tk.W)
            elif c_type == "sub_frame":
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
                    lambda event: self._treeview_select(event, detail_label),
                )
                tree.bind(
                    "<Escape>",
                    lambda event: self._treeview_deselect(event, detail_label),
                )
                tree.pack(expand=1, fill=tk.BOTH)
                self.tree = tree
            else:
                raise ValueError(f"c_type '{c_type}' not found in view._display_frame")
            row += 1

    def _treeview_select(self, event: tk.Event, label: ttk.Label):
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

    def _treeview_deselect(self, event: tk.Event, label: ttk.Label):
        self.tree.selection_remove(self.tree.selection())
        label.place_forget()
