s_atual = float(input())
s_minimo = float(input())

quant_salario = s_atual / s_minimo

if 1.5 < quant_salario <= 3:
    reajuste = s_atual * 1.20
elif 3 < quant_salario <= 5:
    reajuste = s_atual * 1.15
elif 1 <= quant_salario <= 1.5:
    reajuste = s_minimo * 1.5
elif quant_salario >= 19:
    reajuste = s_minimo * 20
elif 5 < quant_salario < 17:
    reajuste = s_atual * 1.10 

print(f"{reajuste: 0.2f}")
