import logging

from models import DataRepository
from utils import InputData, TabType
from views import View

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self):
        self.window = View(self)
        self.repo = None
        self.path = ""

    def start(self, path: str):
        self.open_file(path)
        self.window.start()
        logger.info("app start")

    def open_file(self, path: str):
        self.path = path
        # TODO
        self.repo = DataRepository(path)
        self._update_tab(TabType.FILTERS)
        self._update_tab(TabType.CHARACTERS)

    def save_file(self, path: str = ""):
        if path:
            self.path = path
        # TODO
        self.repo.save_file(self.path)

    def add_record(self, input_data: InputData, tab: TabType):
        # TODO
        self.repo.add(input_data, tab)

    def delete_record(self, index: int, tab: TabType):
        # TODO
        self.repo.delete(index, tab)
        self._update_tab(tab)

    def update_record(self, input_data: InputData, index: int, tab: TabType):
        try:
            self.repo.update(input_data, index, tab)
        except ValueError as e:
            logger.warning(
                f"editing {tab.value} #{index} validation failed", exc_info=e
            )
            raise e
        except Exception as e:
            logger.error(f"editing {tab.value} #{index} error", exc_info=e)
            raise e
        else:
            logger.info(f"editing {tab.value} #{index} success")
            self._update_tab(tab)

    def move_filter(self, index: int, direction: int):
        # TODO
        self.repo.move_filter(index, direction)
        self._update_tab(TabType.FILTERS)

    def _update_tab(self, tab: TabType):
        # TODO
        view_list = self.repo.read(tab)
        # TODO
        self.window.refresh_tabs(view_list, tab)


if __name__ == "__main__":
    app = Controller()
    app.start("test.js")
