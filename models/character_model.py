from calmjs.parse import asttypes

from .base_model import BaseModel


class CharacterModel(BaseModel):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    # TODO
    @classmethod
    def parse_input(cls, record: dict) -> str:
        raise NotImplementedError(f"TODO: {cls.__name__} parse_input")

    def gen_view_node(self):
        node_list = []
        for item in self.tree_list:
            node = []
            node.append(("label", "name", item["name"]))
            node.append(("label", "img", item["img"]))
            opts = [("key", "option")]
            item_opts = item["opts"]
            for opt in item_opts:
                opts.append((opt, item_opts[opt]))
            node.append(("sub_frame", "filter options", opts))
            node_list.append(node)
        return node_list
