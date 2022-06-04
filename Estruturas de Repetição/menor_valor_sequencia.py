tamanho_sequencia = int(input())

menor_n = float('inf')

for _ in range(tamanho_sequencia):
    n = int(input())
    if n < menor_n:
        menor_n = n
        
print(menor_n)

    
    
