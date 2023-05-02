
num_linhas, num_colunas = [int(x) for x in input().split()] 

matriz = [[int(x) for x in input().split()] for x in range(num_linhas)]

soma_maior = 0 
soma = 0 
for coluna in range(num_colunas): 
    for linha in range(num_linhas): 
        soma += matriz[linha][coluna] 
    soma_coluna = soma 
    if soma_coluna > soma_maior: 
        soma_maior = soma_coluna
    soma = 0 

for i in range(num_linhas): 
    soma_linha = sum(matriz[i])
    if soma_linha > soma_maior: 
        soma_maior = soma_linha

print(soma_maior) 