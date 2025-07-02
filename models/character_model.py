import logging

from calmjs.parse import asttypes

from utils import CharacterInput, InputData, ViewData, WidgetType

from .base_model import BaseModel
from .sort_mixin import SortMixin

logger = logging.getLogger(__name__)


class CharacterModel(BaseModel, SortMixin):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)
        logger.info(f"initialized, get {len(self.tree_list)} data")

    @classmethod
    def validate(cls, input_data: InputData):
        return CharacterInput(**input_data).model_dump(exclude_defaults=True)

    @classmethod
    def build_view_data(cls, node: dict):
        opts = [("key", "option")]
        node_opts = node.get("opts", {})
        for opt in node_opts:
            opts.append((opt, node_opts[opt]))
        view_data = ViewData(
            name=(WidgetType.LABEL, "name", node.get("name", "")),
            img=(WidgetType.LABEL, "img", node.get("img", "")),
            opts=(WidgetType.SUB_FRAME, "filter options", opts),
        )
        return view_data
