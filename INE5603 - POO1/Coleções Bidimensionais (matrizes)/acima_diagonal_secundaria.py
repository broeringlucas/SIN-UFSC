operacao = input()

matriz = [ [float(input()) for _ in range(12)] for _ in range(12)]

soma = 0
for lin in range(0, 11):
    for col in range(0, 11 - lin):
        soma += matriz[lin][col]
        
if operacao == 'S':
    print(soma)
else:
    n = (1 + 11) * 11 / 2
    media = round(soma / n)
    print(f'{media:0.1f}')

