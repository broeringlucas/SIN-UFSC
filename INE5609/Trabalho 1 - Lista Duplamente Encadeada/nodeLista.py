class NodeLista:
    def __init__(self, elemento, anterior=None, proximo=None):
        self.__elemento = elemento
        self.__anterior = anterior
        self.__proximo = proximo

    @property
    def elemento(self):
        return self.__elemento

    @property
    def anterior(self):
        return self.__anterior

    @property
    def proximo(self):
        return self.__proximo
