class Registro:
    def __init__(self, nome : str, tipo: str, departamento : str, preco : float):
        self.__id = 0
        self.__nome = nome
        self.__tipo = tipo  
        self.__departamento = departamento
        self.__preco = preco 

    @property
    def id(self):
        return self.__id
    
    @property
    def nome(self):
        return self.__nome

    @property
    def tipo(self):
        return self.__tipo

    @property
    def departamento(self):
        return self.__departamento
    
    @property
    def preco(self):
        return self.__preco
    
    @id.setter
    def id(self, id):
        self.__id = id