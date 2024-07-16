import random
import math
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Número de gerações para limitar o algoritmo
NUMBER_OF_GENERATIONS = 100
# Probabilidade de cruzamento
CROSSOVER_PROBABILITY = 0.7
# Probabilidade de mutação
MUTATION_PROBABILITY = 0.2

# Geração da população inicial
# A função generate_cities gera coordenadas aleatórias para simular as coordenadas das cidades, de acordo com o número de cidades informadas
def generate_cities(num_cities):
  return [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(num_cities)] # Gera um número aleatório para a posição (x, y)

# A função distance calcula a distância euclidiana entre duas cidades
def distance(city1, city2):
  return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

# --

# Avaliação de Aptidão dos indivíduos
# a função evaluate serve para avaliar o fitness, ou qualidade, de uma solução proposta pelo algarismo.
# A proposta recebida é uma lista com os índices que representam uma permutação entre as cidades, ou seja, uma possibilidade de ordem de cidades para se seguir.
# A função itera sobre o conjunto de cidades e acumula suas distâncias, acumulando na variável dist.
# Ao final ele calcula e soma distância entre a última cidade e a primeira.
def evaluate(proposal):
  dist = 0
  for i in range(len(proposal) - 1):
    dist += distance(cities[proposal[i]], cities[proposal[i+1]])
  dist += distance(cities[proposal[-1]], cities[proposal[0]])
  return (dist,)

# --

# Função de suporte para uso de libs
# A função configDeap realiza a configuração da lib deap, que é um framework para facilitar a configuração e uso
# de algoritmos evolutivos, incluindo algoritmos genéticos
def configDeap():
  creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
  creator.create("Individual", list, fitness=creator.FitnessMin)
  toolbox = base.Toolbox()
  toolbox.register("indices", random.sample, range(len(cities)), len(cities))
  toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
  toolbox.register("population", tools.initRepeat, list, toolbox.individual)
  toolbox.register("mate", tools.cxOrdered)
  toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
  toolbox.register("select", tools.selTournament, tournsize=3)
  toolbox.register("evaluate", evaluate)
  return toolbox

# Função para visualizar o resultado final do algoritmo
def plot_route(cities, route):
  # Cria uma nova figura e define o tamanho
  plt.figure(figsize=(10, 6))
  # Extrai as coordenadas das cidades na ordem especificada pela rota
  x = [cities[i][0] for i in route]
  y = [cities[i][1] for i in route]
  # Adiciona a coordenada inicial no final da lista para fechar o ciclo
  x.append(x[0])
  y.append(y[0])
  # Plota a rota conectando os pontos
  plt.plot(x, y, 'o-', markersize=5)
  # Destaca o ponto inicial em verde
  plt.plot(cities[route[0]][0], cities[route[0]][1], 'go', markersize=10, label='First City')
  # Destaca o ponto final em vermelho
  plt.plot(cities[route[-1]][0], cities[route[-1]][1], 'ro', markersize=10, label='Last City')
  # Destaca os outros pontos em azul
  for i in range(1, len(route)-1):
      plt.plot(cities[route[i]][0], cities[route[i]][1], 'bo', markersize=7)
  # Adiciona título e rótulos dos eixos
  plt.title('TSP Route')
  plt.xlabel('X coordinate')
  plt.ylabel('Y coordinate')
  # Adiciona uma legenda
  plt.legend()
  # Mostra o gráfico
  plt.show()

# Função para execução do algoritmo
def run_ga(toolbox):
  population = toolbox.population(n=NUMBER_OF_GENERATIONS)
  
  for gen in range(NUMBER_OF_GENERATIONS):
    # Avaliar todos os indivíduos na população executando a função de evaluate para as possibilidades
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
      ind.fitness.values = fit
    
    # Seleção através do método configurado no DEAP
    # No caso foi configurado com o modo torneio
    offspring = toolbox.select(population, len(population))
    # Os indivíduos selecionados são clonados para passar pelo processo de mutação e cruzamento
    offspring = list(map(toolbox.clone, offspring))
    
    # Cruzamento
    # São selecionados pares de elementos, caso o número aleatório esteja dentro da probabilidade de cruzamento
    # os elementos selecionados são cruzados e possuem seus índices de fitness removidos para passarem pelo processo de seleção novamente.
    # A estratégia utilizada e configurada no DEAP foi a de "ordenação", ou ordered crossover.
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
      if random.random() < CROSSOVER_PROBABILITY:
        toolbox.mate(child1, child2)
        del child1.fitness.values
        del child2.fitness.values
    
    # Mutação
    # São percorridos os indivíduos da lista e de acordo com a probabilidade de mutação
    # os elementos selecionados são submetidos ao processo de mutação configurado no DEAP
    # neste caso foi configurada uma estratégia de shuffle, na qual embaralha os indíces do gene selecionado
    # e ao final do processo possuem seu índice de fitness removido para serem selecionados novamente
    for mutant in offspring:
      if random.random() < MUTATION_PROBABILITY:
        toolbox.mutate(mutant)
        del mutant.fitness.values
        
    # Avaliar os indivíduos com fitness inválido
    # é realizada uma verificação para garantir que todos os genes possuem fitness válido
    # para os casos dos indivíduos que passaram pela mutação ou cruzamento e tiveram seu fitness invalidado
    # ele é calculado novamente
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
      ind.fitness.values = fit
      
    # Substituir a população atual pela nova geração
    population[:] = offspring

    # Registro e impressão da melhor solução encontrada até agora
    # Este trecho de código calcula e imprime estatísticas da população em uma determinada geração. 
    # As estatísticas incluem o valor mínimo, máximo, médio e o desvio padrão dos fitnesses dos indivíduos na população.
    fits = [ind.fitness.values[0] for ind in population]
    length = len(population)
    mean = sum(fits) / length
    sum2 = sum(x*x for x in fits)
    std = abs(sum2 / length - mean**2)**0.5
    
    print(f"{gen + 1}º Generation: Min {min(fits)}, Max {max(fit)}, Avg {mean}, Std {std}")
    
  # Melhor indivíduo encontrado após as gerações
  best_ind = tools.selBest(population, 1)[0]
  print(f"Melhor rota: {best_ind}")
  print(f"Distância: {evaluate(best_ind)[0]}")
  return list(best_ind)

# Startup do algoritmo
num_cities = 20
cities = generate_cities(num_cities)
toolbox = configDeap()
best_ind = run_ga(toolbox)
plot_route(cities, best_ind)