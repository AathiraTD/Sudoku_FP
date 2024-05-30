from typing import List, Tuple, Optional

# Define the Node as a tuple
Node = Tuple[
    Optional['Node'], Optional['Node'], Optional['Node'], Optional['Node'], Optional[int], Optional[int], Optional[
        'ColumnNode']]
ColumnNode = Tuple[
    Optional['Node'], Optional['Node'], Optional['Node'], Optional['Node'], Optional[int], Optional[int], int]


def create_node(row: Optional[int] = None, col: Optional[int] = None) -> Node:
    """Create a new node."""
    return (None, None, None, None, row, col, None)


def create_column_node(col: Optional[int] = None) -> ColumnNode:
    """Create a new column header node."""
    return (None, None, None, None, None, col, 0)


def link_columns(header: ColumnNode, columns: List[ColumnNode], index: int) -> ColumnNode:
    """Recursively link column headers into a circular doubly linked list."""
    if index >= len(columns):
        return header
    column = columns[index]
    header_left = header[0] or header  # Initialize header_left if it's None
    column = (header_left, header, *column[2:])
    header_left = (header_left[0], column, *header_left[2:])
    header = (column, header[1], *header[2:])
    return link_columns(header, columns, index + 1)


def add_rows(matrix: List[List[int]], columns: List[ColumnNode], row_index: int):
    """Recursively add rows to the Dancing Links structure."""
    if row_index >= len(matrix):
        return
    row = matrix[row_index]
    add_row(columns, row, row_index, 0, None)
    add_rows(matrix, columns, row_index + 1)


def add_row(columns: List[ColumnNode], row: List[int], row_index: int, col_index: int, prev_node: Optional[Node]):
    """Recursively add nodes for a single row to the Dancing Links structure."""
    if col_index >= len(row):
        return
    if row[col_index]:
        node = create_node(row_index, col_index)
        col_node = columns[col_index]
        col_node_size = col_node[6] + 1
        columns[col_index] = (*col_node[:6], col_node_size)

        if prev_node:
            prev_node_left = prev_node[0] or prev_node
            node = (prev_node_left, prev_node, *node[2:])
            prev_node_left = (prev_node_left[0], node, *prev_node_left[2:])
            prev_node = (node, prev_node[1], *prev_node[2:])
        else:
            prev_node = node

        col_node_up = col_node[2] or col_node
        node = (*node[:2], col_node_up, col_node, *node[4:])
        col_node_up = (*col_node_up[:3], node, *col_node_up[4:])
        columns[col_index] = (*col_node[:2], node, *col_node[3:])

    add_row(columns, row, row_index, col_index + 1, prev_node)


def build_dancing_links(matrix: List[List[int]]) -> ColumnNode:
    """Build the Dancing Links structure from the given matrix."""
    columns = [create_column_node(i) for i in range(len(matrix[0]))]
    header = create_column_node()
    header = link_columns(header, columns, 0)
    add_rows(matrix, columns, 0)
    return header


def search(header: ColumnNode, solution: List[Node], k: int = 0) -> bool:
    """Search for the solution using the Dancing Links algorithm."""
    if header[1] == header:
        return True  # Solution found

    column = select_column(header)
    cover(column)
    return search_row(column[3], column, header, solution, k)


def search_row(row: Node, column: ColumnNode, header: ColumnNode, solution: List[Node], k: int) -> bool:
    """Recursively search through rows for a solution."""
    if row == column:
        uncover(column)
        return False

    solution.append(row)
    cover_row(row[1], row)

    if search(header, solution, k + 1):
        return True

    solution.pop()
    uncover_row(row[0], row)
    return search_row(row[3], column, header, solution, k)


def cover_row(right_node: Node, row: Node):
    """Recursively cover nodes in the row."""
    if right_node == row:
        return
    cover(right_node[6])
    cover_row(right_node[1], row)


def uncover_row(left_node: Node, row: Node):
    """Recursively uncover nodes in the row."""
    if left_node == row:
        return
    uncover(left_node[6])
    uncover_row(left_node[0], row)


def cover(column: ColumnNode):
    """Cover the given column."""
    column_right = column[1]
    column_left = column[0]
    column_right = (column_left, *column_right[1:])
    column_left = (*column_left[:1], column_right, *column_left[2:])
    cover_column(column[3], column)


def cover_column(row: Node, column: ColumnNode):
    """Recursively cover nodes in the column."""
    if row == column:
        return
    cover_row_nodes(row[1], row)
    cover_column(row[3], column)


def cover_row_nodes(right_node: Node, row: Node):
    """Recursively cover nodes in the row."""
    if right_node == row:
        return
    right_node_down = right_node[3]
    right_node_up = right_node[2]
    right_node_down = (*right_node_down[:2], right_node_up, *right_node_down[3:])
    right_node_up = (*right_node_up[:3], right_node_down, *right_node_up[4:])
    right_node_column_size = right_node[6][6]
    right_node_column_size -= 1
    right_node = (*right_node[:6], right_node_column_size)
    cover_row_nodes(right_node[1], row)


def uncover(column: ColumnNode):
    """Uncover the given column."""
    uncover_column(column[2], column)
    column_right = column[1]
    column_left = column[0]
    column_right = (column, *column_right[1:])
    column_left = (*column_left[:1], column, *column_left[2:])


def uncover_column(row: Node, column: ColumnNode):
    """Recursively uncover nodes in the column."""
    if row == column:
        return
    uncover_row_nodes(row[0], row)
    uncover_column(row[2], column)


def uncover_row_nodes(left_node: Node, row: Node):
    """Recursively uncover nodes in the row."""
    if left_node == row:
        return
    left_node_column_size = left_node[6][6]
    left_node_column_size += 1
    left_node = (*left_node[:6], left_node_column_size)
    left_node_down = left_node[3]
    left_node_up = left_node[2]
    left_node_down = (*left_node_down[:2], left_node, *left_node_down[3:])
    left_node_up = (*left_node_up[:3], left_node, *left_node_up[4:])
    uncover_row_nodes(left_node[0], row)


def select_column(header: ColumnNode) -> ColumnNode:
    """Select the column with the fewest 1s."""
    min_size = float('inf')
    selected_column = None

    def find_column(column: ColumnNode):
        nonlocal min_size, selected_column
        if column == header:
            return
        if column[6] < min_size:
            min_size = column[6]
            selected_column = column
        find_column(column[1])

    find_column(header[1])
    return selected_column
