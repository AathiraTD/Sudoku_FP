import numpy as np
cimport numpy as np

def is_valid(np.ndarray[int, ndim=2] grid, int row, int col, int num, int grid_size):
    cdef int subgrid_size = int(grid_size ** 0.5)
    cdef int start_row = (row // subgrid_size) * subgrid_size
    cdef int start_col = (col // subgrid_size) * subgrid_size

    def check_row_col(r: int, c: int) -> bool:
        if r >= grid_size:
            return True
        if grid[row, r] == num or grid[r, col] == num:
            return False
        return check_row_col(r + 1, c)

    def check_subgrid(sr: int, sc: int, r: int, c: int) -> bool:
        if r >= sr + subgrid_size:
            return True
        if c >= sc + subgrid_size:
            return check_subgrid(sr, sc, r + 1, sc)
        if grid[r, c] == num:
            return False
        return check_subgrid(sr, sc, r, c + 1)

    return check_row_col(0, 0) and check_subgrid(start_row, start_col, start_row, start_col)


