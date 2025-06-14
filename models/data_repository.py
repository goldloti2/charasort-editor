from calmjs.parse import asttypes, es5, io
from calmjs.parse.walkers import Walker

from .character_model import CharacterModel
from .filter_model import FilterModel


class DataRepository:
    def __init__(self, path: str):
        with open(path, "r", encoding="UTF-8") as file:
            tree = io.read(es5, file)

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

        self.tree = tree
        self.walker = walker
        self.filters = FilterModel(filters)
        self.characters = CharacterModel(characters)

    def save_file(self, path: str):
        with open(path, "w") as file:
            print(self.tree, file=file)


if __name__ == "__main__":
    repo = DataRepository("test.js")
