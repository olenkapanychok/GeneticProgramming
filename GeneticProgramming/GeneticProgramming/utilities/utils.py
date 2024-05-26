def expression_to_string(expression):
    """
    Converts a nested list representation of an expression into a readable string format.
    This function recursively traverses the nested list structure of an expression,
    converting it into a human-readable string format. The expression is assumed
    to be in the form of [operator, operand1, operand2], where operands can be
    either variables, constants, or other nested expressions.

    Args:
        expression (list or str): The expression to convert, represented as a
                                  nested list or a variable/constant as a string.

    Returns:
        str: A string representation of the expression, with operators and operands
             formatted in infix notation.
    """
    if not isinstance(expression, list):
        return str(expression)
    operator = expression[0]
    if len(expression) == 2:
        operand = expression_to_string(expression[1])
        return f"{operator}({operand})"
    elif len(expression) == 3:
        left = expression_to_string(expression[1])
        right = expression_to_string(expression[2])
        return f"({left} {operator} {right})"
    else:
        raise ValueError("Invalid expression format")


def trim_to_parentheses(s):
    """
    Trims a string to include only the part from the first "(" to the last ")".
    This function is useful for extracting expression-like substrings from a larger string,
    particularly when dealing with output from symbolic computation libraries or similar sources.

    Args:
        s (str): The string to trim.

    Returns:
        str: The trimmed string, or the original string if no parentheses are found.
    """
    first_open = s.find("(")
    last_close = s.rfind(")")
    if first_open != -1 and last_close != -1:
        return s[first_open:last_close + 1]
    return s