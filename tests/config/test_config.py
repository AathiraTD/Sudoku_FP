from types import MappingProxyType

import pytest
from config.config import load_config, get_config_path


def test_load_config_valid():
    # Assuming you have a valid config file at this path
    config_path = get_config_path()
    config = load_config(config_path)
    assert isinstance(config, MappingProxyType), "Config should be an immutable dictionary"


def test_load_config_invalid_path():
    with pytest.raises(FileNotFoundError):
        load_config('invalid/path/to/config.yaml')


def test_load_config_invalid_format():
    # Create a temporary invalid config file for testing
    invalid_config_path = 'invalid_config.yaml'
    with open(invalid_config_path, 'w') as f:
        f.write("invalid_yaml: [this, is, not, valid, yaml")

    with pytest.raises(ValueError):
        load_config(invalid_config_path)
