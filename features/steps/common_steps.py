# features/steps/common_steps.py

def capture_output(func):
    # Example function to capture output
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output
    func()
    sys.stdout = sys.__stdout__
    return captured_output.getvalue()
