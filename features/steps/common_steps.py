import sys
from io import StringIO

from behave import given

from user_interface.display.menu_display import display_main_menu


@given('the game application is launched')
def step_given_game_application_is_launched(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    # Here you would initialize your game application
    display_main_menu()
    context.main_menu_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__


@given('the user is on the main menu')
def step_given_user_is_on_the_main_menu(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    display_main_menu()
    context.main_menu_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__
