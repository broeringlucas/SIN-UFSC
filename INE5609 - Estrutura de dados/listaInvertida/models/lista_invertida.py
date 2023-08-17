from models.diretorio import Diretorio
from models.registro import Registro

class ListaInvertida:
    def __init__(self): 
        self.__dirNome = Diretorio() 
        self.__dirTipo = Diretorio() 
        self.__dirDepartamento = Diretorio() 
        self.__dirPreco = Diretorio() 
        self.__registros = []
        self.__contador = 1
    
    @property
    def dirNome(self):
        return self.__dirNome
    
    @property
    def dirTipo(self):
        return self.__dirTipo
    
    @property
    def dirDepartamento(self):
        return self.__dirDepartamento 
    
    @property
    def dirPreco(self):
        return self.__dirPreco
    
    @property
    def contador(self):
        return self.__contador
    
    @property
    def registros(self):
        return self.__registros
    
    def add_registro(self, registro: Registro):
        try: 

            registro.id = self.__contador

            self.__registros.append(registro)

            self.__contador += 1 

            self.__update_diretorio(self.__dirNome, registro.nome, registro.id)
            self.__update_diretorio(self.__dirTipo, registro.tipo, registro.id)
            self.__update_diretorio(self.__dirDepartamento, registro.departamento, registro.id)
            self.__update_diretorio(self.__dirPreco, registro.preco, registro.id)
            print("Registro adicionado com sucesso!!")
        
        except KeyError:
            print("Registro repetido")
    

    def __update_diretorio(self, diretorio, referencia, id):
        if isinstance(referencia, str) and referencia not in diretorio.dir:
            diretorio.dir[referencia] = []
        elif isinstance(referencia, float) or isinstance(referencia, int): 
            referencia = self.__define_faixa(referencia) 
            if referencia not in diretorio.dir:
                diretorio.dir[referencia] = []
    
        diretorio.dir[referencia].append(id)

    def __define_faixa(self, referencia):
        if referencia < 10:
            faixa = 'Menor que 10'
        elif referencia < 50:
            faixa = '10 até 49.99'
        elif referencia < 100:
            faixa = '50 até 99.99'
        elif referencia < 200:
            faixa = '100 até 199.99'
        else:
            faixa = 'Maior que 200'

        return faixa 

    def del_registro(self, id):
        try: 
            id_array = id - 1 
            if self.__registros[id_array].id:
                faixa = self.__define_faixa(self.__registros[id_array ].preco) 
                if id in self.__dirNome.dir[self.__registros[id_array].nome]:
                    self.__dirNome.dir[self.__registros[id_array].nome].remove(id) 
                if id in self.__dirTipo.dir[self.__registros[id_array].tipo]:
                    self.__dirTipo.dir[self.__registros[id_array].tipo].remove(id) 
                if id in self.__dirDepartamento.dir[self.__registros[id_array].departamento]:
                    self.__dirDepartamento.dir[self.__registros[id_array].departamento].remove(id)
                if id in self.__dirPreco.dir[faixa]:
                    self.__dirPreco.dir[faixa].remove(id) 
                self.__registros[id_array] = ''
                print(f'Registro {id} removido com sucesso!!')
            else: 
                raise KeyError
        except:
            print("Registro não existi!!")

    def busca_simples(self, valor): 
        ids = None
        try: 
            diretorios = [self.__dirNome.dir, self.__dirTipo.dir, self.__dirDepartamento.dir, self.__dirPreco.dir]

            for diretorio in diretorios:
                if valor in diretorio:
                    ids = diretorio[valor]
                    
            if ids:
                print("|     ID     |         Nome         |         Tipo         |     Departamento     |        Preço         |")
                print("| -------------------------------------------------------------------------------------------------------|")
                for i in ids:
                    i = i - 1 
                    print(f'| {self.__registros[i].id:<10} | {self.__registros[i].nome:<20} | {self.__registros[i].tipo:<20} | {self.__registros[i].departamento:<20} | {self.__registros[i].preco:<20} |')
                print("| -------------------------------------------------------------------------------------------------------|")
            else: 
                raise KeyError

        except KeyError:
            print("Nenhum registro encontrado!!")
    
    def busca_composta(self, valor1, valor2):
        ids1 = None 
        ids2 = None 
        try:

            diretorios = [self.__dirNome.dir, self.__dirTipo.dir, self.__dirDepartamento.dir, self.__dirPreco.dir]

            for diretorio in diretorios:
                if valor1 in diretorio:
                    ids1 = diretorio[valor1]
                if valor2 in diretorio:
                    ids2 = diretorio[valor2]

            if ids1 and ids2:
                print("|     ID     |         Nome         |         Tipo         |     Departamento     |        Preço         |")
                print("| -------------------------------------------------------------------------------------------------------|")
                for i in ids1:
                    for j in ids2:
                        if i == j:
                            i = i - 1 
                            print(f'| {self.__registros[i].id:<10} | {self.__registros[i].nome:<20} | {self.__registros[i].tipo:<20} | {self.__registros[i].departamento:<20} | {self.__registros[i].preco:<20} |')
                print("| -------------------------------------------------------------------------------------------------------|")

            else:
                raise KeyError     
            
        except KeyError:
            print("Nenhum registro encontrado!!")
    
    def mostrar_todos(self):
        print("|     ID     |         Nome         |         Tipo         |     Departamento     |        Preço         |")
        print("| -------------------------------------------------------------------------------------------------------|")
        for i in range (len(self.__registros)):
            if self.__registros[i] != '':
                print(f'| {self.__registros[i].id:<10} | {self.__registros[i].nome:<20} | {self.__registros[i].tipo:<20} | {self.__registros[i].departamento:<20} | {self.__registros[i].preco:<20} |')
        print("| -------------------------------------------------------------------------------------------------------|")

