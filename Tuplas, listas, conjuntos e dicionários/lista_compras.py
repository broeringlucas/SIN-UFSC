num_testes = int(input()) 

for _ in range(num_testes): 
    lista_compras = set([(x) for x in input().split()])
    lista_compras = sorted(list(lista_compras))
    print(*lista_compras) 