import logging

from config.config import load_config, get_config_path
from user_interface.controller.main_menu_controller import menu_loop

# Configure logging to log to both console and file
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG to capture all types of log messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the log format
    handlers=[
        logging.FileHandler("error_log.txt")  # Log to a file
    ]
)


def main() -> None:
    """
    Main function to initialize configuration and start the menu loop.
    """
    try:
        config_path = get_config_path()  # Get the configuration file path
        config = load_config(config_path)  # Load the configuration settings

        menu_loop(config)  # Initial call to start the menu loop

    except Exception as e:
        logging.error("An error occurred", exc_info=True)  # Log the error to the file
        input("An error occurred. Press Enter to exit...")  # Keep the window open for the user to see the error


if __name__ == "__main__":
    main()
