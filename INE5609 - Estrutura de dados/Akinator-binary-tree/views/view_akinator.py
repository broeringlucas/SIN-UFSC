
class ViewAkinator():
  # fazer aqui tratamento dos dados, caso a entrada seja diferente do esperado
  def menu_principal(self):
    print("---------------- BEM VINDO!! EU SOU O ANIMATOR ----------------")
    print("-------- VOU TENTAR ADIVINHAR O ANIMAL QUE ESTÁ PENSANDO!! ----------")
    print("1 - Jogar")
    print("2 - Carregar Jogo")
    print("0 - Sair")
 
    opcao = self.le_num_inteiro(("Escolha uma opcao: "), [1, 2, 0])
    return opcao

  def menu(self):
    print("-------- ESCOLHA UMA OPÇÃO ----------")
    print("1 - Jogar novamente")
    print("2 - Reniciar jogo (Renicia a árvore)")
    print("3 - Salvar Jogo")
    print("0 - Voltar")

    opcao = self.le_num_inteiro(("Escolha uma opcao: "), [1, 2, 3, 0])
    return opcao

  def pega_animal(self):
    animal = self.le_string("Qual animal vc pensou ? \n")

    return animal

  def qual_caracteristica(self, animal1, animal2):
    resposta =  self.le_string(f'Qual a caracteristica da/o {animal1} que se difere da/o {animal2} ? \n')

    return resposta
  
  def qual_animal(self, animal):
    resposta = self.le_sim_nao(f'O animal que vc pensou foi um/a {animal} ? (s/n) \n')

    return resposta

  def faz_pergunta(self, carac):
     resposta =self.le_sim_nao(f'O animal que vc pensou {carac} ? (s/n) \n')

     return resposta 
  
  def mostra_mensagem(self, msg):
    print(msg)

  def le_num_inteiro(self, mensagem = "", ints_validos = None):
      while True:
        valor_lido = input(mensagem)
        try:
            valor_int = int(valor_lido)
            if ints_validos and valor_int not in ints_validos:
                raise ValueError
            return valor_int
        except ValueError:
            print("Valor incorreto!! Escolha uma opção valida.")
  
  def le_string(self, mensagem): 
    while True:
        valor_lido = input(mensagem)
        try:
            if not valor_lido:
                raise ValueError
            return valor_lido
        except ValueError:
            print("Por favor, insera alguma coisa.")

  def le_sim_nao(self, mensagem): 
    while True:
        valor_lido = input(mensagem)
        try:
            if valor_lido != 's' and valor_lido != 'n': 
                raise ValueError
            return valor_lido
        except ValueError:
            print("Por favor, insera um valor valido. (s/n)")