from calmjs.parse import asttypes, es5, io
from calmjs.parse.walkers import Walker


class Model:
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
        self.waler = walker
        self.filters = filters
        self.characters = characters
        self.flt_list = self.tree_to_list(filters)
        self.chr_list = self.tree_to_list(characters)

    def tree_to_list(self, tree: asttypes.Array) -> list:
        def parse_node(node):
            if isinstance(node, asttypes.Array):
                return [parse_node(child) for child in node.children()]
            elif isinstance(node, asttypes.Object):
                return {
                    prop.left.value: parse_node(prop.right) for prop in node.children()
                }
            else:
                return node.value

        return [parse_node(child) for child in tree.children()]
