import os
import json
from typing import Optional, List, Dict, Tuple
from core_data.grid.grid import Grid, Cell, Coordinate
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from puzzle_handler.solve.sudoku_validation import count_solutions
from user_interface.display.display_grid import display_grid
from user_interface.game_actions import game_actions

def prompt_for_load_location() -> str:
    """
    Prompt the user for the load location.

    Returns:
        str: The directory path where saved games are located.
    """
    print("Choose the load location:")
    print("1. Default location (current directory)")
    print("2. Custom location")
    location_choice = input("> ").strip()

    if location_choice == "1":
        return os.getcwd()  # Return the current directory
    elif location_choice == "2":
        custom_location = input("Enter the custom directory path: ").strip()
        if os.path.isdir(custom_location):
            return custom_location  # Return the custom directory if it exists
        else:
            print("Invalid directory. Please try again.")
            return prompt_for_load_location()  # Recursively prompt again if invalid directory
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return prompt_for_load_location()  # Recursively prompt again if invalid choice

def list_saved_game_files(directory: str) -> List[str]:
    """
    List all saved game files in the specified directory.

    Args:
        directory (str): The directory to search for saved game files.

    Returns:
        List[str]: A list of saved game file names.
    """

    def list_files_recursively(index: int, files: List[str]) -> List[str]:
        """
        Recursively list .json files in the directory.

        Args:
            index (int): The current index in the directory listing.
            files (List[str]): The list of found .json files.

        Returns:
            List[str]: The updated list of .json files.
        """
        directory_contents = os.listdir(directory)
        if index >= len(directory_contents):
            return files  # Base case: all files have been checked
        file = directory_contents[index]
        if file.endswith('.json'):
            files.append(file)  # Add .json files to the list
        return list_files_recursively(index + 1, files)  # Recursively check the next file

    return list_files_recursively(0, [])  # Start the recursion with an empty list

def prompt_for_file_choice(files: List[str]) -> str:
    """
    Prompt the user to choose a file from the list of saved game files.

    Args:
        files (List[str]): The list of saved game file names.

    Returns:
        str: The chosen file name.
    """

    def print_files_recursively(index: int) -> None:
        """
        Recursively print the list of files.

        Args:
            index (int): The current index in the list of files.
        """
        if index >= len(files):
            return  # Base case: all files have been printed
        print(f"{index + 1}. {files[index]}")
        print_files_recursively(index + 1)  # Recursively print the next file

    print("Available saved game files:")
    print_files_recursively(0)  # Start printing from the first file

    def get_choice() -> int:
        """
        Prompt the user to enter their choice and validate it.

        Returns:
            int: The valid choice entered by the user.
        """
        try:
            choice = int(input("Enter the number of the file to load: ").strip())
            if 1 <= choice <= len(files):
                return choice  # Return the valid choice
            else:
                print("Invalid choice. Please try again.")
                return get_choice()  # Recursively prompt again if invalid choice
        except ValueError:
            print("Invalid input. Please enter a number.")
            return get_choice()  # Recursively prompt again if invalid input

    choice = get_choice()
    return files[choice - 1]  # Return the chosen file

def validate_saved_game_file(file_path: str) -> Optional[Grid]:
    """
    Validate the saved game file and load the game state.

    Args:
        file_path (str): The path to the saved game file.

    Returns:
        Optional[Grid]: The loaded game state if valid, otherwise None.
    """
    try:
        with open(file_path, 'r') as file:
            game_state = json.load(file)  # Load the game state from the file

        grid_size = game_state['grid_size']
        cells = {
            Coordinate(int(row), int(col), grid_size): Cell(
                CellValue(cell_data['value'], grid_size),
                CellState[cell_data['state']]
            )
            for key, cell_data in game_state['cells'].items()
            for row, col in [key.strip('()').split(',')]
        }

        grid = Grid(cells, grid_size)

        if count_solutions(grid, grid.grid_size) == 1:
            return grid  # Return the grid if it has a unique solution
        else:
            print("The puzzle in the saved file does not have a unique solution.")
            return None  # Return None if the puzzle does not have a unique solution
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Failed to load the saved game file: {e}")
        return None  # Return None if there was an error loading the file

def load_saved_game(config: dict) -> None:
    """
    Load a saved game file and pass control to game actions.

    Args:
        config (dict): Configuration settings.
    """
    directory = prompt_for_load_location()  # Get the load location from the user
    saved_game_files = list_saved_game_files(directory)  # List saved game files in the directory

    if not saved_game_files:
        print("No saved game files found in the specified location.")
        return  # Exit if no saved game files found

    chosen_file = prompt_for_file_choice(saved_game_files)  # Get the user's file choice
    file_path = os.path.join(directory, chosen_file)  # Construct the file path

    grid = validate_saved_game_file(file_path)  # Validate and load the saved game file
    if grid:
        print("Saved game loaded successfully.")
        display_grid(grid)  # Display the loaded grid
        game_actions(config, grid)  # Pass control to game actions
    else:
        print("Failed to load the saved game. Returning to main menu.")
