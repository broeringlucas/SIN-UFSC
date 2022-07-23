operacao = input()

matriz = [ [float(input()) for _ in range(12)] for _ in range(12)]

soma = 0
for lin in range(1, 12):
    for col in range(0, lin):
        soma += matriz[lin][col]
        
if operacao == 'S':
    print(soma)
else:
    n = (1 + 11) * 11 / 2
    media = round(soma / n)
    print(media)

