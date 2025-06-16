from models import DataRepository
from utils import TabType
from views import View


class Controller:
    def __init__(self):
        self.window = View(self)
        self.repo = None
        self.path = ""
        self.tabs_list = {TabType.FILTERS: [], TabType.CHARACTERS: []}

    def start(self, path: str):
        self.open_file(path)
        self.window.start()

    def open_file(self, path):
        self.path = path
        self.repo = DataRepository(path)
        self._update_tab(TabType.FILTERS)
        self._update_tab(TabType.CHARACTERS)

    def save_file(self, path=""):
        if path:
            self.path = path
        self.repo.save_file(self.path)

    def get_record(self, index: int, tab: TabType):
        return self.tabs_list[tab][index]

    def delete_record(self, index: int, tab: TabType):
        if tab == TabType.FILTERS:
            self.repo.filters.delete(index)
        elif tab == TabType.CHARACTERS:
            self.repo.characters.delete(index)
        self._update_tab(tab)

    def update_record(self, record: dict, index: int, tab: TabType):
        if tab == TabType.FILTERS:
            if self.repo.filters.update(record, index):
                self._update_tab(tab)
        elif tab == TabType.CHARACTERS:
            if self.repo.characters.update(record, index):
                self._update_tab(tab)

    def move_filter(self, index: int, direction: int):
        self.repo.filters.swap(index, direction)
        self._update_tab(TabType.FILTERS)

    def _update_tab(self, tab: TabType):
        if tab == TabType.FILTERS:
            new_list = [
                self._gen_node_filter(node) for node in self.repo.filters.tree_list
            ]
        elif tab == TabType.CHARACTERS:
            new_list = [
                self._gen_node_character(node)
                for node in self.repo.characters.tree_list
            ]
        else:
            raise ValueError(f"tab '{tab}' not found in controller._update_tab")
        self.tabs_list[tab] = new_list
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
