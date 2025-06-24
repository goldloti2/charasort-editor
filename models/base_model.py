from abc import ABC, abstractmethod

from calmjs.parse import asttypes, es5
from calmjs.parse.walkers import Walker

from utils import InputData, TreeData, ViewData, obj_to_js

walker = Walker()


def after_db_update(func):
    def wrapper(self: "BaseModel", *args, **kwargs):
        result = func(self, *args, **kwargs)
        self._refresh_lists()
        return result

    return wrapper


class BaseModel(ABC):
    def __init__(self, tree: asttypes.Array):
        self.tree = tree
        self.tree_list: list[TreeData] = []
        self.view_list: list[ViewData] = []
        self._refresh_lists()

    @after_db_update
    def add(self, valid_dict: dict):
        node = self._dict_to_tree(valid_dict)
        self.tree.children().append(node)

    @after_db_update
    def update(self, valid_dict: dict, index: int):
        node = self._dict_to_tree(valid_dict)
        self.tree.children()[index] = node

    @after_db_update
    def delete(self, index: int):
        self.tree.children().pop(index)

    def read(self):
        return self.view_list

    @classmethod
    @abstractmethod
    def validate(cls, input_data: InputData) -> dict:
        raise NotImplementedError(f"{cls.__name__} not implement 'validate'")

    @classmethod
    @abstractmethod
    def build_view_data(cls, node: dict) -> ViewData:
        raise NotImplementedError(f"{cls.__name__} not implement 'build_view_data'")

    @classmethod
    def _dict_to_tree(cls, valid_dict: dict) -> asttypes.Object:
        js_string = "data = " + obj_to_js(valid_dict)
        tree = es5(js_string)
        return next(walker.filter(tree, lambda n: isinstance(n, asttypes.Object)))

    def _refresh_lists(self):
        self._refresh_tree_list()
        self._refresh_view_list()

    def _refresh_tree_list(self):
        def parse(node: asttypes.Node):
            if isinstance(node, asttypes.Array):
                return [parse(child) for child in node.children()]
            elif isinstance(node, asttypes.Object):
                return {prop.left.value: parse(prop.right) for prop in node.children()}
            elif node.value == "true":
                return True
            elif node.value == "false":
                return False
            else:
                return node.value.strip('"')

        self.tree_list = [parse(child) for child in self.tree.children()]

    def _refresh_view_list(self):
        view_data_list = []
        for node in self.tree_list:
            view_data = self.build_view_data(node)
            view_data_list.append(view_data)
        self.view_list = view_data_list
