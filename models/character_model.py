from calmjs.parse import asttypes

from utils import Field, WidgetType

from .base_model import BaseModel


class CharacterModel(BaseModel):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    # TODO
    @classmethod
    def parse_input(cls, input_data: dict):
        raise NotImplementedError(f"TODO: {cls.__name__} parse_input")

    def _refresh_view_list(self):
        view_data_list = []
        for node in self.tree_list:
            view_data = []
            view_data.append((WidgetType.LABEL, "name", node[Field.NAME.value]))
            view_data.append((WidgetType.LABEL, "img", node[Field.IMG.value]))
            opts = [("key", "option")]
            node_opts = node[Field.OPTS.value]
            for opt in node_opts:
                opts.append((opt, node_opts[opt]))
            view_data.append((WidgetType.SUB_FRAME, "filter options", opts))
            view_data_list.append(view_data)
        self.view_list = view_data_list
