from .base_model import BaseModel


class SortMixin:
    @BaseModel.after_db_update
    def swap(self, index: int, direction: int):
        swap_idx = index + direction
        swap_list = self.tree.children()
        swap_list[index], swap_list[swap_idx] = swap_list[swap_idx], swap_list[index]
