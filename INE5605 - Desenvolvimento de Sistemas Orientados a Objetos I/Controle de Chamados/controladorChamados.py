from abstractControladorChamados import AbstractControladorChamados
from tipoChamado import TipoChamado
from chamado import Chamado
from datetime import date as Date
from cliente import Cliente
from tecnico import Tecnico
from collections import defaultdict


class ControladorChamados(AbstractControladorChamados):

    def __init__(self):
        self.__chamados = [] 
        self.__tipos_chamados = []
    
    def total_chamados_por_tipo(self, tipo: TipoChamado):
        if isinstance(tipo, TipoChamado):
            total_chamados = 1 
            for t in self.__chamados: 
                if t.codigo == t.tipo.codigo: 
                    total_chamados += 1 
                return total_chamados 

    def inclui_chamado(self, data: Date, cliente: Cliente, tecnico: Tecnico, titulo: str, descricao: str, prioridade: int, tipo: TipoChamado):
        duplicado = False 
        for c in self.__chamados: 
            if c.data == data and c.cliente == c.cliente.codigo and c.tecnico == c.tecnico.codigo and tipo.codigo == c.tipo.codigo:
                duplicado = True 
                print("Chamado duplicado")
        if not duplicado: 
            chamado = Chamado(data, cliente, tecnico, titulo, descricao, prioridade, tipo) 
            self.__chamados.append(chamado)
            print("Chamado Adicionado")
            return chamado 

    def inclui_tipochamado(self, codigo: int, nome: str, descricao: str):
        duplicado = False 
        for c in self.tipos_chamados:
            if c.codigo == codigo:
                print("Tipo chamado duplicado")
                duplicado = True 
        if not duplicado: 
            tipo_chamado = TipoChamado(codigo, descricao, nome) 
            self.__tipos_chamados.append(codigo, descricao, nome)
            print("Tipo chamado adicionado")
            return tipo_chamado
    @property
    def tipos_chamados(self): 
        return self.__tipos_chamados