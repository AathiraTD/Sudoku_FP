from typing import List, Optional, Tuple

from utils.grid_utils import label_to_index


def parse_user_input(user_input: str, grid_size: int) -> List[Tuple[Tuple[int, int], int]]:
    """
    Parse user input into a list of (coordinate, value) tuples.

    Args:
        user_input (str): The user's input string.
        grid_size (int): The size of the grid.

    Returns:
        List[Tuple[Tuple[int, int], int]]: A list of parsed (coordinate, value) tuples.
    """
    moves = user_input.split(',')
    parsed_moves = []

    def parse_move(move_list: List[str], acc: List[Tuple[Tuple[int, int], int]]) -> List[Tuple[Tuple[int, int], int]]:
        if not move_list:
            return acc  # Base case: all moves have been parsed

        move = move_list[0].strip()
        if '=' not in move:
            raise ValueError(f"Invalid input format: {move}")

        position, value = move.split('=')
        coord = label_to_index(position.strip(), grid_size)
        if coord is None or not value.strip().isdigit():
            raise ValueError(f"Invalid input format: {move}")

        acc.append((coord, int(value.strip())))
        return parse_move(move_list[1:], acc)  # Recursively parse the next move

    return parse_move(moves, parsed_moves)  # Start parsing from the first move
