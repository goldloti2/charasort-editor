from calmjs.parse import asttypes

from utils import WidgetType

from .base_model import BaseModel
from .sort_mixin import SortMixin


class FilterModel(BaseModel, SortMixin):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    @classmethod
    def parse_input(cls, record: dict) -> str:
        if ("name" not in record) or ("key" not in record):
            print('filter object require "name" and "key" attribute')
            return ""  # TODO

        name = record["name"].strip('"')
        key = record["key"].strip('"')
        js_string = f'name: "{name}", key: "{key}"'

        if "tooltip" in record:
            tooltip = record["tooltip"].strip('"')
            js_string = f'{js_string}, tooltip: "{tooltip}"'

        if "checked" in record:
            checked = str(record["checked"]).lower()
            js_string = f'{js_string}, checked: "{checked}"'

        if "tree" in record:
            sub_string = ""
            for item in record["tree"]:
                if not item[0] or not item[1]:
                    print(
                        'object in "sub" list in filter require "name" and "key" attribute'
                    )
                    return ""  # TODO
                sub_string = f'{sub_string}, {{name: "{item[0]}", key: "{item[1]}"}}'
            js_string = f"{js_string}, sub: [{sub_string[2:]}]"

        return js_string

    def refresh_view_list(self):
        view_list = []
        for item in self.tree_list:
            node = []
            node.append((WidgetType.LABEL, "name", item["name"]))
            node.append((WidgetType.LABEL, "key", item["key"]))
            node.append((WidgetType.LABEL, "tooltip", item.get("tooltip", "")))
            node.append(
                (
                    WidgetType.CHECK,
                    "checked",
                    str(item.get("checked", "")).lower() == "true",
                )
            )
            subs = [("name", "key")]
            if "sub" in item:
                for sub in item["sub"]:
                    subs.append((sub["name"], sub["key"]))
            node.append((WidgetType.SUB_FRAME, "sub", subs))
            view_list.append(node)
        self.view_list = view_list
