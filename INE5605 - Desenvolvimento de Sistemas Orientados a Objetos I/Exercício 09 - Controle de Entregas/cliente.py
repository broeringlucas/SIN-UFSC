

class Cliente():
    def __init__(self, cpf: str, nome: str, endereco: str, telefone: str):
        if isinstance(cpf, str): 
            self.__cpf = cpf 
        if isinstance(nome, str): 
            self.__nome = nome
        if isinstance(endereco, str):
            self.__endereco = endereco
        if isinstance(telefone, str):
            self.__telefone = telefone 

    @property
    def cpf(self):
        return self.__cpf 
    
    @property
    def nome(self): 
        return self.__nome 
    
    @property
    def endereco(self): 
        return self.__endereco 
    
    @property
    def telefone(self):
        return self.__telefone 

    @cpf.setter
    def cpf(self, cpf: str):
        if isinstance(cpf, str):
            self.__cpf = cpf 
    
    @nome.setter
    def nome(self, nome: str): 
        if isinstance(nome, str): 
            self.__nome = nome 
    
    @endereco.setter
    def endereco(self, endereco: str):
        if isinstance(endereco, str):
            self.__endereco = endereco
    
    @telefone.setter
    def telefone(self, telefone: str):
        if isinstance(telefone, str):
            self.__telefone = telefone 
