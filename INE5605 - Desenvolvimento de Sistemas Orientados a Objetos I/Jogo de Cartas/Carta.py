from AbstractCarta import *
from Personagem import *


class Carta(AbstractCarta):

    def __init__(self, personagem: Personagem):
        if isinstance(personagem, Personagem):
            self.__personagem = personagem

    def valor_total_carta(self) -> int:
        atributos = [self.__personagem.energia, self.__personagem.habilidade,
                     self.personagem.resistencia, self.personagem.velocidade]
        somatorio_atributos = 0
        for i in range(len(atributos)):
            somatorio_atributos += atributos[i]

        return somatorio_atributos

    @property
    def personagem(self) -> Personagem:
        return self.__personagem
