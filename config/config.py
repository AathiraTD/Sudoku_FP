import yaml
from typing import Dict
from types import MappingProxyType
import os


def load_config(file_path: str) -> Dict:
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            return MappingProxyType(config)  # Make the configuration immutable
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing configuration file: {e}")


def get_config_path() -> str:
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'config.yaml')
