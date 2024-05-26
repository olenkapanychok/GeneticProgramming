import random
import numpy as np
from ..configuration.config import VARIABLES
from ..configuration.operations import ops, safe_sqr


def create_expression(max_depth, operations, variables):
    """
    Recursively creates a random function from the available operations and variables.
    The depth of the tree determines the complexity of the function generated.

    Args:
        max_depth (int): The maximum depth of the expression tree.
        operations (dict): A dictionary of available operations.
        variables (list): A list of variable names that can be used in the expression.

    Returns:
        list or str: A nested list representing the expression, or a single variable/constant.
    """
    if max_depth == 1 or (variables and random.random() > 0.5):
        return random.choice(variables)
    operation = random.choices(list(operations.keys()), weights=[operations[op]['weight'] for op in operations], k=1)[0]
    operands = [create_expression(max_depth - 1, operations, variables) for _ in range(operations[operation]['arity'])]
    return [operation] + operands


def evaluate_expression(expression, input_variables):
    """
    Evaluates an expression based on the provided input variables.

    Args:
        expression (list or str): The expression to evaluate, either a nested list or a variable name.
        input_variables (dict): A dictionary mapping variable names to their values.

    Returns:
        float: The result of the evaluated expression.
    """
    if isinstance(expression, str):
        return input_variables.get(expression, 0)
    operation = ops[expression[0]]['func']
    evaluated_operands = [evaluate_expression(arg, input_variables) for arg in expression[1:]]

    expected_args = ops[expression[0]]['arity']
    if len(evaluated_operands) != expected_args:
        raise ValueError(f"Operation {expression[0]} expected {expected_args} operands, got {len(evaluated_operands)}")

    return operation(*evaluated_operands)


def deviation(expression, data):
    """
    Calculates the deviation of an expression from provided data using the sum of squared errors.

    Args:
        expression (list): The expression to evaluate.
        data (list of tuples): Data points, each a tuple of (input values, expected output).

    Returns:
        float: The root-mean-square error of the expression across all data points.
    """
    total_error = sum(safe_sqr(evaluate_expression(expression, dict(zip(VARIABLES, inputs))) - output)
                      for inputs, output in data)
    return np.sqrt(total_error / len(data))


def tournament_selection(population, deviations, tournament_size):
    """
    Selects an individual from the population using tournament selection.

    Args:
        population (list): The current population of individuals.
        deviations (list): Corresponding fitness values for the population.
        tournament_size (int): The number of individuals to include in each tournament.

    Returns:
        list: The winning individual from the tournament.
    """
    selected_indices = random.sample(range(len(population)), tournament_size)
    best_index = min(selected_indices, key=lambda idx: deviations[idx])
    return population[best_index]


def crossover(parent1, parent2):
    """
    Performs crossover between two parent expressions to create a child expression.

    Args:
        parent1, parent2 (list): Parent expressions.

    Returns:
        list: A new child expression resulting from crossover.
    """
    if not isinstance(parent1, list) or not isinstance(parent2, list):
        return random.choice([parent1, parent2])
    if len(parent1) > 1 and len(parent2) > 1:
        valid_points = [i for i in range(1, min(len(parent1), len(parent2))) if
                        isinstance(parent1[i], list) and isinstance(parent2[i], list)]
        if valid_points:
            crossover_point = random.choice(valid_points)
            return parent1[:crossover_point] + parent2[crossover_point:]
    return random.choice([parent1, parent2])


def mutate(expression, max_depth, mutation_rate, depth = 0):
    """
    Mutates an expression with a given probability at each node.

    Args:
        expression (list): The expression to mutate.
        max_depth (int): The maximum depth for newly generated expressions.
        mutation_rate (float): The mutation rate.

    Returns:
        list: The mutated expression.
    """
    if random.random() < mutation_rate:
        if isinstance(expression, list) and depth < max_depth:
            operation = expression[0]
            required_arity = ops[operation]['arity']
            new_args = [
                mutate(create_expression(max_depth - depth - 1, ops, VARIABLES), max_depth, mutation_rate, depth + 1)
                for _ in range(required_arity)]
            return [operation] + new_args
        else:
            return create_expression(max_depth - depth, ops, VARIABLES)
    if isinstance(expression, list):
        return [expression[0]] + [mutate(arg, max_depth, mutation_rate, depth + 1) for arg in expression[1:]]
    return expression