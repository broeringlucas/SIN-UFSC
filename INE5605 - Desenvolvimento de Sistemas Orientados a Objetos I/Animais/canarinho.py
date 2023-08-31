from ave import Ave 

class Canarinho(Ave): 
    
    def __init__(self, tamanho_passo: int, altura_voo: int): 
        super().__init__(tamanho_passo, altura_voo)

    def cantar(self):
        print("AVE: PRODUZ SOM: PIU")

canarinho1 = Canarinho("3", "1") 
canarinho1.cantar() 
canarinho1.mover() 

