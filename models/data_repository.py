import logging

from calmjs.parse import asttypes, es5, io
from calmjs.parse.walkers import Walker

from utils.utils import InputData, TabType

from .character_model import CharacterModel
from .filter_model import FilterModel

logger = logging.getLogger(__name__)

walker = Walker()


class DataRepository:
    def __init__(self, path: str):
        with open(path, "r", encoding="UTF-8") as file:
            tree = io.read(es5, file)

        filters = None
        characters = None
        for node in walker.filter(
            tree,
            lambda n: (
                isinstance(n, asttypes.Assign)
                and isinstance(n.left, asttypes.DotAccessor)
            ),
        ):
            if node.left.identifier.value == "options":
                filters = node.right
            elif node.left.identifier.value == "characterData":
                characters = node.right
        if not (filters and characters):
            raise ValueError("Input file not complete")

        self.tree = tree
        self.models: dict[TabType, FilterModel | CharacterModel] = {
            TabType.FILTERS: FilterModel(filters),
            TabType.CHARACTERS: CharacterModel(characters),
        }
        logger.info("initialized")

    def get_empty_record(self, tab: TabType):
        return self.models[tab].build_view_data({})

    def save_file(self, path: str):
        with open(path, "w", encoding="UTF-8") as file:
            print(self.tree, file=file)

    def add(self, input_data: InputData, tab: TabType):
        valid_dict = self.models[tab].validate(input_data)
        self.models[tab].add(valid_dict)

    def update(self, input_data: InputData, index: int, tab: TabType):
        valid_dict = self.models[tab].validate(input_data)
        self.models[tab].update(valid_dict, index)

    def delete(self, index: int, tab: TabType):
        self.models[tab].delete(index)

    def get_filter_keys(self):
        return self.models[TabType.FILTERS].get_filter_keys()

    def move(self, index: int, tab: TabType, direction: int):
        self.models[tab].swap(index, direction)

    def read(self, tab: TabType):
        return self.models[tab].read()


if __name__ == "__main__":
    repo = DataRepository("test.js")
