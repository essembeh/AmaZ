def hello_world():
    """
    some documentation here
    """
    return "Hello World =)"


def my_function(a: int, b: int, c: int):
    """
    simple addition
    """
    return a + b + c + 42


def test():
    """
    all in one test
    """
    print(hello_world(), my_function(1, 2, 3))
