from abc import ABC, abstractmethod

from calmjs.parse import asttypes, es5
from calmjs.parse.walkers import Walker

from utils import InputData, TreeData, ViewData, obj_to_js


def after_db_update(func):
    def wrapper(self: "BaseModel", *args, **kwargs):
        result = func(self, *args, **kwargs)
        self._refresh_tree_list()
        self._refresh_view_list()
        return result

    return wrapper


class BaseModel(ABC):
    def __init__(self, tree: asttypes.Array):
        self.tree = tree
        self.walker = Walker()
        self.tree_list: list[TreeData] = []
        self.view_list: list[ViewData] = []
        self._refresh_tree_list()
        self._refresh_view_list()

    # TODO
    @after_db_update
    def add(self, input_data: InputData):
        raise NotImplementedError("BaseModel not implement 'add'")

    @after_db_update
    def delete(self, index: int):
        self.tree.children().pop(index)

    @after_db_update
    def update(self, valid_dict: dict, index: int):
        js_string = "data = " + obj_to_js(valid_dict)
        tree = es5(js_string)
        node = next(self.walker.filter(tree, lambda n: isinstance(n, asttypes.Object)))
        self.tree.children()[index] = node

    def read(self):
        return self.view_list

    @classmethod
    @abstractmethod
    def validate(cls, input_data: InputData) -> dict:
        raise NotImplementedError(f"{cls.__name__} not implement 'validate'")

    def _refresh_tree_list(self):
        def parse(node: asttypes.Node):
            if isinstance(node, asttypes.Array):
                return [parse(child) for child in node.children()]
            elif isinstance(node, asttypes.Object):
                return {prop.left.value: parse(prop.right) for prop in node.children()}
            else:
                return node.value.strip('"')

        self.tree_list = [parse(child) for child in self.tree.children()]

    @abstractmethod
    def _refresh_view_list(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} not implement '_refresh_view_list'"
        )
