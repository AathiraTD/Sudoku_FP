from pytest_bdd import then


@then('the system should prompt the user to input Sudoku values')
def step_impl(context):
    # Simulate system prompting user
    context.system_prompt = "Please enter the Sudoku values"
    print(context.system_prompt)
