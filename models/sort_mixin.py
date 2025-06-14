class SortMixin:
    def move_filter(self, index: int, direction: int):
        swap_idx = index + direction
        swap_list = self.filters.children()
        swap = swap_list[index]
        swap_list[index] = swap_list[swap_idx]
        swap_list[swap_idx] = swap
        self.flt_list = self._tree_to_list(self.filters)
