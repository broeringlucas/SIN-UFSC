from RadioFM import RadioFM 

class MudaFrequencia(RadioFM):

    def __init__(self, ligado:bool, nome:str, frequencia:float): 
        super().__init__(ligado, nome, frequencia)

    def down(self): 
        self._RadioFM__frequencia -= 0.01 
    
    def up(self): 
        self._RadioFM__frequencia += 0.01 

    
