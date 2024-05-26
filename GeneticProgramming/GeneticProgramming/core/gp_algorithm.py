from ..configuration.config import GA_PARAMETERS, DATA, VARIABLES
from .gp_core import create_expression, evaluate_expression, deviation, tournament_selection, crossover, mutate
from ..configuration.operations import ops


def run_algorithm():
    """
    Executes the genetic programming algorithm to evolve a population of expressions towards minimizing deviation from
    the provided dataset. It returns the best solutions for each generation along with their deviations.

    Returns:
        list of tuples: Each tuple contains the best expression from each generation and its deviation.
    """
    population_size = GA_PARAMETERS['population_size']
    populations_amount = GA_PARAMETERS['populations_amount']
    tournament_size = GA_PARAMETERS['tournament_size']
    max_depth = GA_PARAMETERS['max_depth']
    mutation_rate = GA_PARAMETERS['mutation_rate']
    best_candidates = GA_PARAMETERS['best_candidates']
    worst_candidates = GA_PARAMETERS['worst_candidates']

    population = [create_expression(max_depth, ops, VARIABLES) for _ in range(population_size)]
    best_solutions = []

    for generation in range(populations_amount):
        fitness_scores = [deviation(ind, DATA) for ind in population]
        sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1])

        best_individuals = sorted_population[:int(best_candidates * population_size / 100)]
        worst_individuals = sorted_population[-int(worst_candidates * population_size / 100):]

        new_population = [ind for ind, _ in best_individuals]
        while len(new_population) < population_size - len(worst_individuals):
            parent1 = tournament_selection(population, fitness_scores, tournament_size)
            parent2 = tournament_selection(population, fitness_scores, tournament_size)
            child = crossover(parent1, parent2)
            child = mutate(child, max_depth, mutation_rate, 0)
            new_population.append(child)

        new_population.extend([ind for ind, _ in worst_individuals])
        population = new_population

        best_solution = min(population, key=lambda x: deviation(x, DATA))
        best_deviation = deviation(best_solution, DATA)
        best_solutions.append((best_solution, best_deviation))

    return best_solutions
