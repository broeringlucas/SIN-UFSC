
class ItemPedido: 
    def __init__(self, codigo: int, descricao: str, preco_unitario: float):
        if isinstance(codigo, int): 
            self.__codigo = codigo 
        if isinstance(descricao, str): 
            self.__descricao = descricao
        if isinstance(preco_unitario, float) or isinstance(preco_unitario, int): 
            self.__preco_unitario = preco_unitario
    
    @property
    def codigo(self): 
        return self.__codigo

    @property
    def descricao(self): 
        return self.__descricao
    
    @property
    def preco_unitario(self): 
        return self.__preco_unitario
    
    @codigo.setter
    def codigo(self, codigo: int): 
        if isinstance(codigo, int): 
            self.__codigo = codigo 

    @descricao.setter
    def descricao(self, descricao: str): 
        if isinstance(descricao, str): 
            self.__descricao = descricao
    
    @preco_unitario.setter
    def preco_unitario(self, preco_unitario: float): 
        if isinstance(preco_unitario, float) or isinstance(preco_unitario, int): 
            self.__preco_unitario = preco_unitario
            
