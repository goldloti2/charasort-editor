from calmjs.parse import asttypes

from utils import Field, WidgetType

from .base_model import BaseModel
from .sort_mixin import SortMixin


class FilterModel(BaseModel, SortMixin):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    @classmethod
    def parse_input(cls, input_data: dict):
        if (Field.NAME.value not in input_data) or (Field.KEY.value not in input_data):
            print('filter object require "name" and "key" attribute')
            return ""  # TODO

        name = input_data[Field.NAME.value].strip('"')
        key = input_data[Field.KEY.value].strip('"')
        js_string = f'name: "{name}", key: "{key}"'

        if Field.TOOLTIP.value in input_data:
            tooltip = input_data[Field.TOOLTIP.value].strip('"')
            js_string = f'{js_string}, tooltip: "{tooltip}"'

        if Field.CHECKED.value in input_data:
            checked = str(input_data[Field.CHECKED.value]).lower()
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
            view_data = []
            view_data.append((WidgetType.LABEL, "name", node[Field.NAME.value]))
            view_data.append((WidgetType.LABEL, "key", node[Field.KEY.value]))
            view_data.append(
                (WidgetType.LABEL, "tooltip", node.get(Field.TOOLTIP.value, ""))
            )
            view_data.append(
                (
                    WidgetType.CHECK,
                    "checked",
                    str(node.get(Field.CHECKED.value, "")).lower() == "true",
                )
            )
            subs = [("name", "key")]
            if Field.SUB.value in node:
                for sub in node[Field.SUB.value]:
                    subs.append((sub[Field.NAME.value], sub[Field.KEY.value]))
            view_data.append((WidgetType.SUB_FRAME, "sub", subs))
            view_data_list.append(view_data)
        self.view_list = view_data_list
