from models import DataRepository
from views import View


class Controller:
    def __init__(self):
        self.window = View(self)
        self.repo = None
        self.path = ""
        self.filter_list = []
        self.character_list = []

    def start(self, path: str):
        self.open_file(path)
        self.window.start()

    def open_file(self, path):
        self.path = path
        self.repo = DataRepository(path)
        self._update_tab("filters")
        self._update_tab("characters")

    def save_file(self, path=""):
        if path:
            self.path = path
        self.repo.save_file(self.path)

    def get_record(self, index: int, tab: str):
        if tab == "filters":
            return self.filter_list[index]
        elif tab == "characters":
            return self.character_list[index]

    def delete_record(self, index: int, tab: str):
        if tab == "filters":
            self.repo.filters.delete(index)
        elif tab == "characters":
            self.repo.characters.delete(index)
        self._update_tab(tab)

    def update_record(self, record: dict, index: int, tab: str):
        if tab == "filters":
            if self.repo.filters.update(record, index):
                self._update_tab(tab)
        elif tab == "characters":
            if self.repo.characters.update(record, index):
                self._update_tab(tab)

    def move_filter(self, index: int, direction: int):
        self.repo.filters.swap(index, direction)
        self._update_tab("filters")

    def _update_tab(self, tab: str):
        if tab == "filters":
            new_list = [
                self._gen_node_filter(node) for node in self.repo.filters.tree_list
            ]
            self.filter_list = new_list
        elif tab == "characters":
            new_list = [
                self._gen_node_character(node)
                for node in self.repo.characters.tree_list
            ]
            self.character_list = new_list
        else:
            raise ValueError(f"tab '{tab}' not found in controller._update_tab")
        if new_list:
            self.window.refresh_tabs(new_list, tab)
        else:
            self.window.destroy_tabs(tab)

    @classmethod
    def _gen_node_filter(cls, flt: dict):
        node = []
        node.append(("label", "name", flt["name"]))
        node.append(("label", "key", flt["key"]))
        node.append(("label", "tooltip", flt.get("tooltip", "")))
        node.append(("check", "checked", flt.get("checked", None) == "true"))
        subs = [("name", "key")]
        if "sub" in flt:
            for sub in flt["sub"]:
                subs.append((sub["name"], sub["key"]))
        node.append(("sub_frame", "sub", subs))
        return node

    @classmethod
    def _gen_node_character(cls, chr: dict):
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
    app.start("test.js")
