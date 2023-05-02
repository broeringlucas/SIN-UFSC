# Importando duas classes de exceção e a classe nó da lista
from listaCheiaException import ListaCheia
from listaVaziaException import ListaVazia
from nodeLista import NodeLista

# Criando a classe lista duplamente encadeada


class ListaDuplamenteEncadeada:
    def __init__(self, tamanho):
        self.__tamanho = tamanho
        self.__inicio = None
        self.__fim = None
        self.__num_elementos = 0
        self.__cursor = None

    @property
    def tamanho(self):
        return self.__tamanho

    @property
    def inicio(self):
        return self.__inicio

    @property
    def fim(self):
        return self.__fim

    @property
    def num_elementos(self):
        return self.__num_elementos

    @property
    def cursor(self):
        return self.__cursor

# Dois métodos que retornam bool, para verificar se a lista está vazia ou cheia
    def Vazia(self):
        return self.__num_elementos == 0

    def Cheia(self):
        return self.__num_elementos == self.__tamanho

# Métodos privados que auxiliam na implementação dos outros
    def __irParaPrimeiro(self):
        self.__cursor = self.__inicio

    def __irParaUltimo(self):
        self.__cursor = self.__fim

    def __avancarKPosicoes(self, k):
        if k < 0 or k - 1 > self.__num_elementos:
            raise ValueError(
                "Não foi possivel avançar. Lista não tem tantos elementos")
        else:
            for _ in range(k - 1):
                self.__cursor = self.__cursor.__proximo

    def __retrocederKPosicoes(self, k):
        if k < 0 or k - 1 > self.__num_elementos:
            raise ValueError(
                "Não foi possivel retroceder. Lista não tem tantos elementos")
        else:
            for _ in range(k - 1):
                self.__cursor = self.__cursor.__anterior

    def __SoUmElemento(self):
        self.__inicio = None
        self.__fim = None
        self.__cursor = None

    def __PrimeiraInserção(self, node):
        self.__inicio = node
        self.__fim = node
        self.__cursor = node

    def __posicaoDe(self, chave):
        cont_pos = 0
        self.__irParaPrimeiro()
        encontrado = False
        while self.__cursor.elemento != None:
            if self.__cursor.elemento == chave or self.__fim == chave:
                encontrado = True
                return cont_pos + 1
            elif self.__cursor == self.__fim:
                break
            self.__cursor = self.__cursor.__proximo
            cont_pos += 1
        if not encontrado:
            print("Elemento não encontrado!!")

# Método que retorna o elemento atual do cursor
    def acessarAtual(self):
        return self.__cursor.elemento

# Métodos de inserir, conforme está no enunciado do trabalho
    def inserirAntesDoAtual(self, dado):
        if self.Cheia():
            raise ListaCheia
        novo = NodeLista(dado)
        if self.Vazia():
            self.__PrimeiraInserção(novo)
        else:
            if self.__cursor == self.__inicio:
                novo.__proximo = self.__cursor
                self.__cursor.__anterior = novo
                self.__inicio = novo
            else:
                novo.__proximo = self.__cursor
                novo.__anterior = self.__cursor.__anterior
                self.__cursor.__anterior.__proximo = novo
                self.__cursor.__anterior = novo
        self.__num_elementos += 1
        self.__cursor = novo

    def inserirAposAtual(self, dado):
        if self.Cheia():
            raise ListaCheia
        novo = NodeLista(dado)
        if self.Vazia():
            self.__PrimeiraInserção(novo)
        else:
            if self.__cursor == self.__fim:
                novo.__anterior = self.__cursor
                self.__cursor.__proximo = novo
                self.__fim = novo
            else:
                novo.__anterior = self.__cursor
                novo.__proximo = self.__cursor.__proximo
                self.__cursor.__proximo.__anterior = novo
                self.__cursor.__proximo = novo
        self.__num_elementos += 1
        self.__cursor = novo

    def inserirComoUltimo(self, dado):
        if self.Cheia():
            raise ListaCheia
        novo = NodeLista(dado)
        self.__irParaUltimo()
        if self.Vazia():
            self.__PrimeiraInserção(novo)
        else:
            novo.__anterior = self.__cursor
            self.__cursor.__proximo = novo
            self.__fim = novo
        self.__num_elementos += 1
        self.__cursor = novo

    def inserirComoPrimeiro(self, dado):
        if self.Cheia():
            raise ListaCheia
        novo = NodeLista(dado)
        self.__irParaPrimeiro()
        if self.Vazia():
            self.__PrimeiraInserção(novo)
        else:
            novo.__proximo = self.__cursor
            self.__cursor.__anterior = novo
            self.__inicio = novo
        self.__num_elementos += 1
        self.__cursor = novo

    def inserirNaPosicaoK(self, dado, k):
        if self.Cheia():
            raise ListaCheia
        novo = NodeLista(dado)
        if k == 1:
            self.inserirComoPrimeiro(dado)
        elif k - 1 == self.__num_elementos:
            self.inserirComoUltimo(dado)
        else:
            self.__irParaPrimeiro()
            self.__avancarKPosicoes(k)
            novo.__proximo = self.__cursor
            novo.__anterior = self.__cursor.__anterior
            self.__cursor.__anterior.__proximo = novo
            self.__cursor.__anterior = novo
            self.__num_elementos += 1
            self.__cursor = novo

# Esses dois métodos imprimem os elementos da lista, o primeiro impreme na ordem correta e o segundo em ordem inversa
    def imprimirElementosDaLista(self):
        if self.Vazia():
            raise ListaVazia
        cursor_print = self.__inicio
        for _ in range(self.__num_elementos - 1):
            print(cursor_print.elemento, end=' ')
            cursor_print = cursor_print.__proximo
        print(cursor_print.elemento)

    def imprimirElementosInvertido(self):
        if self.Vazia():
            raise ListaVazia
        cursor_print = self.__fim
        for _ in range(self.__num_elementos - 1):
            print(cursor_print.elemento, end=' ')
            cursor_print = cursor_print.__anterior
        print(cursor_print.elemento)

# Métodos que excluem elementos, conforme está no enunciado do trabalho
    def excluirAtual(self):
        if self.Vazia():
            raise ListaVazia
        if self.__num_elementos == 1:
            self.__SoUmElemento()
        elif self.__cursor == self.__inicio:
            self.__inicio = self.__cursor.__proximo
            self.__cursor = self.__cursor.__proximo
        elif self.__cursor == self.__fim:
            self.__fim = self.__cursor.__anterior
            self.__cursor = self.__cursor.__anterior
        else:
            self.__cursor.__anterior.__proximo = self.__cursor.__proximo
            self.__cursor.__proximo.__anterior = self.__cursor.__anterior
            self.__cursor = self.__cursor.__proximo

        self.__num_elementos -= 1

    def excluirPrimeiro(self):
        if self.Vazia():
            raise ListaVazia
        if self.__num_elementos == 1:
            self.__SoUmElemento()
        else:
            self.__irParaPrimeiro()
            self.__inicio = self.__cursor.__proximo
            self.__cursor = self.__cursor.__proximo

        self.__num_elementos -= 1

    def excluirUltimo(self):
        if self.Vazia():
            raise ListaVazia
        if self.__num_elementos == 1:
            self.__SoUmElemento()
        else:
            self.__irParaUltimo()
            self.__fim = self.__cursor.__anterior
            self.__cursor = self.__cursor.__anterior

        self.__num_elementos -= 1

    def excluirElem(self, chave):
        if self.Vazia():
            raise ListaVazia
        k = self.__posicaoDe(chave)
        if self.__num_elementos == 1:
            self.__SoUmElemento()
        elif k == 1:
            self.excluirPrimeiro()
        elif k == self.__num_elementos:
            self.excluirUltimo()
        else:
            self.__irParaPrimeiro()
            self.__avancarKPosicoes(k)
            self.__cursor.__anterior.__proximo = self.__cursor.__proximo
            self.__cursor.__proximo.__anterior = self.__cursor.__anterior
            self.__cursor = self.__cursor.__proximo
            self.__num_elementos -= 1

    def excluirDaPos(self, k):
        if self.Vazia():
            raise ListaVazia
        if self.__num_elementos == 1:
            self.__SoUmElemento()
        elif k == 1:
            self.excluirPrimeiro()
        elif k == self.__num_elementos:
            self.excluirUltimo()
        else:
            self.__irParaPrimeiro()
            self.__avancarKPosicoes(k)
            self.__cursor.__anterior.__proximo = self.__cursor.__proximo
            self.__cursor.__proximo.__anterior = self.__cursor.__anterior
            self.__cursor = self.__cursor.__proximo
            self.__num_elementos -= 1

# Método que busca na lista, e retorna True se o elemento está na lista e False se não está
    def buscar(self, chave):
        k = self.__posicaoDe(chave)
        if k != None:
            print("Elemento encontrado!!")
            return True
        else:
            return False
