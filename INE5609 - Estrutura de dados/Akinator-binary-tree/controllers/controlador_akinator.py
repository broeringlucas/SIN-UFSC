import pickle

from views.view_akinator import ViewAkinator
from models.node_animal import NodeAnimal 
from models.node_question import NodeQuestion
from models.akinator_tree import AkinatorTree


class ControladorAkinator: 
    def __init__(self): 
          self.__view_akinator = ViewAkinator() 
          self.__jogo = AkinatorTree() 

    def play(self): 

        self.__view_akinator.mostra_mensagem("----- Pense em um animal -----")
        

        if self.__jogo.root == None: 
            self.__view_akinator.mostra_mensagem("Primeira jogada não conheço nenhum animal")
            animal = self.__view_akinator.pega_animal()
            new_animal = NodeAnimal(animal)
            self.__jogo.root = new_animal
        

        elif type(self.__jogo.root) == NodeAnimal: 
            old_animal = self.__jogo.root
            resposta = self.__view_akinator.qual_animal(old_animal.animal)

            if resposta == 's':
                self.__view_akinator.mostra_mensagem(f'Eu venci!! O animal que vc pensou foi um/a {old_animal.animal}.')

            elif resposta == 'n':
                self.__view_akinator.mostra_mensagem("Eu desisto!! Você venceu. Agora me diga: ")
                animal = self.__view_akinator.pega_animal() 
                new_animal = NodeAnimal(animal)
                pergunta = self.__view_akinator.qual_caracteristica(old_animal.animal, new_animal.animal)
                self.__jogo.root = NodeQuestion(pergunta, old_animal, new_animal)

        else:
            question = self.__jogo.root
            
            while True:
                    
                respostaP = self.__view_akinator.faz_pergunta(question.question)

                if respostaP == 's' and type(question.yesQ) == NodeAnimal:
                    resposta = self.__view_akinator.qual_animal(question.yesQ.animal)

                    if resposta == 's':
                        self.__view_akinator.mostra_mensagem(f'Eu venci!! O animal que vc pensou foi um/a {question.yesQ.animal}.')
                        break

                    elif resposta == 'n':
                        self.__view_akinator.mostra_mensagem("Eu desisto!! Você venceu. Agora me diga: ")
                        animal = self.__view_akinator.pega_animal() 
                        new_animal = NodeAnimal(animal)
                        pergunta = self.__view_akinator.qual_caracteristica(new_animal.animal, question.yesQ.animal)
                        new_question = NodeQuestion(pergunta, new_animal, question.yesQ)
                        question.yesQ = new_question
                        break
                        
                elif respostaP == 'n' and type(question.noQ) == NodeAnimal:
                    resposta = self.__view_akinator.qual_animal(question.noQ.animal)

                    if resposta == 's':
                        self.__view_akinator.mostra_mensagem(f'Eu venci!! O animal que vc pensou foi um/a {question.noQ.animal}.')
                        break

                    elif resposta == 'n':
                        self.__view_akinator.mostra_mensagem("Eu desisto!! Você venceu. Agora me diga: ")
                        animal = self.__view_akinator.pega_animal() 
                        new_animal = NodeAnimal(animal)
                        pergunta = self.__view_akinator.qual_caracteristica(new_animal.animal, question.noQ.animal)
                        new_question = NodeQuestion(pergunta, new_animal, question.noQ)
                        question.noQ = new_question
                        break 
                
                elif respostaP == 's':
                    question = question.yesQ

                elif respostaP == 'n':
                    question = question.noQ 

        self.abre_menu() 

    
    def reniciar_jogo(self): 
        self.__jogo.root = None 
        self.play() 

    def abre_menu_principal(self):
        lista_opcoes = {1: self.play, 2: self.carregar_jogo, 0: self.sair}

        continua = True
        while continua:
            lista_opcoes[self.__view_akinator.menu_principal()]()

    def start(self):
        self.abre_menu_principal()

    def abre_menu(self):
        lista_opcoes = {1: self.play, 2: self.reniciar_jogo, 3: self.salvar, 0: self.abre_menu_principal}

        continua = True 
        while continua:
            lista_opcoes[self.__view_akinator.menu()]() 

    def salvar(self):
        self.__view_akinator.mostra_mensagem("Save completo!!")
        with open('jogo', 'wb') as file:
            pickle.dump(self.__jogo, file)

    def carregar_jogo(self):
        try:
            with open('jogo', 'rb') as file:
                jogo_carregado = pickle.load(file)

            self.__view_akinator.mostra_mensagem("Jogo carregado com sucesso!!")
            self.__jogo = jogo_carregado
        except FileNotFoundError:
            self.__view_akinator.mostra_mensagem("Nenhum jogo encontrado para carregar.")

    def sair(self):
        exit(0) 
