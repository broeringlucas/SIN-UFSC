from view_akinator import ViewAkinator


class NodeAnimal:
    def __init__(self, animal, yesA=None, noA=None):
        self.__animal = animal 
        self.__yesA = yesA
        self.__noA = noA 

    @property
    def animal(self):
        return self.__animal 
    
    @property
    def yesA(self):
        return self.__yesA
    
    @property
    def noA(self):
        return self.__noA

class NodeQuestion:
    def __init__(self, question, yesQ=None, noQ=None):
        self.__question = question 
        self.__yesQ = yesQ
        self.__noQ = noQ 

    @property
    def question(self):
        return self.__question
    
    @property
    def yesQ(self):
        return self.__yesQ
    
    @property
    def noQ(self):
        return self.__noQ 
    
    @yesQ.setter
    def yesQ(self, new_yesQ):
        self.__yesQ = new_yesQ

    @noQ.setter
    def noQ(self, new_noQ):
        self.__noQ = new_noQ
    
class Akinator:
    def __init__(self, root=None): 
        self.__root = root 
        self.__view_akinator = ViewAkinator() 

    @property
    def root(self):
        return self.__root 
    
    def play(self): 

        self.__view_akinator.mostra_mensagem("----- Pense em um animal -----")

        if self.__root == None: 
            self.__view_akinator.mostra_mensagem("Primeira Jogada nao conheco nenhum animal")
            animal = self.__view_akinator.pega_animal()
            new_animal = NodeAnimal(animal)
            self.__root = new_animal
            

        elif type(self.__root) == NodeAnimal: 
            old_animal = self.__root
            resposta = self.__view_akinator.qual_animal(old_animal.animal)
            # resposta = input(f'O animal que vc pensou foi um/a {old_animal.animal} ? (s/n) \n')

            if resposta == 's':
                self.__view_akinator.mostra_mensagem(f'Eu venci!! O animal que vc pensou foi um/a {old_animal.animal}.')
                # print(f'Eu venci!! O animal que vc pensou foi um/a {old_animal.animal}.')

            elif resposta == 'n':
                self.__view_akinator.mostra_mensagem("Eu desisto!! Voce venceu. Agora me diga: ")
                # print("Eu desisto!! Voce venceu. Agora me diga: ")
                animal = self.__view_akinator.pega_animal() 
                # animal = input("Qual animal vc pensou ? \n")
                new_animal = NodeAnimal(animal)
                # pergunta = input(f'Qual a caracteristica da/o {old_animal.animal} que se difere da/o {new_animal.animal} ? \n')
                pergunta = self.__view_akinator.qual_caracteristica(old_animal.animal, new_animal.animal)
                self.__root = NodeQuestion(pergunta, old_animal, new_animal)

        else:
            old_question = self.__root
            
            while True:
                    
                # respostaP = input(f'O animal que vc pensou {old_question.question} ? (s/n) \n')
                respostaP = self.__view_akinator.faz_pergunta(old_question.question)

                if respostaP == 's' and type(old_question.yesQ) == NodeAnimal:
                    # resposta = input(f'O animal que vc pensou foi um/a {old_question.yesQ.animal} ? (s/n) \n')
                    resposta = self.__view_akinator.qual_animal(old_question.yesQ.animal)

                    if resposta == 's':
                        # print(f'Eu venci!! O animal que vc pensou foi um/a {old_question.yesQ.animal}.')
                        self.__view_akinator.mostra_mensagem(f'Eu venci!! O animal que vc pensou foi um/a {old_question.yesQ.animal}.')
                        break

                    elif resposta == 'n':
                        self.__view_akinator.mostra_mensagem("Eu desisto!! Voce venceu. Agora me diga: ")
                        # print("Eu desisto!! Voce venceu. Agora me diga: ")
                        # animal = input("Qual animal vc pensou ? \n")
                        animal = self.__view_akinator.pega_animal() 
                        new_animal = NodeAnimal(animal)
                        # pergunta = input(f'Qual a caracteristica da/o {new_animal.animal} que se difere da/o {old_question.yesQ.animal} ? \n')
                        pergunta = self.__view_akinator.qual_caracteristica(new_animal.animal, old_question.yesQ.animal)
                        new_question = NodeQuestion(pergunta, new_animal, old_question.yesQ)
                        old_question.yesQ = new_question
                        break
                        
                elif respostaP == 'n' and type(old_question.noQ) == NodeAnimal:
                    # resposta = input(f'O animal que vc pensou foi um/a {old_question.noQ.animal} ? (s/n) \n')
                    resposta = self.__view_akinator.qual_animal(old_question.noQ.animal)

                    if resposta == 's':
                        # print(f'Eu venci!! O animal que vc pensou foi um/a {old_question.noQ.animal}.')
                        self.__view_akinator.mostra_mensagem(f'Eu venci!! O animal que vc pensou foi um/a {old_question.noQ.animal}.')
                        break

                    elif resposta == 'n':
                        # print("Eu desisto!! Voce venceu. Agora me diga: ")
                        self.__view_akinator.mostra_mensagem("Eu desisto!! Voce venceu. Agora me diga: ")
                        # animal = input("Qual animal vc pensou ? \n")
                        animal = self.__view_akinator.pega_animal() 
                        new_animal = NodeAnimal(animal)
                        # pergunta = input(f'Qual a caracteristica da/o {new_animal.animal} que se difere da/o {old_question.noQ.animal} ? \n')
                        pergunta = self.__view_akinator.qual_caracteristica(new_animal.animal, old_question.noQ.animal)
                        new_question = NodeQuestion(pergunta, new_animal, old_question.noQ)
                        old_question.noQ = new_question
                        break 
                
                elif respostaP == 's':
                    old_question = old_question.yesQ

                elif respostaP == 'n':
                    old_question = old_question.noQ 

        self.abre_menu() 

    
    def reniciar_jogo(self): 
        self.__root = None 
        self.play() 

    def abre_menu_principal(self):
        lista_opcoes = {1: self.play}

        continua = True
        while continua:
            lista_opcoes[self.__view_akinator.menu_principal()]()
    
    def start(self):
        self.abre_menu_principal()

    def abre_menu(self):
        lista_opcoes = {1: self.play, 2: self.reniciar_jogo, 0: self.abre_menu_principal}

        continua = True 
        while continua:
            lista_opcoes[self.__view_akinator.menu()]() 

animal1 = NodeAnimal("Baleia")
A = Akinator() 
A.start()