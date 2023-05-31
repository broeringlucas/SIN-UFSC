
class ViewAkinator():
  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def tela_opcoes(self):
    print("-------- ANINATOR ----------")
    print("Escolha a opcao")
    print("1 - Jogar")
    print("2 - Carregar Jogo")
    print("0- Sair")

    opcao = int(input("Escolha a opcao: "))
    return opcao

  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def pega_animal(self):
    animal = input("Qual animal vc pensou ? \n")

    return animal

  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def mostra_amigo(self, dados_amigo):
    print("NOME DO AMIGO: ", dados_amigo["nome"])
    print("FONE DO AMIGO: ", dados_amigo["telefone"])
    print("CPF DO AMIGO: ", dados_amigo["cpf"])
    print("\n")

  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def seleciona_amigo(self):
    cpf = input("CPF do amigo que deseja selecionar: ")
    return cpf

  def mostra_mensagem(self, msg):
    print(msg)