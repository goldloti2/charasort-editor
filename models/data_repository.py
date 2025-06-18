from typing import Dict

from calmjs.parse import asttypes, es5, io
from calmjs.parse.walkers import Walker

from utils import TabType

from .base_model import BaseModel
from .character_model import CharacterModel
from .filter_model import FilterModel


class DataRepository:
    def __init__(self, path: str):
        with open(path, "r", encoding="UTF-8") as file:
            tree = io.read(es5, file)

        filters = None
        characters = None
        walker = Walker()
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
            raise ValueError("Input file not complete")  # TODO

        self.tree = tree
        self.walker = walker
        self.models: Dict[TabType, BaseModel] = {
            TabType.FILTERS: FilterModel(filters),
            TabType.CHARACTERS: CharacterModel(characters),
        }

    def save_file(self, path: str):
        with open(path, "w") as file:
            print(self.tree, file=file)

    def add(self, input_data: dict, tab: TabType):
        self.models[tab].add(input_data)

    def delete(self, index: int, tab: TabType):
        self.models[tab].delete(index)

    def update(self, input_data: dict, index: int, tab: TabType):
        return self.models[tab].update(input_data, index)

    def move_filter(self, index: int, direction: int):
        self.models[TabType.FILTERS].swap(index, direction)

    def read(self, tab: TabType):
        return self.models[tab].read()


if __name__ == "__main__":
    repo = DataRepository("test.js")
