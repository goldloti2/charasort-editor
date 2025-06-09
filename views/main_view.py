import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
from typing import TYPE_CHECKING

from .display_record import DisplayRecord
from .widgets import VerticalScrolledFrame

if TYPE_CHECKING:
    from control import Controller


class View:
    def __init__(self, controller: "Controller"):
        root = tk.Tk()
        root.title("charasort editor")
        root.geometry("600x800")
        root.resizable(False, False)

        menubar = tk.Menu(root)
        menubar.add_command(label="Open", command=self._menu_open)
        menubar.add_command(label="Save", command=self._menu_save)
        menubar.add_command(label="Save To", command=self._menu_save_to)
        root.config(menu=menubar)

        tabcontrol = ttk.Notebook()
        flt_tab_base = VerticalScrolledFrame(tabcontrol)
        chr_tab_base = VerticalScrolledFrame(tabcontrol)
        tabcontrol.add(flt_tab_base, text="Filters")
        tabcontrol.add(chr_tab_base, text="Characters")
        tabcontrol.pack(expand=1, fill=tk.BOTH)

        detail_label_style = ttk.Style()
        detail_label_style.configure(
            "detail_label.TLabel",
            background="white",
            border=1,
            padding=1,
            relief=tk.SOLID,
            wraplength=150,
        )

        self.root = root
        self.flt_tab = flt_tab_base.interior
        self.chr_tab = chr_tab_base.interior
        self.detail_label_style = detail_label_style
        self.controller = controller
        self.edit_window = None

    def start(self):
        self.root.mainloop()

    def refresh_tabs(self, node_list: list, tab: str):
        self.destroy_tabs(tab)
        frame = self._display_frame(node_list[0], tab)
        if tab == "filters":
            frame.children["!frame"].children["!button3"].config(state=tk.DISABLED)
        for node in node_list[1:-1]:
            self._display_frame(node, tab)
        if len(node_list) > 1:
            frame = self._display_frame(node_list[-1], tab)
        if tab == "filters":
            frame.children["!frame"].children["!button4"].config(state=tk.DISABLED)

    def destroy_tabs(self, tab: str):
        if tab == "filters":
            destroy = self.flt_tab.winfo_children()
        elif tab == "characters":
            destroy = self.chr_tab.winfo_children()
        else:
            raise ValueError(f"tab '{tab}' not found in view.destroy_tabs")
        if not destroy:
            return
        for frame in destroy:
            frame.destroy()

    def _display_frame(self, record: dict, tab: str) -> ttk.Frame:
        # create base frame
        if tab == "filters":
            frame = ttk.Frame(self.flt_tab, relief=tk.GROOVE, border=10)
        elif tab == "characters":
            frame = ttk.Frame(self.chr_tab, relief=tk.GROOVE, border=10)
        frame.columnconfigure(1, weight=1)
        frame.grid(column=0, sticky=tk.EW)

        # add information
        DisplayRecord(record, frame, False)

        # add buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=0, column=2, rowspan=4, sticky=tk.NW)
        button_edit = ttk.Button(
            button_frame, text="edit", command=lambda: self._button_edit(frame, tab)
        )
        button_edit.pack(fill=tk.X)
        button_delete = ttk.Button(
            button_frame,
            text="delete",
            command=lambda: self._button_delete(frame, tab),
        )
        button_delete.pack(fill=tk.X)
        if tab == "filters":
            button_up = ttk.Button(
                button_frame, text="↑", command=lambda: self._button_move(frame, -1)
            )
            button_up.pack(fill=tk.X)
            button_down = ttk.Button(
                button_frame, text="↓", command=lambda: self._button_move(frame, 1)
            )
            button_down.pack(fill=tk.X)
        return frame

    def _menu_open(self):
        path = filedialog.askopenfilename(
            initialdir=".", filetypes=[("JavaScript (*.js)", "*.js"), ("all (*)", "*")]
        )
        if path:
            self.destroy_tabs("filters")
            self.destroy_tabs("characters")
            self.controller.open_file(path)

    def _menu_save(self):
        result = messagebox.askyesno(
            "Overwrite", "Do you want to overwrite the old file?"
        )
        if result:
            self.controller.save_file()

    def _menu_save_to(self):
        path = filedialog.asksaveasfilename(
            initialdir=".",
            initialfile=f"{datetime.now().strftime('%Y-%m-%d')}.js",
            defaultextension=".js",
            filetypes=[("JavaScript (*.js)", "*.js"), ("all (*)", "*")],
        )
        if path:
            self.controller.save_file(path)

    def _button_edit(self, frame: ttk.Frame, tab: str):
        if self.edit_window:
            self.edit_window.focus()
            return

        record = self.controller.get(frame.grid_info()["row"], tab)

        self.edit_window = edit_window = tk.Toplevel(self.root)
        edit_window.title(f"'{record[0][2]}' editing...")
        edit_window.geometry("600x420")
        edit_window.resizable(False, True)
        edit_window.protocol("WM_DELETE_WINDOW", self._edit_window_close)
        edit_window.focus()

        frame = ttk.Frame(edit_window, relief=tk.GROOVE, border=10)
        frame.columnconfigure(0, pad=10)
        frame.columnconfigure(1, weight=1, pad=10)
        frame.columnconfigure(2, pad=10)
        frame.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)

        # add information
        display_record = DisplayRecord(record, frame, True)
        return_variables = display_record.return_variables
        tree = return_variables["tree"]

        # add buttons
        button_save = ttk.Button(
            frame, text="save", command=lambda: self._edit_window_save(return_variables)
        )
        button_save.grid(row=0, column=2)
        button_cancel = ttk.Button(
            frame, text="cancel", command=self._edit_window_close
        )
        button_cancel.grid(row=1, column=2)

        frame_edit = ttk.Frame(frame)
        frame_edit.grid(row=4, column=2, sticky=tk.N)
        button_option_add = ttk.Button(
            frame_edit, text="add option", command=lambda: self._edit_treeview_add(tree)
        )
        button_option_add.pack(fill=tk.X)
        button_option_edit = ttk.Button(
            frame_edit,
            text="edit option",
            command=lambda: self._edit_treeview_edit(tree),
            state=tk.DISABLED,
        )
        button_option_edit.pack(fill=tk.X)
        button_option_delete = ttk.Button(
            frame_edit,
            text="delete option",
            command=lambda: self._edit_treeview_delete(tree),
            state=tk.DISABLED,
        )
        button_option_delete.pack(fill=tk.X)
        button_option_up = ttk.Button(
            frame_edit,
            text="↑",
            command=lambda: self._edit_treeview_move_up(tree),
            state=tk.DISABLED,
        )
        button_option_up.pack(fill=tk.X)
        button_option_down = ttk.Button(
            frame_edit,
            text="↓",
            command=lambda: self._edit_treeview_move_down(tree),
            state=tk.DISABLED,
        )
        button_option_down.pack(fill=tk.X)
        display_record.add_toggle_button(
            (
                button_option_edit,
                button_option_delete,
                button_option_up,
                button_option_down,
            )
        )

    def _button_delete(self, frame: ttk.Frame, tab: str):
        self.controller.delete_record(frame.grid_info()["row"], tab)

    def _button_move(self, frame: ttk.Frame, direction: int):
        self.controller.move_filter(frame.grid_info()["row"], direction)

    def _edit_window_save(self, variable: dict):
        for key in variable:
            if key == "tree":
                tree = variable[key]
                for item in tree.get_children():
                    print(tree.item(item, "values"))
            else:
                print(key, variable[key].get())
        self._edit_window_close()

    def _edit_window_close(self):
        self.edit_window.destroy()
        self.edit_window = None

    def _edit_treeview_add(self, tree: ttk.Treeview):
        tree.insert("", "end", values=("aaa", "bbb"))

    def _edit_treeview_edit(self, tree: ttk.Treeview):
        item = tree.selection()
        if item:
            print(tree.item(item, "values"))

    def _edit_treeview_delete(self, tree: ttk.Treeview):
        item = tree.selection()
        if item:
            print("delete", tree.item(item, "values"))
            tree.delete(item)
            # TODO: disable buttons
            tree.selection_remove(tree.selection())

    def _edit_treeview_move_up(self, tree: ttk.Treeview):
        item = tree.selection()
        if item:
            index = tree.index(item)
            swap = tree.prev(item)
            if swap:
                tree.move(item, "", index - 1)
                tree.move(swap, "", index)

    def _edit_treeview_move_down(self, tree: ttk.Treeview):
        item = tree.selection()
        if item:
            index = tree.index(item)
            swap = tree.next(item)
            if swap:
                tree.move(item, "", index + 1)
                tree.move(swap, "", index)


if __name__ == "__main__":
    window = View()
    window.start()
