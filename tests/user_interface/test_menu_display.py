from user_interface.display.menu_display import display_main_menu


def test_display_main_menu(capsys):
    display_main_menu()
    captured = capsys.readouterr()
    assert "Sudoku Main Menu" in captured.out
