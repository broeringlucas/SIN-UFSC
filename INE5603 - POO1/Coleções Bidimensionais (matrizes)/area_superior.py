operacao = input() 

matriz = [[float(input()) for _ in range(12)] for _ in range(12)]

soma = 0 
for linha in range(0, 5):
    for coluna in range(1+linha, 11-linha):
        soma += matriz[linha][coluna] 

if operacao == 'S':
    print(soma)
else: 
    media = soma / 30
    print(f'{media:0.1f}') 