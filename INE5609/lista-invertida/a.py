class Diretorio:
    def __init__(self):
        self.__dir = {}

    @property
    def dir(self):
        return self.__dir 
    
class Registro:
    def __init__(self, nome : str, cidade : str, time : str, plano : float):
        self.__id = 0
        self.__nome = nome 
        self.__cidade = cidade 
        self.__time = time 
        self.__plano = plano 

    @property
    def id(self):
        return self.__id
    
    @property
    def nome(self):
        return self.__nome

    @property
    def cidade(self):
        return self.__cidade
    
    @property
    def time(self):
        return self.__time
    
    @property
    def plano(self):
        return self.__plano
    
    @id.setter
    def id(self, id):
        self.__id = id

class ListaInvertida:
    def __init__(self): 
        self.__dirNome = Diretorio() 
        self.__dirCidade = Diretorio() 
        self.__dirTime = Diretorio() 
        self.__dirPlano = Diretorio() 
        self.__registros = {}
        self.__contador = 1 
    
    @property
    def dirNome(self):
        return self.__dirNome
    
    @property
    def dirCidade(self):
        return self.__dirCidade 
    
    @property
    def dirTime(self):
        return self.__dirTime 
    
    @property
    def dirPlano(self):
        return self.__dirPlano
    
    @property
    def contador(self):
        return self.__contador
    
    @property
    def registros(self):
        return self.__registros
    
    def add_registro(self, registro: Registro):
        registro.id = self.__contador

        if registro not in self.__registros:
            self.__registros[registro.id] = registro

        self.__contador += 1 

        self.__update_diretorio(self.__dirNome, registro.nome, registro.id)
        self.__update_diretorio(self.__dirCidade, registro.cidade, registro.id)
        self.__update_diretorio(self.__dirTime, registro.time, registro.id)
        self.__update_diretorio(self.__dirPlano, registro.plano, registro.id)

    def __update_diretorio(self, diretorio, referencia, id):
        if referencia not in diretorio.dir:
            diretorio.dir[referencia] = []
        diretorio.dir[referencia].append(id)

    def del_registro(self, id):
        if id in self.__dirCidade.dir[self.__registros[id].cidade]:
            self.__dirCidade.dir[self.__registros[id].cidade].remove(id) 
        if id in self.__dirNome.dir[self.__registros[id].nome]:
            self.__dirNome.dir[self.__registros[id].nome].remove(id) 
        if id in self.__dirTime.dir[self.__registros[id].time]:
            self.__dirTime.dir[self.__registros[id].time].remove(id) 
        if id in self.__dirPlano.dir[self.__registros[id].plano]:
            self.__dirPlano.dir[self.__registros[id].plano].remove(id) 
        if id in self.__registros:
            del self.__registros[id]
    
    def busca_simples(self, valor): 
        ids = None
        try: 
            diretorios = [self.__dirCidade.dir, self.__dirNome.dir, self.__dirTime.dir, self.__dirPlano.dir]

            for diretorio in diretorios:
                if valor in diretorio:
                    ids = diretorio[valor]
            if ids:
                print("|     ID     |         Nome         |        Cidade        |         Time         |        Plano         |")
                print("| -------------------------------------------------------------------------------------------------------|")
                for i in ids:
                    print(f'| {self.__registros[i].id:<10} | {self.__registros[i].nome:<20} | {self.__registros[i].cidade:<20} | {self.__registros[i].time:<20} | {self.__registros[i].plano:<20} |')
            else: 
                raise KeyError

        except KeyError:
            print("Nenhum registro encontrado.")
    
    def busca_composta(self, valor1, valor2):
        ids1 = None 
        ids2 = None 
        try:

            diretorios = [self.__dirCidade.dir, self.__dirNome.dir, self.__dirTime.dir, self.__dirPlano.dir]

            for diretorio in diretorios:
                if valor1 in diretorio:
                    ids1 = diretorio[valor1]
                if valor2 in diretorio:
                    ids2 = diretorio[valor2]
            print(ids2)
            print(ids1)
            if ids1 and ids2:
                print("|     ID     |         Nome         |        Cidade        |         Time         |        Plano         |")
                print("| -------------------------------------------------------------------------------------------------------|")
                for i in ids1:
                    for j in ids2:
                        if i == j:
                            print(f'| {self.__registros[i].id:<10} | {self.__registros[i].nome:<20} | {self.__registros[i].cidade:<20} | {self.__registros[i].time:<20} | {self.__registros[i].plano:<20} |')
            else:
                raise KeyError     
            
        except KeyError:
            print("Nenhum registro encontrado.")
    
    def mostrar_todos(self):
        print("|     ID     |         Nome         |        Cidade        |         Time         |        Plano         |")
        print("| -------------------------------------------------------------------------------------------------------|")
        for i in self.__registros:
            print(f'| {self.__registros[i].id:<10} | {self.__registros[i].nome:<20} | {self.__registros[i].cidade:<20} | {self.__registros[i].time:<20} | {self.__registros[i].plano:<20} |')

        

L = ListaInvertida() 
registro1 = Registro('Lucas', 'Palhoca', 'Avai', 19.99)
# registro2 = Registro('Lucas', 'Florianopolis', 'Figueirense', 19.99)
registro2 = Registro('Lucas', 'Florianopolis', 'Figueirense', 19.99)
registro3 = Registro('Joao', 'Sao Jose', 'Figueirense', 19.99)
L.add_registro(registro1)
L.add_registro(registro2)
L.add_registro(registro3)
# L.del_registro(2)
# L.busca_simples('Palhoca')
# L.busca_composta('Palhoca', 'Avai')
L.mostrar_todos() 


