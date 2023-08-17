from listaDuplamenteEncadeada import ListaDuplamenteEncadeada

# Criando a lista
lista = ListaDuplamenteEncadeada(10)

# O índice da lista começa no 1, ou seja o primeiro elemento está no índice 1
# Sempre vou imprimir a lista toda, depois de chamar algum método para demonstrar que realmente aconteceu alguma mudança nela
# Seguir o passo a passo para observar que a lista está mudando

print("--- INÍCIO ---")
# Inserindo elementos
lista.inserirAntesDoAtual(10)
lista.inserirAntesDoAtual(13)
lista.inserirAntesDoAtual(20)
lista.imprimirElementosDaLista()
print('------------')

lista.inserirAposAtual(15)
lista.inserirAposAtual(100)
lista.imprimirElementosDaLista()
print('------------')

lista.inserirComoPrimeiro(3)
lista.imprimirElementosDaLista()
print('------------')

lista.inserirComoUltimo(4)
lista.imprimirElementosDaLista()
print('------------')

lista.inserirNaPosicaoK(8, 2)
lista.imprimirElementosDaLista()
print('------------')

# Excluindo elementos
# Acessei o atual para mostrar que ele vai ser excluido pela método
print(lista.acessarAtual())
lista.excluirAtual()
lista.imprimirElementosDaLista()
print('------------')

lista.excluirPrimeiro()
lista.imprimirElementosDaLista()
print('------------')

lista.excluirUltimo()
lista.imprimirElementosDaLista()
print('------------')

lista.excluirElem(13)
lista.imprimirElementosDaLista()
print('------------')

lista.excluirDaPos(2)
lista.imprimirElementosDaLista()
print('------------')

# Buscando elementos, um que está na lista e outro que não existi não lista
lista.buscar(100)
lista.buscar(1000)

print("--- FIM ---")
