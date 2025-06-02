from calmjs.parse import io, es5
from calmjs.parse import asttypes
from calmjs.parse.unparsers.es5 import pretty_print
from calmjs.parse.unparsers.extractor import ast_to_dict
from calmjs.parse.walkers import Walker

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from control import Controller


class Model:
    def __init__(self, path: str):
        with open(path, "r", encoding = "UTF-8") as file:
            tree = io.read(es5, file)

        walker = Walker()
        for node in walker.filter(
                tree, lambda n: (
                    isinstance(n, asttypes.Assign)
                    and isinstance(n.left, asttypes.DotAccessor)
                )
        ):
            if node.left.identifier.value == "options":
                filters = node.right
            elif node.left.identifier.value == "characterData":
                characters = node.right

        self.tree = tree
        self.waler = walker
        self.filters = filters
        self.characters = characters
        self.flt_list = self.tree_to_list(filters)
        self.chr_list = self.tree_to_list(characters)
    
    def tree_to_list(self, tree: asttypes.Array) -> list:
        new_list = []
        for child in tree.children():
            node = {}
            for prop in child.children():
                if isinstance(prop.right, asttypes.Array):      # sub[]
                    value = self.tree_to_list(prop.right)
                elif isinstance(prop.right, asttypes.Object):   # opts{}
                    value = {}
                    for opts in prop.right.children():
                        if isinstance(opts.right, asttypes.Array):
                            opts_list = [opt.value
                                         for opt in opts.right.children()]
                            value[opts.left.value] = opts_list
                        else:
                            value[opts.left.value] = opts.right.value
                else:
                    value = prop.right.value
                node[prop.left.value] = value
            new_list.append(node)
        return new_list