from calmjs.parse import asttypes

from utils import WidgetType

from .base_model import BaseModel


class CharacterModel(BaseModel):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    # TODO
    @classmethod
    def parse_input(cls, record: dict) -> str:
        raise NotImplementedError(f"TODO: {cls.__name__} parse_input")

    def refresh_view_list(self):
        view_list = []
        for item in self.tree_list:
            node = []
            node.append((WidgetType.LABEL, "name", item["name"]))
            node.append((WidgetType.LABEL, "img", item["img"]))
            opts = [("key", "option")]
            item_opts = item["opts"]
            for opt in item_opts:
                opts.append((opt, item_opts[opt]))
            node.append((WidgetType.SUB_FRAME, "filter options", opts))
            view_list.append(node)
        self.view_list = view_list
