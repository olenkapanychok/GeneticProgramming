import matplotlib.pyplot as plt
import numpy as np
from ..core.gp_core import evaluate_expression


def plot_fitness_over_generations(best_solutions):
    """
    Plots the fitness (deviation) of the best solutions over generations.

    Args:
        best_solutions (list of tuples): Each tuple contains the best expression and its deviation for each generation.
    """
    generations = np.arange(1, len(best_solutions) + 1)
    deviations = [solution[1] for solution in best_solutions]

    plt.figure(figsize=(10, 5))
    plt.plot(generations, deviations, marker='o', linestyle='-', color='blue')
    plt.title('Fitness Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Deviation (Lower is better)')
    plt.grid(True)
    plt.show()


def plot_expression_over_data(expression, data, variables):
    """
    Plots the result of a genetic expression over the actual data points.

    Args:
        expression (list or str): The genetic expression to evaluate.
        data (list of tuples): Data points, each a tuple of (input values, expected output).
        variables (list of str): The variable names corresponding to input values in data.
    """
    if len(data[0][0]) == 1:
        x_vals, y_vals = zip(*[(inputs[0], output) for inputs, output in data])
        x_vals = np.array(x_vals)
        y_vals = np.array(y_vals)

        x_line = np.linspace(min(x_vals), max(x_vals), 300)
        y_line = np.array([evaluate_expression(expression, {variables[0]: x}) for x in x_line])

        plt.figure(figsize=(10, 5))
        plt.scatter(x_vals, y_vals, color='red', label='Actual Data')
        plt.plot(x_line, y_line, color='blue', label='GP Approximation')
        plt.title('Expression Fit to Data')
        plt.xlabel('Input')
        plt.ylabel('Output')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print("Multi-dimensional data visualization not implemented.")