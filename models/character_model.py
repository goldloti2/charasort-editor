from calmjs.parse import asttypes

from utils import InputData, ViewData, WidgetType

from .base_model import BaseModel


class CharacterModel(BaseModel):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    # TODO
    @classmethod
    def validate(cls, input_data: InputData):
        raise NotImplementedError(f"TODO: {cls.__name__} validate")

    def _refresh_view_list(self):
        view_data_list = []
        for node in self.tree_list:
            opts = [("key", "option")]
            node_opts = node["opts"]
            for opt in node_opts:
                opts.append((opt, node_opts[opt]))
            view_data = ViewData(
                name=(WidgetType.LABEL, "name", node["name"]),
                img=(WidgetType.LABEL, "img", node["img"]),
                opts=(WidgetType.SUB_FRAME, "filter options", opts),
            )
            view_data_list.append(view_data)
        self.view_list = view_data_list
