from calmjs.parse import asttypes

from utils import InputData, ViewData, WidgetType

from .base_model import BaseModel
from .sort_mixin import SortMixin


class FilterModel(BaseModel, SortMixin):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    @classmethod
    def parse_input(cls, input_data: InputData):
        if ("name" not in input_data) or ("key" not in input_data):
            print('filter object require "name" and "key" attribute')
            return ""  # TODO

        name = input_data["name"].strip('"')
        key = input_data["key"].strip('"')
        js_string = f'name: "{name}", key: "{key}"'

        if "tooltip" in input_data:
            tooltip = input_data["tooltip"].strip('"')
            js_string = f'{js_string}, tooltip: "{tooltip}"'

        if "checked" in input_data:
            checked = str(input_data["checked"]).lower()
            js_string = f'{js_string}, checked: "{checked}"'

        if "tree" in input_data:
            sub_string = ""
            for item in input_data["tree"]:
                if not item[0] or not item[1]:
                    print(
                        'object in "sub" list in filter require "name" and "key" attribute'
                    )
                    return ""  # TODO
                sub_string = f'{sub_string}, {{name: "{item[0]}", key: "{item[1]}"}}'
            js_string = f"{js_string}, sub: [{sub_string[2:]}]"

        return js_string

    def _refresh_view_list(self):
        view_data_list = []
        for node in self.tree_list:
            view_data = ViewData()
            view_data["name"] = (WidgetType.LABEL, "name", node["name"])
            view_data["key"] = (WidgetType.LABEL, "key", node["key"])
            view_data["tooltip"] = (
                WidgetType.LABEL,
                "tooltip",
                node.get("tooltip", ""),
            )
            view_data["checked"] = (
                WidgetType.CHECK,
                "checked",
                str(node.get("checked", "")).lower() == "true",
            )

            subs = [("name", "key")]
            if "sub" in node:
                for sub in node["sub"]:
                    subs.append((sub["name"], sub["key"]))
            view_data["sub"] = (WidgetType.SUB_FRAME, "sub", subs)
            view_data_list.append(view_data)
        self.view_list = view_data_list
