import os
import sys

import pytest
from core_data.cell_value import CellValue

# Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


def test_cell_value_creation_valid():
    cell_value = CellValue(value=5, max_value=9)
    assert cell_value.value == 5, "Cell value should be 5"
    assert cell_value.max_value == 9, "Max value should be 9"


def test_cell_value_creation_none():
    cell_value = CellValue(value=None, max_value=9)
    assert cell_value.value is None, "Cell value should be None"
    assert cell_value.max_value == 9, "Max value should be 9"


def test_cell_value_invalid_value():
    with pytest.raises(ValueError):
        CellValue(value=10, max_value=9)


def test_cell_value_create_method():
    cell_value, error = CellValue.create(value=5, max_value=9)
    assert cell_value.value == 5, "Cell value should be 5"
    assert error is None, "Error should be None"

    cell_value, error = CellValue.create(value=10, max_value=9)
    assert cell_value is None, "Cell value should be None"
    assert error is not None, "Error should not be None"
