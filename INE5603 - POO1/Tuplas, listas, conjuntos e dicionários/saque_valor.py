quant_diferentes_valores = int(input()) 

quantidade_cedulas = [0] * quant_diferentes_valores 
valores = [0] * quant_diferentes_valores 
saque_cedulas = [0] * quant_diferentes_valores

for i in range(quant_diferentes_valores):
    valores[i] = int(input())
    quantidade_cedulas[i] = int(input()) 

saque_valor = float(input())

for i in range(-1, -quant_diferentes_valores - 1, -1):
    if quantidade_cedulas[i] > 0: 
        saque_cedulas[i] = int(saque_valor) // valores[i]
        saque_valor = saque_valor % valores[i]

print(*saque_cedulas)
