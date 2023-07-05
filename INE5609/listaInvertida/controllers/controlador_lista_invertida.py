import pickle


from models.registro import Registro
from models.lista_invertida import ListaInvertida
from views.view_lista import ViewListaInvertida


class ControladorListaInvertida: 
    def __init__(self): 
        self.__view_lista_invertida = ViewListaInvertida() 
        self.__lista_invertida = ListaInvertida() 

    def abre_menu_principal(self):
        lista_opcoes = {1: self.abre_menu_lista, 2: self.carregar, 0: self.sair}

        continua = True
        while continua:
            lista_opcoes[self.__view_lista_invertida.menu_principal()]()

    def abre_menu_lista(self):
        lista_opcoes = {1: self.add_registro, 2: self.del_registro, 3: self.busca_simples, 4: self.busca_composta, 5: self.__lista_invertida.mostrar_todos, 6: self.salvar, 0: self.abre_menu_principal}

        continua = True 
        while continua:
            lista_opcoes[self.__view_lista_invertida.menu()]() 
    
    def add_registro(self): 
        dados_registro = self.__view_lista_invertida.pega_dados_registro() 
        registro = Registro(dados_registro['nome'], dados_registro['tipo'], dados_registro['departamento'], dados_registro['preco'])
        self.__lista_invertida.add_registro(registro)

    def del_registro(self):
        id = self.__view_lista_invertida.pega_id() 
        self.__lista_invertida.del_registro(id)
    
    def abre_menu_busca(self):
        lista_opcoes = {1: self.__view_lista_invertida.pega_referencia, 2: self.busca_range_valores, 0: self.abre_menu_lista}

        while True:
            opcao = self.__view_lista_invertida.menu_busca()
            if opcao in lista_opcoes:
                referencia = lista_opcoes[opcao]()
                return referencia
    
    def busca_simples(self):
        referencia = self.abre_menu_busca()
        self.__lista_invertida.busca_simples(referencia) 

    def busca_range_valores(self):
        index = self.__view_lista_invertida.menu_range_valores() - 1 
        ranges = ['Menor que 10','10 até 49.99', '50 até 99.99', '100 até 199.99', '100 até 199.99', 'Maior que 200']
        return ranges[index]
    
    def busca_composta(self): 
        referencia1 = self.abre_menu_busca()
        self.__view_lista_invertida.mostra_mensagem("Escolha um segundo paramêtro para a busca \n")
        referencia2 = self.abre_menu_busca()
        self.__lista_invertida.busca_composta(referencia1, referencia2) 

    def salvar(self):
        self.__view_lista_invertida.mostra_mensagem("Save completo!!")
        with open('lista_invertida', 'wb') as file:
            pickle.dump(self.__lista_invertida, file)

    def carregar(self):
        try:
            with open('lista_invertida', 'rb') as file:
                lista_carregada = pickle.load(file)

            self.__view_lista_invertida.mostra_mensagem("Lista carregada com sucesso!!")
            self.__lista_invertida = lista_carregada
        except FileNotFoundError:
            self.__view_lista_invertida.mostra_mensagem("Nenhuma lista encontrada para carregar!!")

    def sair(self):
        exit(0) 

        