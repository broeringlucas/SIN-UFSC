numero_multiplo = int(input())
tamanho_intervalo = int(input())

for x in range(1,(tamanho_intervalo + 1) ): 
    if x % numero_multiplo == 0:
        print(x, end= " ")
        
