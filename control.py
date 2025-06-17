from models import DataRepository
from utils import TabType
from views import View


class Controller:
    def __init__(self):
        self.window = View(self)
        self.repo = None
        self.path = ""

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

    def delete_record(self, index: int, tab: TabType):
        self.repo.models[tab].delete(index)
        self._update_tab(tab)

    def update_record(self, record: dict, index: int, tab: TabType):
        if self.repo.models[tab].update(record, index):
            self._update_tab(tab)
        else:
            print(f"[Update Failed] Invalid data at index {index} in {tab}")  # TODO

    def move_filter(self, index: int, direction: int):
        self.repo.models[TabType.FILTERS].swap(index, direction)
        self._update_tab(TabType.FILTERS)

    def _update_tab(self, tab: TabType):
        new_list = self.repo.models[tab].view_list
        self.window.refresh_tabs(new_list, tab)


if __name__ == "__main__":
    app = Controller()
    app.start("test.js")
