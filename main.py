import sys
import os
import traceback
from user_interface.main_menu import menu_loop
from config.config import load_config, get_config_path


def main() -> None:
    """
    Main function to display the menu and start the game based on user choice.
    """
    try:
        config_path = get_config_path()  # Get the configuration file path
        config = load_config(config_path)  # Load the configuration settings

        menu_loop(config)  # Initial call to start the menu loop

    except Exception:
        # Log the error to a file and keep the window open in case of an error
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())
        input("An error occurred. Press Enter to exit...")  # Keep the window open


if __name__ == "__main__":
    main()
