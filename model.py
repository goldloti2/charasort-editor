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
        self.walker = walker
        self.filters = filters
        self.characters = characters
        self.flt_list = self._tree_to_list(filters)
        self.chr_list = self._tree_to_list(characters)

    def save_file(self, path: str):
        with open(path, "w") as file:
            print(self.tree, file=file)

    def move_filter(self, index: int, direction: int):
        swap_idx = index + direction
        swap_list = self.filters.children()
        swap = swap_list[index]
        swap_list[index] = swap_list[swap_idx]
        swap_list[swap_idx] = swap
        self.flt_list = self._tree_to_list(self.filters)

    def delete_record(self, index: int, tab: str):
        if tab == "filters":
            self.filters.children().pop(index)
            self.flt_list = self._tree_to_list(self.filters)
        elif tab == "characters":
            self.characters.children().pop(index)
            self.chr_list = self._tree_to_list(self.characters)

    def update_filter(self, record: dict, index: int):
        if ("name" not in record) or ("key" not in record):
            print('filter object require "name" and "key" attribute')
            return False

        name = record["name"].strip('"')
        key = record["key"].strip('"')
        js_string = f'name: "{name}", key: "{key}"'

        if "tooltip" in record:
            tooltip = record["tooltip"].strip('"')
            js_string = f'{js_string}, tooltip: "{tooltip}"'

        if "checked" in record:
            checked = "true" if record["checked"] else "false"
            js_string = f'{js_string}, checked: "{checked}"'

        if "tree" in record:
            sub_string = ""
            for item in record["tree"]:
                if not item[0] or not item[1]:
                    print(
                        '"sub" attribute in filter object require "name" and "key" attribute'
                    )
                    return False
                sub_string = f'{sub_string}, {{name: "{item[0]}", key: "{item[1]}"}}'
            js_string = f"{js_string}, sub: [{sub_string[2:]}]"

        js_string = f"data = {{ {js_string} }}"
        tree = es5(js_string)
        node = next(self.walker.filter(tree, lambda n: isinstance(n, asttypes.Object)))
        self.filters.children()[index] = node
        self.flt_list = self._tree_to_list(self.filters)
        return True

    def _tree_to_list(self, tree: asttypes.Array) -> list:
        def parse_node(node):
            if isinstance(node, asttypes.Array):
                return [parse_node(child) for child in node.children()]
            elif isinstance(node, asttypes.Object):
                return {
                    prop.left.value: parse_node(prop.right) for prop in node.children()
                }
            else:
                return node.value.strip('"')

        return [parse_node(child) for child in tree.children()]
