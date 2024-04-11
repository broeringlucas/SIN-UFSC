# https://judge.beecrowd.com/pt/problems/view/1466

class Node: 
    def __init__(self, valor): 
        self.valor = valor 
        self.esq = None
        self.dir = None
    
    def inserir(self, valor): 
        
        if valor < self.valor: 
            if self.esq is None: 
                self.esq = Node(valor) 
            else: 
                self.esq.inserir(valor)
        else: 
            if self.dir is None: 
                self.dir = Node(valor)
            else:
                self.dir.inserir(valor)

    def printTree(self, n): 
        fila = [] 
        fila.append(self) 
        while fila: 
            node = fila.pop(0) 
            if n == 1:
                print(node.valor, end="")
            else: 
                print(node.valor, end=" ") 
            if node.esq is not None: 
                fila.append(node.esq) 
            if node.dir is not None: 
                fila.append(node.dir)
            n -= 1

def main():
    casos_teste = int(input())
    for j in range(casos_teste):
        n = int(input())
        elementos = list(map(int, input().split()))
        root = Node(elementos[0])
        for i in range(1, n):
            root.inserir(elementos[i])
        print("Case", j+1, end="")
        print(":")
        root.printTree(n)
        print("\n")

main()

