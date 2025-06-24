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
        except (FileNotFoundError, OSError) as e:
            logger.error(e)
            logger.debug("", exc_info=e)
            self.window.show_error(f"{path} cannot open.\nPlease try another file.")
        except (AttributeError, ValueError, KeyError) as e:
            logger.error(e)
            logger.debug("", exc_info=e)
            self.window.show_error(
                f"{path} contains an invalid format.\nPlease try another file."
            )
        else:
            logger.info(f"open file success: {path}")
            self._update_tab(TabType.FILTERS)
            self._update_tab(TabType.CHARACTERS)

    def save_file(self, path: str = ""):
        if path:
            self.path = path
        try:
            self.repo.save_file(self.path)
        except (FileNotFoundError, OSError) as e:
            logger.error(e)
            logger.debug("", exc_info=e)
            self.window.show_error(f"Cannot save to {path}.")
        else:
            logger.info(f"save file success: {self.path}")

    def get_empty_record(self, tab: TabType):
        return self.repo.get_empty_record(tab)

    def add_record(self, input_data: InputData, tab: TabType):
        try:
            self.repo.add(input_data, tab)
        except ValueError as e:
            logger.warning(f"adding {tab.value} validation failed")
            logger.debug("", exc_info=e)
            raise e
        else:
            logger.info(f"add success: {tab.value}")
            self._update_tab(tab)

    def update_record(self, input_data: InputData, index: int, tab: TabType):
        try:
            self.repo.update(input_data, index, tab)
        except ValueError as e:
            logger.warning(f"editing {tab.value} #{index} validation failed")
            logger.debug("", exc_info=e)
            raise e
        else:
            logger.info(f"edit success: {tab.value}, #{index}")
            self._update_tab(tab)

    def delete_record(self, index: int, tab: TabType):
        try:
            self.repo.delete(index, tab)
        except IndexError as e:
            logger.error(f"{e}, index: #{index}")
            logger.debug("", exc_info=e)
            self.window.show_error(f"Index #{index} in {tab.value} is out of range.")
        else:
            logger.info(f"delete success: {tab.value}, #{index}")
            self._update_tab(tab)

    def move_filter(self, index: int, direction: int):
        try:
            self.repo.move_filter(index, direction)
        except IndexError as e:
            logger.error(e)
            logger.debug("", exc_info=e)
            self.window.show_error(
                f"Index #{index}{direction:+} in filter is out of range."
            )
        else:
            logger.info(f"swap success: filters, #{index}{direction:+}")
            self._update_tab(TabType.FILTERS)

    def _update_tab(self, tab: TabType):
        try:
            view_list = self.repo.read(tab)
        except KeyError as e:
            logger.error(f"cannot find data of {e}")
            logger.debug("", exc_info=e)
            self.window.show_error(f"cannot find data of {e}")
        else:
            logger.info(f"read success: {tab.value}")
            self.window.refresh_tabs(view_list, tab)


if __name__ == "__main__":
    app = Controller()
    app.start("test.js")
