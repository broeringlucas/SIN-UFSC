from abstractControladorPessoas import AbstractControladorPessoas
from cliente import Cliente
from tecnico import Tecnico


class ControladorPessoas(AbstractControladorPessoas):
    def __init__(self):
        self.__clientes = []
        self.__tecnicos = [] 
    
    @property
    def clientes(self): 
        return self.__clientes 
    
    @property
    def tecnicos(self):
        return self.__tecnicos 
    
    def inclui_cliente(self, codigo: int, nome: str):
        if isinstance(codigo, int) and isinstance(nome, str): 
            duplicado = False 
            for c in self.__clientes: 
                if c.codigo == codigo: 
                    duplicado = True 
                    print("Cliente duplicado")
            if not duplicado: 
                cliente_novo = Cliente(nome, codigo) 
                self.__clientes.append(cliente_novo)
                print("Cliente Adicionado")
                return cliente_novo 
    
    def inclui_tecnico(self, codigo: int, nome: str): 
        if isinstance(codigo, int) and isinstance(nome, str):
            duplicado = False
            for t in self.__tecnicos:
                if t.codigo == codigo:
                    duplicado = True
                    print("Tecnico Duplicado")
            if not duplicado: 
                tecnico_novo = Tecnico(nome, codigo)
                self.__tecnicos.append(tecnico_novo)
                print("Tecnico Adicionado")
                return tecnico_novo


