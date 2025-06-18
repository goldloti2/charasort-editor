from calmjs.parse import asttypes

from utils import Field, WidgetType

from .base_model import BaseModel


class CharacterModel(BaseModel):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    # TODO
    @classmethod
    def parse_input(cls, record: dict):
        raise NotImplementedError(f"TODO: {cls.__name__} parse_input")

    def _refresh_view_list(self):
        view_list = []
        for item in self.tree_list:
            node = []
            node.append((WidgetType.LABEL, "name", item[Field.NAME.value]))
            node.append((WidgetType.LABEL, "img", item[Field.IMG.value]))
            opts = [("key", "option")]
            item_opts = item[Field.OPTS.value]
            for opt in item_opts:
                opts.append((opt, item_opts[opt]))
            node.append((WidgetType.SUB_FRAME, "filter options", opts))
            view_list.append(node)
        self.view_list = view_list
