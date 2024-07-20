# pip install geopy
# pip install deap
# pip install scipy
# pip install matplotlib
# pip install numpy
from genetic_algorithm import configDeap, run_ga
from startup import get_user_gen_input, get_user_cross_input, get_user_mutaion_input

NUMBER_OF_GENERATIONS = get_user_gen_input()
CROSSOVER_PROBABILITY = get_user_cross_input()
MUTATION_PROBABILITY = get_user_mutaion_input()

toolbox = configDeap()
run_ga(toolbox, NUMBER_OF_GENERATIONS, CROSSOVER_PROBABILITY, MUTATION_PROBABILITY)