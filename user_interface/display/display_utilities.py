import os
import sys


def clear_screen() -> None:
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Mac and Linux
        os.system('clear')
    if sys.stdout.isatty():
        print("\033[H\033[J", end='')  # ANSI escape sequences for terminals
    else:
        print("\n" * 100)  # Fallback for IDEs like PyCharm


