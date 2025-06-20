from enum import Enum
from typing import Optional, TypedDict

from pydantic import BaseModel, Field, field_validator, model_validator


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


class FilterSub(BaseModel):
    name: str
    key: str

    @field_validator("name", mode="after")
    @classmethod
    def name_check_empty(cls, val):
        if not val:
            raise ValueError('"name" should contain at least 1 character')
        return val

    @field_validator("key", mode="after")
    @classmethod
    def key_check_empty(cls, val):
        if not val:
            raise ValueError('"key" should contain at least 1 character')
        return val


class FilterInput(BaseModel):
    name: str = Field(min_length=1)
    key: str = Field(min_length=1)
    tooltip: Optional[str] = None
    checked: bool = False
    sub: Optional[list[FilterSub]] = Field(default=None, alias="tree")
    model_config = {"populate_by_name": True}

    @model_validator(mode="before")
    @classmethod
    def convert_input(cls, data):
        if not isinstance(data, dict):
            return data
        for name in ["sub", "tree"]:
            if name in data:
                convert = data.get(name)
                if not isinstance(convert, (list, tuple)):
                    continue
                if all(isinstance(t, (tuple, list)) and len(t) == 2 for t in convert):
                    data[name] = [{"name": t[0], "key": t[1]} for t in convert]
                    break
        return data

    @field_validator("tooltip", mode="after")
    @classmethod
    def tooltip_check_empty(cls, val):
        if not val:
            return None
        return val

    @field_validator("sub", mode="after")
    @classmethod
    def sub_check_empty(cls, val):
        if not val:
            return None
        return val


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


def obj_to_js(value):
    if isinstance(value, dict):
        value_str = (
            "{ "
            + ", ".join(f"{key}: {obj_to_js(val)}" for key, val in value.items())
            + " }"
        )
    elif isinstance(value, list):
        value_str = "[ " + ", ".join([obj_to_js(val) for val in value]) + " ]"
    elif isinstance(value, str):
        value_str = f'"{value}"'
    elif isinstance(value, bool):
        value_str = "true" if value else "false"
    elif value is None:
        value_str = "null"
    else:
        value_str = str(value)
    return value_str
