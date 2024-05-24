import sys
from io import StringIO

from behave import given

from user_interface.display.menu_display import display_main_menu


# Helper to capture output
def capture_output(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        func(*args, **kwargs)
        return captured_output.getvalue()
    finally:
        sys.stdout = old_stdout

@given('the user is on the main menu')
def step_given_user_on_main_menu(context):
    context.stdout = capture_output(display_main_menu)
    context.menu_output = context.stdout.split('\n')
