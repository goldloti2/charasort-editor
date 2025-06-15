from calmjs.parse import asttypes

from .base_model import BaseModel


class CharacterModel(BaseModel):
    def __init__(self, tree: asttypes.Array):
        super().__init__(tree)

    @classmethod
    def parse_input(cls, record: dict) -> str:
        raise NotImplementedError(f"TODO: {cls.__name__} parse_input")
