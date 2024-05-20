import yaml
from typing import Dict
import os

# Load configuration from YAML file
def load_config(file_path: str) -> Dict:
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing configuration file: {e}")

# Dynamically get the path to the config file
def get_config_path() -> str:
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'config.yaml')

# Get color based on state
def get_color(config, state):
    return config['color'].get(state, '\033[0m')
