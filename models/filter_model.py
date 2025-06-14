from calmjs.parse import asttypes

from .base_model import BaseModel
from .sort_mixin import SortMixin


class FilterModel(BaseModel, SortMixin):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    @classmethod
    def parse_input(cls, record: dict) -> str:
        if ("name" not in record) or ("key" not in record):
            print('filter object require "name" and "key" attribute')
            return False

        name = record["name"].strip('"')
        key = record["key"].strip('"')
        js_string = f'name: "{name}", key: "{key}"'

        if "tooltip" in record:
            tooltip = record["tooltip"].strip('"')
            js_string = f'{js_string}, tooltip: "{tooltip}"'

        if "checked" in record:
            checked = "true" if record["checked"] else "false"
            js_string = f'{js_string}, checked: "{checked}"'

        if "tree" in record:
            sub_string = ""
            for item in record["tree"]:
                if not item[0] or not item[1]:
                    print(
                        'object in "sub" list in filter require "name" and "key" attribute'
                    )
                    return False
                sub_string = f'{sub_string}, {{name: "{item[0]}", key: "{item[1]}"}}'
            js_string = f"{js_string}, sub: [{sub_string[2:]}]"

        return js_string
