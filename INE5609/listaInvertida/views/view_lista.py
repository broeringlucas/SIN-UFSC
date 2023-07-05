
class ViewListaInvertida():
  def menu_principal(self):
    print("-------- MENU PRINCIPAL ----------")
    print("1 - Menu lista")
    print("2 - Carregar Lista")
    print("0 - Sair")
 
    opcao = self.le_num_inteiro(("Escolha uma opcao: "), [1, 2, 0])
    return opcao

  def menu(self):
    print("-------- Menu lista ----------")
    print("1 - Adicionar Registro")
    print("2 - Deletar Registro")
    print("3 - Busca Simples")
    print("4 - Busca Composta")
    print("5 - Mostrar todos")
    print("6 - Salvar lista")
    print("0 - Voltar")

    opcao = self.le_num_inteiro(("Escolha uma opcao: "), [1, 2, 3, 4, 5, 6, 0])
    return opcao

  def pega_dados_registro(self):
    nome = self.le_string("Digite o nome do produto:  \n")
    tipo = self.le_string("Digite o tipo do produto:  \n")
    departamento = self.le_string("Digite o departamento do produto:  \n")
    preco = self.le_num_float("Digite o preco do produto:  \n")

    return {'nome': nome, 'tipo': tipo, 'departamento': departamento, 'preco': preco}
  
  def pega_id(self):
     id = self.le_num_inteiro("Digite o id do produto: \n")

     return id 
  
  def pega_referencia(self):
     referencia = self.le_string("Digite uma referencia para buscar: \n")

     return referencia 
  
  def menu_busca(self): 
      print("-------- Menu busca ----------")
      print("1 - Referencia normal(string)")
      print("2 - Range de valores")
      print("0 - Voltar")

      opcao = self.le_num_inteiro(("Escolha uma opcao: "), [1, 2, 0])
      return opcao

  def menu_range_valores(self):
      print("-------- Range de valores ----------")
      print("1 - Menor que 10")
      print("2 - 10 até 49.99")
      print("3 - 50 até 99.99")
      print("4 - 100 até 199.99")
      print("5 - 100 até 199.99")
      print("6 - Maior que 200")
      print("0 - Voltar")

      opcao = self.le_num_inteiro(("Escolha uma opcao: "), [1, 2, 3, 4, 5, 6, 0])
      return opcao

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

  def le_num_float(self, valor):
      while True:
        valor_lido = input(valor)
        try:
            valor_float = float(valor_lido) 
            if type(valor_float) == float:
                return valor_float
            else:
               raise ValueError
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

