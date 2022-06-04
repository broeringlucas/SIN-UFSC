tamanho_sequencia = int(input())

maior_n = float('-inf')
posicao = 0
for i in range(1,(tamanho_sequencia + 1)):
    n = int(input())
    if n > maior_n:
        maior_n = n
        posicao = i
    
print(maior_n, posicao)