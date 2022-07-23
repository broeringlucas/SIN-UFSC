num_testes = int(input())
teste = 1 
for _ in range(num_testes):
    nl, nc, i_soco, j_soco = [ int(x) for x in input().split() ]
    i_soco -= 1
    j_soco -= 1

    matriz = [ [int(x) for x in input().split()] for _ in range(nl) ]

    for i in range(nl):
        for j in range(nc):
            matriz[i][j] += max(10 - max(abs(i - i_soco), abs(j - j_soco)), 1)
    print(f"Parede {teste}:")      
    print(matriz)
    teste += 1 
