import os
from typing import Tuple


def get_menu_choice() -> int:
    """
   Function to get the user's menu choice.

   Returns:
       int: The user's menu choice.
   """

    def prompt_main_menu_choice() -> int:
        try:
            choice = int(input("> "))  # Get input from the user
            if 1 <= choice <= 4:
                return choice  # Return valid choice
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
                return prompt_main_menu_choice()  # Recursive call for invalid input
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            return prompt_main_menu_choice()  # Recursive call for non-integer input

    return prompt_main_menu_choice()  # Start the recursion


def get_difficulty_choice() -> str:

    def prompt_difficulty_choice() -> str:

        print("Choose difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        try:
            choice = int(input("> "))  # Get input from the user
            if 1 <= choice <= 3:
                return ["easy", "medium", "hard"][choice - 1]  # Return corresponding difficulty
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
                return prompt_difficulty_choice()  # Recursive call for invalid input
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            return prompt_difficulty_choice()  # Recursive call for non-integer input

    return prompt_difficulty_choice()  # Start the recursion


def get_user_move() -> str:
    """
   Function to get the user's move input.

   Returns:
       str: The user's move input.
   """
    print("Enter your moves in the format 'A1=5, B2=3, C3=7'. To make a cell empty - 'A1=None' :")

    def prompt_user_move() -> str:
        """
       Recursively prompt the user for a valid move input.

       Returns:
           str: The user's valid move input.
       """
        user_input = input("> ").strip()  # Get input from the user

        try:
            # Split the input string into individual moves
            moves = user_input.split(",")

            # Check if each move is in the correct format
            for move in moves:
                move = move.strip()  # Remove leading/trailing whitespaces
                if not move:
                    continue  # Skip empty strings

                if "=" not in move:  # Check if the move contains an '=' sign
                    print(f"Invalid move format: '{move}'. Expected format: 'A1=5'.")
                    return prompt_user_move()

                cell, value = move.split("=")  # Split the move into cell and value
                if not (len(cell) == 2 and cell[0].isalpha() and cell[1].isdigit()):  # Check if the cell is in the
                    # correct format
                    print(f"Invalid cell format: '{cell}'. Expected format: 'A1'.")
                    return prompt_user_move()

                if value.lower() != "none" and not value.isdigit():  # Check if the value is a digit or 'None'
                    print(f"Invalid value: '{value}'. Expected a digit or 'None'.")
                    return prompt_user_move()

            return user_input  # Return the valid user input

        except ValueError as e:  # Catch any ValueError exceptions
            print(f"Invalid input: {e}")
            return prompt_user_move()  # Recursive call for invalid input

    return prompt_user_move()  # Start the recursion



def get_post_solve_choice() -> int:

    def prompt_post_solve_choice() -> int:
        """
        Recursively prompt the user for a valid post-solve choice.

        Returns:
            int: The user's valid choice (1 for new game, 2 for main menu).
        """

        print("Please Select an Option")
        print("1. Play a new game")
        print("2. Return to main menu")

        try:
            choice = int(input("> "))  # Get input from the user
            if choice == 1 or choice == 2:
                return choice  # Return valid choice
            else:
                print("Invalid choice. Please enter 1 or 2.")
                return prompt_post_solve_choice()  # Recursive call for invalid input
        except ValueError:
            print("Invalid input. Please enter a number (1 or 2).")
            return prompt_post_solve_choice()  # Recursive call for non-integer input

    return prompt_post_solve_choice()  # Start the recursion


def get_hint_choice() -> str:
    """
    Prompt the user to choose between a random or specific cell for the hint, or to go back to the game action screen.
    Returns the user's choice as a string.
    """
    def prompt_hint_choice() -> str:
        """
        Recursively prompt the user for a valid hint choice.
        """
        print("\nChoose an option for hint:")
        print("1. Random cell")
        print("2. Specific cell")
        # print("3. Back to game action screen")

        choice = input("> ").strip()
        if choice == '1':
            return 'random'
        elif choice == '2':
            return 'specific'
        # elif choice == '3':
        #     return
        else:
            print("Invalid choice. Please enter 1 or 2,")
            return prompt_hint_choice()  # Recursive call for invalid input

    return prompt_hint_choice()  # Start the recursion


def prompt_for_file_details() -> Tuple[str, str]:
    """
    Prompt the user for the file name and save location.

    Returns:
        Tuple[str, str]: The file name and the directory path.
    """
    # Prompt for file name
    file_name = input("Enter the file name (without extension): ").strip()
    if not file_name.endswith(".json"):
        file_name += ".json"

    # Prompt for save location
    print("Choose the save location:")
    print("1. Default location (current directory)")
    print("2. Custom location")
    location_choice = input("> ").strip()

    if location_choice == "1":
        return file_name, os.getcwd()  # Return the current directory
    elif location_choice == "2":
        directory = input("Enter the custom directory path: ").strip()
        if os.path.isdir(directory):
            return file_name, directory  # Return the custom directory if it exists
        else:
            print("Invalid directory. Saving to the default location instead.")
            return file_name, os.getcwd()  # Use the default directory if the custom one is invalid
    else:
        print("Invalid choice. Saving to the default location instead.")
        return file_name, os.getcwd()  # Use the default directory if the choice is invalid