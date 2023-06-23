class Diretorio:
    def __init__(self):
        self.__dir = {}

    @property
    def dir(self):
        return self.__dir 
    
class Registro:
    def __init__(self, codigo: str, nome : str, tipo: str, departamento : str, preco : float):
        self.__id = 0
        self.__codigo = codigo 
        self.__nome = nome
        self.__tipo = tipo  
        self.__departamento = departamento
        self.__preco = preco 
    
    @property
    def codigo(self): 
        return self.__codigo 
    
    @property
    def id(self):
        return self.__id
    
    @property
    def nome(self):
        return self.__nome

    @property
    def tipo(self):
        return self.__tipo

    @property
    def departamento(self):
        return self.__departamento
    
    @property
    def preco(self):
        return self.__preco
    
    @id.setter
    def id(self, id):
        self.__id = id

class ListaInvertida:
    def __init__(self): 
        self.__dirCodigo = Diretorio() 
        self.__dirNome = Diretorio() 
        self.__dirTipo = Diretorio() 
        self.__dirDepartamento = Diretorio() 
        self.__dirPreco = Diretorio() 
        self.__registros = []
        self.__contador = 1
    

    @property
    def dirCodigo(self):
        return self.__dirCodigo
    
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

            if len(self.__registros) == 0: 
                self.__registros.append(registro)
            else: 
                for i in range (len(self.__registros)):
                    print('a')
                    if registro.codigo == self.__registros[i].codigo:
                        raise KeyError
                    else:
                        self.__registros.append(registro)

            self.__contador += 1 

            self.__update_diretorio(self.__dirCodigo, registro.codigo, registro.id)
            self.__update_diretorio(self.__dirNome, registro.nome, registro.id)
            self.__update_diretorio(self.__dirTipo, registro.tipo, registro.id)
            self.__update_diretorio(self.__dirDepartamento, registro.departamento, registro.id)
            self.__update_diretorio(self.__dirPreco, registro.preco, registro.id)
        
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

        print(diretorio.dir)

    def __define_faixa(self, referencia):
        if referencia < 10:
            faixa = 'Menor que 10'
        elif referencia < 50:
            faixa = '10 - 49.99'
        elif referencia < 100:
            faixa = '50 - 99.99'
        else:
            faixa = 'Maior que 100'

        return faixa 

    def del_registro(self, id):
        id_array = id - 1 
        faixa = self.__define_faixa(self.__registros[id_array ].preco) 
        if id in self.__dirCodigo.dir[self.__registros[id_array].codigo]:
            self.__dirCodigo.dir[self.__registros[id_array].codigo].remove(id) 
        if id in self.__dirNome.dir[self.__registros[id_array].nome]:
            self.__dirNome.dir[self.__registros[id_array].nome].remove(id) 
        if id in self.__dirTipo.dir[self.__registros[id_array].tipo]:
            self.__dirTipo.dir[self.__registros[id_array].tipo].remove(id) 
        if id in self.__dirDepartamento.dir[self.__registros[id_array].departamento]:
            self.__dirDepartamento.dir[self.__registros[id_array].departamento].remove(id)
        if id in self.__dirPreco.dir[faixa]:
            self.__dirPreco.dir[faixa].remove(id) 
        del self.__registros[id_array]

    def busca_simples(self, valor): 
        ids = None
        try: 
            diretorios = [self.__dirCodigo.dir, self.__dirNome.dir, self.__dirTipo.dir, self.__dirDepartamento.dir, self.__dirPreco.dir]

            for diretorio in diretorios:
                if valor in diretorio:
                    ids = diretorio[valor]
                print(ids)
                    
            if ids:
                print("|     ID     |         Nome         |        Cidade        |         Time         |        Plano         |")
                print("| -------------------------------------------------------------------------------------------------------|")
                for i in ids:
                    print(f'| {self.__registros[i].id:<10} | {self.__registros[i].nome:<20} | {self.__registros[i].tipo:<20} | {self.__registros[i].departamento:<20} | {self.__registros[i].preco:<20} |')
            else: 
                raise KeyError

        except KeyError:
            print("Nenhum registro encontrado.")
    
    def busca_composta(self, valor1, valor2):
        ids1 = None 
        ids2 = None 
        try:

            diretorios = [self.__dirNome.dir, self.__dirTime.dir, self.__dirPlano.dir]

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
                            print(f'| {self.__registros[i - 1].id:<10} | {self.__registros[i - 1].nome:<20} | {self.__registros[i - 1].cidade:<20} | {self.__registros[i - 1].time:<20} | {self.__registros[i - 1].plano:<20} |')
            else:
                raise KeyError     
            
        except KeyError:
            print("Nenhum registro encontrado.")
    
    def mostrar_todos(self):
        print("|     ID     |         Nome         |        Cidade        |         Time         |        Plano         |")
        print("| -------------------------------------------------------------------------------------------------------|")
        for i in range (len(self.__registros)):
         print(f'| {self.__registros[i].id:<10} | {self.__registros[i].nome:<20} | {self.__registros[i].cidade:<20} | {self.__registros[i].time:<20} | {self.__registros[i].plano:<20} |')
        

L = ListaInvertida() 
registro1 = Registro('ABC', 'Queijo Prato', 'Queijo', 'Comida', 10.99)
registro2 = Registro('AB1', 'Queijo Prato', 'Queijo', 'Comida', 10.99)
registro3 = Registro('ABD', 'Queijo Prato', 'Queijo', 'Comida', 9)
L.add_registro(registro1)
L.add_registro(registro2)
L.add_registro(registro3)
# L.del_registro(1)
# L.del_registro(3)
# L.busca_simples('ABD')
# L.busca_composta('Palhoca', 'Avai')
# L.mostrar_todos() 


