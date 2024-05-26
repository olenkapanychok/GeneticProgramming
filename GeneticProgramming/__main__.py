import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

from GeneticProgramming.configuration.config import DATA, VARIABLES
from GeneticProgramming.core.gp_algorithm import run_algorithm
from GeneticProgramming.utilities.utils import expression_to_string
from GeneticProgramming.visualization.visualization import plot_fitness_over_generations, plot_expression_over_data


def calculate_averages(data):
    sums = {var: 0 for var in VARIABLES if var not in ['x', 'y']}
    counts = {var: 0 for var in VARIABLES if var not in ['x', 'y']}
    for entry in data:
        for i, var in enumerate(VARIABLES):
            if var not in ['x', 'y']:
                sums[var] += entry[0][i]
                counts[var] += 1
    return {var: sums[var] / counts[var] for var in sums}

def main():
    print("Running Genetic Programming Algorithm...")
    best_solutions = run_algorithm()

    best_solution_expression, best_solution_deviation = best_solutions[-1]

    full_expression = sp.simplify(sp.parse_expr(expression_to_string(best_solution_expression)))
    print("\nBest solution found:", full_expression)

    averages = calculate_averages(DATA)
    expression_sympy = sp.simplify(sp.parse_expr(expression_to_string(best_solution_expression)))

    for var, avg in averages.items():
        expression_sympy = expression_sympy.subs(var, avg)

    print("Expression (with averages substituted):", expression_sympy)
    print("Deviation:", best_solution_deviation)

    x_range = np.linspace(min(entry[0][0] for entry in DATA), max(entry[0][0] for entry in DATA), 100)
    y_range = np.linspace(min(entry[0][1] for entry in DATA), max(entry[0][1] for entry in DATA), 100)
    X, Y = np.meshgrid(x_range, y_range)
    Z = np.array([[float(expression_sympy.subs({'x': x, 'y': y}).evalf()) for x in x_range] for y in y_range])
    Z = np.nan_to_num(Z)

    plt.figure(figsize=(10, 8))
    plt.contourf(X, Y, Z, levels=50, cmap='viridis')
    plt.colorbar().set_label('SO2 Concentration')
    plt.title('Predicted SO2 Concentration Distribution')
    plt.xlabel('X Coordinate (km)')
    plt.ylabel('Y Coordinate (km)')
    plt.grid(True)
    plt.show()

    R = np.sqrt(X**2 + Y**2).ravel()
    Z = Z.ravel()
    indices = np.argsort(R)
    R_sorted = R[indices]
    Z_sorted = Z[indices]
    bins = np.linspace(R_sorted.min(), R_sorted.max(), 100)
    digitized = np.digitize(R_sorted, bins)
    R_binned = [R_sorted[digitized == i].mean() for i in range(1, len(bins))]
    Z_binned = [Z_sorted[digitized == i].mean() for i in range(1, len(bins))]

    plt.figure(figsize=(10, 6))
    plt.plot(R_binned, Z_binned, label='Average SO2 Concentration vs. Radial Distance')
    plt.xlabel('Distance from Factory (km)')
    plt.ylabel('SO2 Concentration')
    plt.title('SO2 Concentration vs. Distance from Source')
    plt.legend()
    plt.grid(True)
    plt.show()

    plot_fitness_over_generations(best_solutions)

if __name__ == "__main__":
    main()