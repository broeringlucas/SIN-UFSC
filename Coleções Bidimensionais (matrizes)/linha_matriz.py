linha = int(input())
operacao = input() 

matriz = [ [float(input()) for _ in range(12)] for _ in range(12)]

soma = sum(matriz[linha])
media = soma / len(matriz[linha])
if operacao == 'S':
    print(soma)
else: 
    print(f'{media:0.1f}')
