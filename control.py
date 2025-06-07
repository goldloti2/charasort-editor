from model import Model
from view import View


class Controller:
    def __init__(self):
        window = View(self)
        self.window = window

    def start(self):
        self.open_file()
        self.window.start()

    def open_file(self, path="test.js"):
        self.path = path
        self.model = Model(path)
        self._update_tab("filters")
        self._update_tab("characters")

    def save_file(self, path=""):
        if not path:
            self.model.save_file(self.path)
        else:
            self.path = path
            self.model.save_file(path)

    def delete_object(self, index: int, tab: str):
        self.model.delete_object(index, tab)
        self._update_tab(tab)

    def move_filter(self, index: int, direction: str):
        self.model.move_filter(index, direction)
        self._update_tab("filters")

    def _update_tab(self, tab: str):
        if tab == "filters":
            new_list = [self._gen_node_filter(flt) for flt in self.model.flt_list]
        elif tab == "characters":
            new_list = [self._gen_node_character(chr) for chr in self.model.chr_list]
        else:
            raise ValueError(f"tab '{tab}' not found in controller._update_tab")
        if new_list:
            self.window.refresh_tabs(new_list, tab)
        else:
            self.window.destroy_tabs(tab)

    def _gen_node_filter(self, flt: dict):
        node = []
        node.append(("label", "name", flt["name"]))
        node.append(("label", "key", flt["key"]))
        node.append(("label", "tooltip", flt.get("tooltip", "")))
        node.append(("check", "checked", flt.get("checked", None) == "true"))
        if "sub" in flt:
            subs = [("name", "key")]
            for sub in flt["sub"]:
                subs.append((sub["name"], sub["key"]))
            node.append(("sub_frame", "sub", subs))
        return node

    def _gen_node_character(self, chr: dict):
        node = []
        node.append(("label", "name", chr["name"]))
        node.append(("label", "img", chr["img"]))
        opts = [("key", "option")]
        chr_opts = chr["opts"]
        for opt in chr_opts:
            opts.append((opt, chr_opts[opt]))
        node.append(("sub_frame", "filter options", opts))
        return node


if __name__ == "__main__":
    app = Controller()
    app.start()
