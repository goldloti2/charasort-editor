from abc import ABC, abstractmethod

from calmjs.parse import asttypes, es5
from calmjs.parse.walkers import Walker


class BaseModel(ABC):
    @staticmethod
    def after_db_update(func):
        def wrapper(self: "BaseModel", *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.refresh_tree_list()
            return result

        return wrapper

    @after_db_update
    def __init__(self, tree: asttypes.Array):
        self.tree = tree
        self.walker = Walker()
        self.tree_list = []

    @after_db_update
    def add(self, record: dict):
        raise NotImplementedError("BaseModel not implement 'add'")

    @after_db_update
    def delete(self, index: int):
        self.tree.children().pop(index)

    @after_db_update
    def update(self, record: dict, index: int):
        js_string = self.parse_input(record)
        if not js_string:
            return False
        js_string = f"data = {{ {js_string} }}"
        tree = es5(js_string)
        node = next(self.walker.filter(tree, lambda n: isinstance(n, asttypes.Object)))
        self.tree.children()[index] = node
        return True

    def read(self):
        return self.tree_list

    @classmethod
    @abstractmethod
    def parse_input(cls, record: dict) -> str:
        raise NotImplementedError(f"{cls.__name__} not implement 'parse_input'")

    def refresh_tree_list(self):
        def parse(node):
            if isinstance(node, asttypes.Array):
                return [parse(child) for child in node.children()]
            elif isinstance(node, asttypes.Object):
                return {prop.left.value: parse(prop.right) for prop in node.children()}
            else:
                return node.value.strip('"')

        self.tree_list = [parse(child) for child in self.tree.children()]
