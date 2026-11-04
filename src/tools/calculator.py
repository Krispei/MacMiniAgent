def calculate(a: float, b: float, operation: str) -> float:
    """
    Perform basic arithmetic.

    Use whenever a user's request explicitly requests a calculation, or if the request requires an implicit calculation, or if a substep in the user's request requires a calculation.

    Args:
        a: First number.
        b: Second number.
        operation: One of 'add', 'subtract',
                   'multiply', or 'divide'.
    """
    operations = {
        "add": lambda a, b: a + b,
        "subtract": lambda a, b: a - b,
        "multiply": lambda a, b: a * b,
        "divide": lambda a, b: a / b
    }

    if operation not in operations:
        raise ValueError("Invalid operation")

    if operation == "divide" and b == 0:
        raise ValueError("Cannot divide by zero")

    return operations[operation](a, b)