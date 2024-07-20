def get_user_gen_input():
  """
  Busca o valor desejado de gerações do usuário, caso não seja informado o algoritmo irá executar 100 gerações.
  """
  try:
    gen = int(input("Insira a quantidade de gerações desejadas (padrão 100): "))
    if gen <= 0:
      return 100
    return gen
  except ValueError:
    return 100

def get_user_cross_input():
  """
  Busca o valor de probabilidade de cruzamento desejado caso o usuário queira customizar, por padrão o valor é 0.7 (70%).
  """
  try:
    value = int(input("Insira a probabilidade de cruzamento desejada (Valor de 0 a 1, padrão é de 0.7): "))
    if value < 0 or value > 1:
      return 0.7
    return value
  except ValueError:
    return 0.7
  
def get_user_mutaion_input():
  """
  Busca o valor de probabilidade de mutação desejado caso o usuário queira customizar, por padrão o valor é 0.2 (20%).
  """
  try:
    value = int(input("Insira a probabilidade de mutação desejada (Valor de 0 a 1, padrão é de 0.2): "))
    if value < 0 or value > 1:
      return 0.2
    return value
  except ValueError:
    return 0.2