from abc import ABC, abstractmethod
from animal import Animal 

class Ave(Animal): 

    @abstractmethod
    def __init__(self, tamanho_passo: int, altura_voo: int):
        super().__init__(tamanho_passo)
        if isinstance(altura_voo, int): 
            self.__altura_voo = altura_voo
    
    @property
    def altura_voo(self):
        return self.__altura_voo
    
    @altura_voo.setter
    def altura_voo(self, altura_voo: int):
        if isinstance(altura_voo, int): 
            self.__altura_voo = altura_voo

    def produzir_som(self): 
        print("AVE: PRODUZ SOM")
    
    def mover(self):
        print("ANIMAL: DESLOCOU "+self.tamanho_passo+" VOANDO")




