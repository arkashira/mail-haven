"""
A dummy test suite to guarantee that pytest discovers and runs at least one test.
"""

def test_placeholder_function():
    """
    Ensure that the placeholder function from the package returns the expected string.
    """
    from axentx_product import placeholder

    assert placeholder() == "axentx placeholder"
