import logging
import sys
import os
import traceback
from user_interface.main_menu import menu_loop
from config.config import load_config, get_config_path

# Configure logging to log to both console and file
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG to capture all types of log messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the log format
    handlers=[
        # logging.StreamHandler(sys.stdout),  # Log to the console
        logging.FileHandler("error_log.txt")  # Log to a file
    ]
)


def main() -> None:
    try:
        config_path = get_config_path()  # Get the configuration file path
        config = load_config(config_path)  # Load the configuration settings

        menu_loop(config)  # Initial call to start the menu loop

    except Exception as e:
        # Log the error to both the console and the file
        logging.error("An error occurred", exc_info=True)
        input("An error occurred. Press Enter to exit...")  # Keep the window open


if __name__ == "__main__":
    main()
