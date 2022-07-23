dimensao_matriz = int(input())

matriz = [ [int(x) for x in input().split()] for _ in range(dimensao_matriz)]

quadrado_magico = True 

diagonal_principal = 0
diagonal_secundaria = 0
coluna = 0


for lin in range(dimensao_matriz):
    diagonal_principal += matriz[lin][lin]

i = -1
for lin in range(dimensao_matriz):
    diagonal_secundaria += matriz[lin][i]
    i -= 1
    
if diagonal_principal != diagonal_secundaria:
    quadrado_magico = False

if quadrado_magico:
    for lin in range(dimensao_matriz):
        for col in range(dimensao_matriz):
            coluna += matriz[lin][col]
        linha = sum(matriz[lin])
        if linha != coluna:
            quadrado_magico = False
            break
        elif linha != linha:
            quadrado_magico = False
            break
        elif coluna != coluna:
            quadrado_magico = False
            break
        elif linha != diagonal_secundaria or linha != diagonal_principal:
            quadrado_magico = False
            break
        elif coluna != diagonal_secundaria or coluna != diagonal_principal:
            quadrado_magico = False
            break 
        coluna = 0

print(quadrado_magico)
