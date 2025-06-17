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
            new_list = self.repo.filters.gen_view_node()
        elif tab == TabType.CHARACTERS:
            new_list = self.repo.characters.gen_view_node()
        else:
            raise ValueError(f"tab '{tab}' not found in controller._update_tab")
        self.tabs_list[tab] = new_list
        self.window.refresh_tabs(new_list, tab)


if __name__ == "__main__":
    app = Controller()
    app.start("test.js")
