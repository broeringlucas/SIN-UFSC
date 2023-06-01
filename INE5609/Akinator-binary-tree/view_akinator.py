
class ViewAkinator():
  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def menu_principal(self):
    print("-------- Bem vindo!! Eu sou o ANINATOR ----------")
    print("1 - Jogar")
    print("2 - Carregar Jogo")
    print("0-  Sair")

    opcao = self.le_num_inteiro(("Escolha uma opcao: "), [1, 2, 0])
    return opcao

  def menu(self):
    print("-------- ANINATOR ----------")
    print("1 - Jogar novamente")
    print("2 - Reniciar jogo")
    print("0-  Voltar")

    opcao = self.le_num_inteiro(("Escolha uma opcao: "), [1, 2, 0])
    return opcao

  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def pega_animal(self):
    animal = input("Qual animal vc pensou ? \n")

    return animal

  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def faz_pergunta(self):
     resposta =  input(f'Qual a caracteristica da/o {new_animal.animal} que se difere da/o {old_question.yesQ.animal} ? \n')

  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def seleciona_amigo(self):
    cpf = input("CPF do amigo que deseja selecionar: ")
    return cpf

  def mostra_mensagem(self, msg):
    print(msg)

  # def verificar_int(self, num):
  #   if type(num) == :
  #     return num 
  #   else:
  #     opcao = input("Opcao invalida!! Escolha outra opcao: ")
  #     return opcao 

  def le_num_inteiro(self, mensagem = "", ints_validos = None):
      while True:
        valor_lido = input(mensagem)
        try:
            valor_int = int(valor_lido)
            if ints_validos and valor_int not in ints_validos:
                raise ValueError
            return valor_int
        except ValueError:
            print("Valor incorreto!! Escolha uma opcao valida.")
            