quantidade_valores = int(input())

contador = 1 
valor = float(input())
soma = valor 
while quantidade_valores > contador:
    contador += 1
    valor = float(input())
    soma += valor

media = soma / contador 

print(media)