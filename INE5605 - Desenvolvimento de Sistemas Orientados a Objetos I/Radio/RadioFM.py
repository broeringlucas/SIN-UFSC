class RadioFM:
    
    def __init__(self, ligado:bool, nome:str, frequencia:float):
        self.__ligado = ligado
        self.__nome = nome
        self.__frequencia = frequencia 

        if not 87.5 <= frequencia <= 108.0: 
            print("Frequencia Invalida. Selecione uma frequencia entre 87,5 MHz e 108,0 MHz")
    
    @property
    def ligado(self):
        return self.__ligado

    @ligado.setter
    def ligado(self, ligado:bool):
        self.__ligado = ligado 

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome:str):
        self.__nome = nome

    @property
    def frequencia(self):
        return self.__frequencia

    @frequencia.setter
    def ligado(self, frequencia:float):
        self.__frequencia = frequencia









