from abc import ABC, abstractmethod
from abstractPessoa import AbstractPessoa


class Pessoa(AbstractPessoa, ABC):
    def __init__(self, nome: str, codigo: int):
        if isinstance(nome, str): 
            self.__nome = nome 
        if isinstance(codigo, str): 
            self.__codigo = codigo 

    @property
    def nome(self): 
        return self.__nome
    
    @property
    def codigo(self): 
        return self.__codigo 