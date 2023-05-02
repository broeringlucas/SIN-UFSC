num_saltadores = int(input())

melhor_salto = 0 
melhor_saltador = ""
for _ in range(num_saltadores):
    salto1, salto2 , salto3, nome = input().split()
    salto1 = float(salto1)
    salto2 = float(salto2)
    salto3 = float(salto3)
    if salto1 > melhor_salto:
        melhor_salto = salto1
        melhor_saltador = nome
    if salto2 > melhor_salto:
        melhor_salto = salto2
        melhor_saltador = nome
    if salto3 > melhor_salto:
        melhor_salto = salto3
        melhor_saltador = nome

print(melhor_saltador)
