from .base_model import after_db_update


class SortMixin:
    @after_db_update
    def swap(self, index: int, direction: int):
        swap_idx = index + direction
        swap_list = self.tree.children()
        if not (0 <= index < len(swap_list)) or not (0 <= swap_idx < len(swap_list)):
            raise IndexError(
                f"swapping index out of range. index:{index}, swap:{swap_idx}, len:{len(swap_list)}"
            )
        swap_list[index], swap_list[swap_idx] = swap_list[swap_idx], swap_list[index]
