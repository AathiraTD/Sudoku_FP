def display_menu_with_title(title: str, options: dict, prompt: str = "Choose an option:") -> None:
    print(title)
    display_options_recursively(options, 1)
    print(prompt)


def display_options_recursively(options: dict, current_index: int) -> None:
    if current_index > len(options):
        return

    if current_index in options:
        description, _ = options[current_index]
        print(f"{current_index}. {description}")

    display_options_recursively(options, current_index + 1)


def display_invalid_input(message: str) -> None:
    print(message)


def display_move_prompt() -> None:
    print("Enter your moves in the format 'A1=5, B2=3, C3=7'. To make a cell empty - 'A1=None' :")
