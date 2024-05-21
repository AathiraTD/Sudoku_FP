def get_menu_choice() -> int:
    """
    Function to get the user's menu choice.

    Returns:
        int: The user's menu choice.
    """

    def prompt_mainmenu_choice() -> int:
        """
        Recursively prompt the user for a valid menu choice.

        Returns:
            int: The user's valid menu choice.
        """
        try:
            choice = int(input("> "))  # Get input from the user
            if 1 <= choice <= 4:
                return choice  # Return valid choice
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
                return prompt_mainmenu_choice()  # Recursive call for invalid input
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            return prompt_mainmenu_choice()  # Recursive call for non-integer input

    return prompt_mainmenu_choice()  # Start the recursion


def get_difficulty_choice() -> str:
    """
    Function to get the user's difficulty choice.

    Returns:
        str: The user's difficulty choice.
    """

    def prompt_difficulty_choice() -> str:
        """
        Recursively prompt the user for a valid difficulty choice.

        Returns:
            str: The user's valid difficulty choice.
        """
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
    """
    print("Enter your moves in the format 'A1=5, B2=3, C3=7'. To make a cell empty - 'A1=None' :")
    return input("> ").strip()


