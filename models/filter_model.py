import logging

from calmjs.parse import asttypes

from utils import FilterInput, InputData, ViewData, WidgetType

from .base_model import BaseModel
from .sort_mixin import SortMixin

logger = logging.getLogger(__name__)


class FilterModel(BaseModel, SortMixin):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)
        logger.info(f"initialized, get {len(self.tree_list)} data")

    @classmethod
    def validate(cls, input_data: InputData):
        return FilterInput(**input_data).model_dump(exclude_defaults=True)

    @classmethod
    def build_view_data(cls, node: dict):
        subs = [("name", "key")]
        if "sub" in node:
            for sub in node["sub"]:
                subs.append((sub["name"], sub["key"]))
        view_data = ViewData(
            name=(WidgetType.LABEL, "name", node["name"]),
            key=(WidgetType.LABEL, "key", node["key"]),
            tooltip=(WidgetType.LABEL, "tooltip", node.get("tooltip", "")),
            checked=(
                WidgetType.CHECK,
                "checked",
                str(node.get("checked", "")).lower() == "true",
            ),
            sub=(WidgetType.SUB_FRAME, "sub", subs),
        )
        return view_data

    def _refresh_view_list(self):
        view_data_list = []
        for node in self.tree_list:
            subs = [("name", "key")]
            if "sub" in node:
                for sub in node["sub"]:
                    subs.append((sub["name"], sub["key"]))
            view_data = ViewData(
                name=(WidgetType.LABEL, "name", node["name"]),
                key=(WidgetType.LABEL, "key", node["key"]),
                tooltip=(WidgetType.LABEL, "tooltip", node.get("tooltip", "")),
                checked=(
                    WidgetType.CHECK,
                    "checked",
                    str(node.get("checked", "")).lower() == "true",
                ),
                sub=(WidgetType.SUB_FRAME, "sub", subs),
            )
            view_data_list.append(view_data)
        self.view_list = view_data_list
