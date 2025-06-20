from enum import Enum
from typing import TypedDict


class TabType(Enum):
    FILTERS = "filters"
    CHARACTERS = "characters"


class ButtonLabel(Enum):
    EDIT = "edit"
    DELETE = "delete"
    MOVEUP = "↑"
    MOVEDOWN = "↓"


class WidgetType(Enum):
    LABEL = "label"
    CHECK = "check"
    SUB_FRAME = "sub_frame"


class InputData(TypedDict):
    name: str
    key: str
    img: str
    tooltip: str
    checked: bool
    tree: list[tuple[str, str]]
    # opts: dict[str, list[str]]


class ViewData(TypedDict):
    name: tuple[WidgetType, str, str]
    key: tuple[WidgetType, str, str]
    img: tuple[WidgetType, str, str]
    tooltip: tuple[WidgetType, str, str]
    checked: tuple[WidgetType, str, bool]
    sub: tuple[WidgetType, str, list[tuple[str, str]]]
    opts: tuple[WidgetType, str, list[tuple[str, str | list[str]]]]


class SubData(TypedDict):
    name: str
    key: str


class TreeData(TypedDict):
    name: str
    key: str
    img: str
    tooltip: str
    checked: str
    sub: list[SubData]
    opts: dict[str, list[str]]
