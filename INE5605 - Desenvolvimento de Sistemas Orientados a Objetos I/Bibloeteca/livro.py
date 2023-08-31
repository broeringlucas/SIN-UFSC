from editora import Editora
from autor import Autor
from capitulo import Capitulo


class Livro:

    def __init__(self, codigo: int, titulo: str, ano: int, editora: Editora,
                 autor: Autor, numero_capitulo: int, titulo_capitulo: str):
        if isinstance(codigo, int):
            self.__codigo = codigo
        if isinstance(titulo, str):
            self.__titulo = titulo
        if isinstance(ano, int):
            self.__ano = ano
        if isinstance(editora, Editora):
            self.__editora = editora
        self.__autores = []
        if isinstance(autor, Autor):
            self.__autores.append(autor)
        self.__capitulos = []
        if isinstance(numero_capitulo, int) and isinstance(titulo_capitulo,
                                                           str):
            self.__capitulos.append(Capitulo(numero_capitulo, titulo_capitulo))

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo: int):
        if isinstance(codigo, int):
            self.__codigo = codigo

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo: str):
        if isinstance(titulo, str):
            self.__titulo = titulo

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, ano: int):
        if isinstance(ano, int):
            self.__ano = ano

    @property
    def editora(self):
        return self.__editora

    @editora.setter
    def editora(self, editora: Editora):
        if isinstance(editora, Editora):
            self.__editora = editora

    @property
    def autores(self):
        return self.__autores

    @property
    def capitulos(self):
        return self.__capitulos

    def incluir_autor(self, autor: Autor):
        if isinstance(autor, Autor) and autor is not None:
            if autor not in self.__autores:
                self.__autores.append(autor)
                print("Autor adicionado")
            else:
                print("Autor Duplicado")

    def excluir_autor(self, autor: Autor):
        if isinstance(autor, Autor) and autor is not None:
            if autor in self.__autores:
                self.__autores.remove(autor)
                print("Autor removido")

            else:
                print("Não há autor para remover")

    def incluir_capitulo(self, numero: int, titulo: str):
        if isinstance(numero, int) and isinstance(titulo, str):
            if self.find_capitulo_by_titulo(titulo) is None:
                self.__capitulos.append(Capitulo(numero, titulo))
                print("Capitulo adicionado")
            else:
                print("Capitulo duplicado")

    def excluir_capitulo(self, titulo: str):
        if isinstance(titulo, str) and titulo is not None:
            if self.find_capitulo_by_titulo(titulo) is not None:
                for t in self.__capitulos:
                    if t.titulo == titulo:
                        self.__capitulos.remove(t)
                        print("Capitulo removido")
                    else:
                        print("Não há capitulo para remover")

    def find_capitulo_by_titulo(self, titulo: str):
        if isinstance(titulo, str):
            for capitulo in self.__capitulos:
                if capitulo.titulo == titulo:
                    print("Capitulo encontrado")
                    return capitulo



autor1 = Autor(321, "Joao")
autor2 = Autor(123, "Lucas")
autor3 = Autor(333, "Mariana")
autor4 = Autor(123, "Joao")
editora1 = Editora(123, "abc")
livro1 = Livro(123, "aaa", 2000, editora1, autor1, 333, "ccc") 
livro1.incluir_capitulo(333, "ccc")
livro1.incluir_capitulo(333, "aaa")
livro1.incluir_capitulo(123, "aca")
print(livro1.capitulos)