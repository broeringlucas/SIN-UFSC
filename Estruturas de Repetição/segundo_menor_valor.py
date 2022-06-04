import math

tamanho_sequencia = int(input())

list = []

for _ in range(tamanho_sequencia):
    num = int(input())
    list.append(num)
    
list.sort()
print(list[1])