
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

    @property
    def root(self):
        return self.__root 
    
    def play(self): 

        print("----- Bem vindo ao Aninator -----")

        print("----- Pense em um animal -----")

        fim = True 
        partida = True 
        primeira = True 
        while partida:
        
            if self.__root == None: 
                animal = input("Qual animal vc pensou ? \n")
                new_animal = NodeAnimal(animal)
                self.__root = new_animal
                print(self.__root.animal)
                

            elif type(self.__root) == NodeAnimal: 
                old_animal = self.__root
                resposta = input(f'O animal que vc pensou foi um/a {old_animal.animal} ? (s/n) \n')

                if resposta == 's':
                    print(f'Eu venci!! O animal que vc pensou foi um/a {old_animal.animal}.')
                    # um jeito de finalizar o jogo 

                elif resposta == 'n':
                    animal = input("Qual animal vc pensou ? \n")
                    new_animal = NodeAnimal(animal)
                    pergunta = input(f'Qual a caracteristica da/o {old_animal.animal} que se difere da/o {new_animal.animal} ? \n')
                    self.__root = NodeQuestion(pergunta, old_animal, new_animal)
                    # jeito de reniciar o jogo 

            else:
                old_question = self.__root
                
                while fim:
                        
                    respostaP = input(f'O animal que vc pensou {old_question.question} ? (s/n) \n')

                    if respostaP == 's' and type(old_question.yesQ) == NodeAnimal:
                        resposta = input(f'O animal que vc pensou foi um/a {old_question.yesQ.animal} ? (s/n) \n')

                        if resposta == 's':
                            print(f'Eu venci!! O animal que vc pensou foi um/a {old_question.yesQ.animal}.')
                            break

                        elif resposta == 'n':
                            animal = input("Qual animal vc pensou ? \n")
                            new_animal = NodeAnimal(animal)
                            pergunta = input(f'Qual a caracteristica da/o {new_animal.animal} que se difere da/o {old_question.yesQ.animal} ? \n')
                            new_question = NodeQuestion(pergunta, new_animal, old_question.yesQ)
                            old_question.yesQ = new_question
                            break
                    
                    elif respostaP == 's':
                        old_question = old_question.yesQ
                          
                    elif respostaP == 'n' and type(old_question.noQ) == NodeAnimal:
                        resposta = input(f'O animal que vc pensou foi um/a {old_question.noQ.animal} ? (s/n) \n')

                        if resposta == 's':
                            print(f'Eu venci!! O animal que vc pensou foi um/a {old_question.noQ.animal}.')
                            break

                        elif resposta == 'n':
                            animal = input("Qual animal vc pensou ? \n")
                            new_animal = NodeAnimal(animal)
                            pergunta = input(f'Qual a caracteristica da/o {new_animal.animal} que se difere da/o {old_question.noQ.animal} ? \n')
                            new_question = NodeQuestion(pergunta, new_animal, old_question.noQ)
                            old_question.noQ = new_question
                            break 
                        
                    elif respostaP == 'n':
                        old_question = old_question.noQ 
                    
    def menu(self):
        print("-------- ANINATOR ----------")
        print("Escolha a opcao")
        print("1 - Jogar")
        print("2 - Carregar Jogo")
        print("0-  Sair")

        opcao = int(input("Escolha a opcao: "))

        return opcao 
    
    def abre_menu(self):
        lista_opcoes = {1: self.play}

        continua = True
        while continua:
            lista_opcoes[self.menu()]()
    
    def start(self):
        self.abre_tela() 


animal1 = NodeAnimal("Baleia")
A = Akinator(animal1) 
A.start()