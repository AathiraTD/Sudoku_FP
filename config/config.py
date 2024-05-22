import yaml
from typing import Dict
from types import MappingProxyType
import os


def load_config(file_path: str) -> Dict:
    try:
        # Open the configuration file in read mode
        with open(file_path, 'r') as file:
            # Parse the YAML file using the safe_load function from the yaml library
            config = yaml.safe_load(file)

        # Convert the loaded configuration to an immutable dictionary.
        # This ensures that the configuration cannot be modified after loading
        return dict(config)

    except FileNotFoundError:
        # If the specified configuration file is not found, raise a FileNotFoundError
        # with a custom error message
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")

    except yaml.YAMLError as e:
        # If there is an error parsing the YAML file (e.g., syntax error, invalid data)
        # raise a ValueError with a custom error message that includes the specific error
        raise ValueError(f"Error parsing configuration file: {e}")


def get_config_path() -> str:
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'config.yaml')
