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

    def start(self, path: str = "test.js"):
        self.open_file(path)
        logger.info("app start")
        self.window.start()

    def open_file(self, path: str):
        self.path = path
        try:
            self.repo = DataRepository(path)
        except [FileNotFoundError, OSError]:
            # TODO: file error, reopen another file
            pass
        except [AttributeError, TypeError]:
            # TODO: AST error, reopen another file
            pass
        else:
            self._update_tab(TabType.FILTERS)
            self._update_tab(TabType.CHARACTERS)

    def save_file(self, path: str = ""):
        if path:
            self.path = path
        try:
            self.repo.save_file(self.path)
        except [FileNotFoundError, OSError]:
            # TODO: can't save the file, let user retry
            pass

    def add_record(self, input_data: InputData, tab: TabType):
        # TODO: implement add, and catch error
        self.repo.add(input_data, tab)

    def delete_record(self, index: int, tab: TabType):
        try:
            self.repo.delete(index, tab)
        except IndexError as e:
            # TODO: index out of bound, just pop up
            logger.warning(f"{e}, index:{index}")
        else:
            self._update_tab(tab)

    def update_record(self, input_data: InputData, index: int, tab: TabType):
        try:
            self.repo.update(input_data, index, tab)
        except ValueError as e:
            logger.warning(f"editing {tab.value} #{index} validation failed")
            logger.debug("", exc_info=e)
            raise e
        else:
            logger.info(f"editing {tab.value} #{index} success")
            self._update_tab(tab)

    def move_filter(self, index: int, direction: int):
        try:
            self.repo.move_filter(index, direction)
        except IndexError as e:
            # TODO: index out of bound, show message
            logger.warning(e)
        else:
            self._update_tab(TabType.FILTERS)

    def _update_tab(self, tab: TabType):
        try:
            view_list = self.repo.read(tab)
        except KeyError:
            # TODO
            pass
        else:
            self.window.refresh_tabs(view_list, tab)


if __name__ == "__main__":
    app = Controller()
    app.start("test.js")
