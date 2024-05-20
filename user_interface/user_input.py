def get_menu_choice():
    """
    Function to get the user's menu choice.
    Uses recursion to ensure valid input.
    """
    try:
        choice = int(input("> "))
        if 1 <= choice <= 4:
            return choice
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            return get_menu_choice()  # Recursive call
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4.")
        return get_menu_choice()  # Recursive call


def get_difficulty_choice():
    """
    Function to get the user's difficulty choice.
    """
    print("Choose difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    try:
        choice = int(input("> "))
        if 1 <= choice <= 3:
            return ["easy", "medium", "hard"][choice - 1]
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
            return get_difficulty_choice()  # Recursive call
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
        return get_difficulty_choice()  # Recursive call
