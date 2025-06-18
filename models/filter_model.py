from calmjs.parse import asttypes

from utils import Field, WidgetType

from .base_model import BaseModel
from .sort_mixin import SortMixin


class FilterModel(BaseModel, SortMixin):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    @classmethod
    def parse_input(cls, record: dict):
        if (Field.NAME.value not in record) or (Field.KEY.value not in record):
            print('filter object require "name" and "key" attribute')
            return ""  # TODO

        name = record[Field.NAME.value].strip('"')
        key = record[Field.KEY.value].strip('"')
        js_string = f'name: "{name}", key: "{key}"'

        if Field.TOOLTIP.value in record:
            tooltip = record[Field.TOOLTIP.value].strip('"')
            js_string = f'{js_string}, tooltip: "{tooltip}"'

        if Field.CHECKED.value in record:
            checked = str(record[Field.CHECKED.value]).lower()
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

    def _refresh_view_list(self):
        view_list = []
        for item in self.tree_list:
            node = []
            node.append((WidgetType.LABEL, "name", item[Field.NAME.value]))
            node.append((WidgetType.LABEL, "key", item[Field.KEY.value]))
            node.append(
                (WidgetType.LABEL, "tooltip", item.get(Field.TOOLTIP.value, ""))
            )
            node.append(
                (
                    WidgetType.CHECK,
                    "checked",
                    str(item.get(Field.CHECKED.value, "")).lower() == "true",
                )
            )
            subs = [("name", "key")]
            if Field.SUB.value in item:
                for sub in item[Field.SUB.value]:
                    subs.append((sub[Field.NAME.value], sub[Field.KEY.value]))
            node.append((WidgetType.SUB_FRAME, "sub", subs))
            view_list.append(node)
        self.view_list = view_list
