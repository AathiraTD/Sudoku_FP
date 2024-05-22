import pytest

from main import main
from user_interface.display.menu_display import display_main_menu


#test main
def test_main(monkeypatch):
    def mock_input(prompt):
        return "4"  # Simulate choosing the "Exit" option

    monkeypatch.setattr('builtins.input', mock_input)
    main()
    # No assertion needed; we just want to ensure no exceptions are raised




