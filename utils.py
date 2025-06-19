from enum import Enum
from typing import Optional, TypedDict

from pydantic import BaseModel, model_validator


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


class ViewData(BaseModel):
    name: tuple[WidgetType, str, str]
    key: Optional[tuple[WidgetType, str, str]] = None
    img: Optional[tuple[WidgetType, str, str]] = None
    tooltip: Optional[tuple[WidgetType, str, str]] = None
    checked: Optional[tuple[WidgetType, str, bool]] = None
    sub: Optional[tuple[WidgetType, str, list[tuple[str, str]]]] = None
    opts: Optional[tuple[WidgetType, str, list[tuple[str, str | list[str]]]]] = None

    @model_validator(mode="after")
    def verify_filter_or_character(self):
        filter_required = bool(self.key)
        filter_has = any([self.key, self.tooltip, self.checked, self.sub])
        character_required = bool(self.img and self.opts)
        character_has = any([self.img, self.opts])
        if (not filter_required or character_has) and (
            not character_required or filter_has
        ):
            raise ValueError(
                "Expected to be filter or character view but not both.\n"
                + f"filter_required:    {filter_required}\n"
                + f"filter_has:         {filter_has}\n"
                + f"character_required: {character_required}\n"
                + f"character_has:      {character_has}\n"
            )
        return self


class InputData(TypedDict):
    name: str
    key: str
    img: str
    tooltip: str
    checked: bool
    tree: list[tuple[str, str]]
    # opts: dict[str, list[str]]


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
