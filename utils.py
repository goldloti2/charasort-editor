from enum import Enum


class TabType(Enum):
    FILTERS = "filters"
    CHARACTERS = "characters"


class ButtonLabel(Enum):
    EDIT = "edit"
    DELETE = "delete"
    MOVEUP = "↑"
    MOVEDOWN = "↓"


class Field(Enum):
    NAME = "name"
    KEY = "key"
    IMG = "img"
    TOOLTIP = "tooltip"
    CHECKED = "checked"
    SUB = "sub"
    OPTS = "opts"
    TREE = "tree"


class WidgetType(Enum):
    LABEL = "label"
    CHECK = "check"
    SUB_FRAME = "sub_frame"
