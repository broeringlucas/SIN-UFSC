from mamifero import Mamifero

class Cachorro(Mamifero): 
    
    def __init__(self, volume_som = 3, tamanho_passo = 3): 
        super().__init__(volume_som, tamanho_passo)

    def latir(self): 
        print("MAMIFERO: PRODUZ SOM: ",self.volume_som," SOM: AU")


cao = Cachorro()
cao.latir() 
cao.mover() 




