from geopy.geocoders import Nominatim
import random
import numpy as np

def get_points():
  """
  Busca as coordenadas dos pontos de parada, dando a opção para o usuário para digitar os endereços e o algoritmo identificar as coordenadas, ou gerar aleatóriamente um número de endereços
  """
  value = input("Você deseja inserir manualmente os endereços? [Y/N]: ")
  if value == "y" or value == "Y":
    return _get_from_addr()
  
  try:
    number = int(input("Insira a quantidade de pontos (coordenadas) desejadas (padrão 20): "))
    if number <= 0:
      number = 20
  except ValueError:
    number = 20
  
  return _generate_random(number)

def _get_from_addr():
  """
  Permite com que o usuário insira os endereços e busca suas coordenadas.
  """
  values = []
  running = True
  loc = Nominatim(user_agent="Geopy Library")
  
  while True:
    text = "Por favor, insira um endereço (ou 'sair' para finalizar): "
    if len(values) == 0:
      text = "Por favor, insira o endereço de partida, este endereço também será para onde retornar: "
    
    address = input(text)
    if address.lower() == 'sair':
      break
    
    try:
      location = loc.geocode(address)
            
      if location:
        values.append((location.latitude, location.longitude))
        print(f"Coordenadas de '{address}': ({location.latitude}, {location.longitude})")
      else:
        print(f"Não foi possível encontrar o endereço: '{address}'")
    except Exception as e:
      print(f"Ocorreu um erro ao tentar geocodificar o endereço: {e}")
  
  return values
  
def _generate_random(amount):
  """
  Gera uma quantidade aleatória de coordenadas baseado no parâmetro desejado.
  """
  return [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(amount)] # Gera um número aleatório para a posição (x, y)

def calculate_distance_matrix(cities):
  n = len(cities)
  distance_matrix = [[0] * n for _ in range(n)]
  for i in range(n):
      for j in range(i, n):
          dist = np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))
          distance_matrix[i][j] = dist
          distance_matrix[j][i] = dist
  return distance_matrix
