from models import DataRepository
from utils import InputData, TabType
from views import View


class Controller:
    def __init__(self):
        self.window = View(self)
        self.repo = None
        self.path = ""

    def start(self, path: str):
        self.open_file(path)
        self.window.start()

    def open_file(self, path: str):
        self.path = path
        self.repo = DataRepository(path)
        self._update_tab(TabType.FILTERS)
        self._update_tab(TabType.CHARACTERS)

    def save_file(self, path: str = ""):
        if path:
            self.path = path
        self.repo.save_file(self.path)

    def add_record(self, input_data: InputData, tab: TabType):
        self.repo.add(input_data, tab)

    def delete_record(self, index: int, tab: TabType):
        self.repo.delete(index, tab)
        self._update_tab(tab)

    def update_record(self, input_data: InputData, index: int, tab: TabType):
        if self.repo.update(input_data, index, tab):
            self._update_tab(tab)
        else:
            print(f"[Update Failed] Invalid data at index {index} in {tab}")  # TODO

    def move_filter(self, index: int, direction: int):
        self.repo.move_filter(index, direction)
        self._update_tab(TabType.FILTERS)

    def _update_tab(self, tab: TabType):
        view_list = self.repo.read(tab)
        self.window.refresh_tabs(view_list, tab)


if __name__ == "__main__":
    app = Controller()
    app.start("test.js")
