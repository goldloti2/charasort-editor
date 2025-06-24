import logging

from calmjs.parse import asttypes

from utils import InputData, ViewData, WidgetType

from .base_model import BaseModel

logger = logging.getLogger(__name__)


class CharacterModel(BaseModel):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)
        logger.info(f"initialized, get {len(self.tree_list)} data")

    # TODO: character validate
    @classmethod
    def validate(cls, input_data: InputData):
        raise NotImplementedError(f"{cls.__name__} validate")

    @classmethod
    def build_view_data(cls, node: dict):
        opts = [("key", "option")]
        node_opts = node["opts"]
        for opt in node_opts:
            opts.append((opt, node_opts[opt]))
        view_data = ViewData(
            name=(WidgetType.LABEL, "name", node.get("name", "")),
            img=(WidgetType.LABEL, "img", node.get("img", "")),
            opts=(WidgetType.SUB_FRAME, "filter options", opts),
        )
        return view_data
