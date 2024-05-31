import unittest

from core_data.cell_state import CellState


class TestCellState(unittest.TestCase):

    def test_enum_values(self):
        # Test the actual values of the enum members
        self.assertEqual(CellState.PRE_FILLED.value, "pre_filled")
        self.assertEqual(CellState.USER_FILLED.value, "user_filled")
        self.assertEqual(CellState.HINT.value, "hint")
        self.assertEqual(CellState.EMPTY.value, "empty")

    def test_enum_members(self):
        # Test that each value maps correctly to the enum member
        self.assertEqual(CellState("pre_filled"), CellState.PRE_FILLED)
        self.assertEqual(CellState("user_filled"), CellState.USER_FILLED)
        self.assertEqual(CellState("hint"), CellState.HINT)
        self.assertEqual(CellState("empty"), CellState.EMPTY)

    def test_enum_iteration(self):
        # Test that all enum members can be iterated over
        expected_members = ["pre_filled", "user_filled", "hint", "empty"]
        actual_members = [state.value for state in CellState]
        self.assertEqual(actual_members, expected_members)

    def test_enum_string_representation(self):
        # Test the string representation of enum members
        self.assertEqual(str(CellState.PRE_FILLED), "CellState.PRE_FILLED")
        self.assertEqual(str(CellState.USER_FILLED), "CellState.USER_FILLED")
        self.assertEqual(str(CellState.HINT), "CellState.HINT")
        self.assertEqual(str(CellState.EMPTY), "CellState.EMPTY")

    def test_enum_member_names(self):
        # Test the names of the enum members
        self.assertEqual(CellState.PRE_FILLED.name, "PRE_FILLED")
        self.assertEqual(CellState.USER_FILLED.name, "USER_FILLED")
        self.assertEqual(CellState.HINT.name, "HINT")
        self.assertEqual(CellState.EMPTY.name, "EMPTY")


if __name__ == '__main__':
    unittest.main()
