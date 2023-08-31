from mamifero import Mamifero

class Gato(Mamifero): 
    
    def __init__(self, volume_som = 2, tamanho_passo = 2): 
        super().__init__(volume_som, tamanho_passo)

    def miar(self):
        print("MAMIFERO: PRODUZ SOM: ",self.volume_som," SOM: MIAU")

gato1 = Gato()
gato1.miar() 
gato1.mover() 
