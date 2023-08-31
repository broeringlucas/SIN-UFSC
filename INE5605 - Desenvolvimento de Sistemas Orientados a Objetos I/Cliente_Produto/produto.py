from categoria_produto import CategoriaProduto
from cliente import Cliente


class Produto:

    def __init__(self, codigo: int, descricao: str,
                 categoria_produto: CategoriaProduto):
        if isinstance(codigo, int):
            self.__codigo = codigo
        if isinstance(descricao, str):
            self.__descricao = descricao
        if isinstance(categoria_produto, CategoriaProduto):
            self.__categoria_produto = categoria_produto

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo: int):
        if isinstance(codigo, int):
            self.__codigo = codigo

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        if isinstance(descricao, str):
            self.__descricao = descricao

    @property
    def categoria_produto(self):
        return self.__categoria_produto

    @categoria_produto.setter
    def categoria_produto(self, categoria_produto: CategoriaProduto):
        if isinstance(categoria_produto, CategoriaProduto):
            self.__categoria_produto = categoria_produto

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade: int):
        if isinstance(quantidade, int):
            self.__quantidade = quantidade

    @property
    def preco_unitario(self):
        return self.__preco_unitario

    @preco_unitario.setter
    def preco_unitario(self, preco_unitario: int):
        if isinstance(preco_unitario, float) or isinstance(preco_unitario,
                                                           int):
            self.__preco_unitario = preco_unitario

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, cliente: Cliente):
        if isinstance(cliente, Cliente) or cliente is None:
            self.__cliente = cliente

    def preco_total(self):
        preco_total = self.__preco_unitario * self.__quantidade

        return preco_total

categoria1 = CategoriaProduto('brinquedos')
produto1 = Produto('123', 'Boneca', categoria1)
cliente1 = Cliente('Maria', '321')
print(cliente1.fone)
