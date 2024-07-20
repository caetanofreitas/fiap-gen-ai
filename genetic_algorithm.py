from get_points import get_points, calculate_distance_matrix
from deap import base, creator, tools, algorithms
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import random

cities = get_points()
distance_matrix = calculate_distance_matrix(cities)

def configDeap():
  """
  Função de suporte para uso de libs;
  A função configDeap realiza a configuração da lib deap, que é um framework para facilitar a configuração e uso de algoritmos evolutivos, incluindo algoritmos genéticos.
  """
  creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
  creator.create("Individual", list, fitness=creator.FitnessMin)
  toolbox = base.Toolbox()
  toolbox.register("indices", random.sample, range(len(cities)), len(cities))
  # Cria População Inicial
  toolbox.register("individual", tools.initIterate, creator.Individual, _create_individual)
  toolbox.register("population", tools.initRepeat, list, toolbox.individual)
  # Define método de cruzamento
  toolbox.register("mate", tools.cxOrdered)
  # Define método de mutação
  toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
  # Define método de seleção
  toolbox.register("select", tools.selTournament, tournsize=3)
  # Define método de fitness
  toolbox.register("evaluate", _evaluate)
  return toolbox

def _create_individual():
  """
  Registro da função de criação de indivíduo utilizando Convex Hull
  """
  return _convex_hull_route(cities, distance_matrix)

def _convex_hull_route(cities, distance_matrix):
  hull = ConvexHull(cities)
  hull_indices = hull.vertices.tolist()
  remaining_indices = [i for i in range(len(cities)) if i not in hull_indices]
  
  # Inicializa a rota com os índices dos pontos do Convex Hull
  route = hull_indices[:]
  
  # Adiciona os pontos restantes de forma sequencial (ou usa outra heurística)
  for point_index in remaining_indices:
      min_distance = float('inf')
      best_position = 0
      for i in range(len(route)):
          distance = (
              distance_matrix[route[i]][point_index] +
              distance_matrix[point_index][route[(i+1) % len(route)]] -
              distance_matrix[route[i]][route[(i+1) % len(route)]]
          )
          if distance < min_distance:
              min_distance = distance
              best_position = i + 1
      route.insert(best_position, point_index)
  
  return route

def _evaluate(individual):
  """
  Avaliação de Aptidão dos indivíduos a função evaluate serve para avaliar o fitness, ou qualidade, de uma solução proposta pelo algarismo.
  A proposta recebida é uma lista com os índices que representam uma permutação entre as cidades, ou seja, uma possibilidade de ordem de cidades para se seguir.
  A função itera sobre o conjunto de cidades e acumula suas distâncias, acumulando na variável dist.
  Ao final ele calcula e soma distância entre a última cidade e a primeira.
  """
  distance = 0
  for i in range(len(individual) - 1):
      distance += distance_matrix[individual[i]][individual[i + 1]]
  distance += distance_matrix[individual[-1]][individual[0]]  # Retorna ao ponto inicial
  return (distance,)

def run_ga(toolbox, maxGen, crossProb, mutProb):
  population = toolbox.population(n=100)
  gen = 1
  
  while True:
    if gen > maxGen:
      break
    
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
      if random.random() < crossProb:
        toolbox.mate(child1, child2)
        del child1.fitness.values
        del child2.fitness.values
        
    # Mutação
    # São percorridos os indivíduos da lista e de acordo com a probabilidade de mutação
    # os elementos selecionados são submetidos ao processo de mutação configurado no DEAP
    # neste caso foi configurada uma estratégia de shuffle, na qual embaralha os indíces do gene selecionado
    # e ao final do processo possuem seu índice de fitness removido para serem selecionados novamente
    for mutant in offspring:
      if random.random() < mutProb:
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
    
    print(f"{gen}º Generation: Min {min(fits)}, Max {max(fit)}, Avg {mean}, Std {std}")
    gen = gen + 1

  # Melhor indivíduo encontrado após as gerações
  best_ind = tools.selBest(population, 1)[0]
  print(f"Melhor rota: {best_ind}")
  print(f"Distância: {_evaluate(best_ind)[0]}")
  plot_route(list(best_ind))
  
def plot_route(route):
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
  plt.plot(cities[route[0]][0], cities[route[0]][1], 'go', markersize=10, label='First Point')
  # Destaca o ponto final em vermelho
  plt.plot(cities[route[-1]][0], cities[route[-1]][1], 'ro', markersize=10, label='Last Point')
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
