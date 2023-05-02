consumo = int(input())

if consumo >= 30:
    valor_total = 30 * 0.09556
    consumo -= 30
    if consumo > 100:
        valor_ate_100 = 70 * 0.16698
        valor_total += valor_ate_100 
        consumo -= 70
        if consumo > 200:
            valor_ate_200 = 100 * 0.25052
            valor_total += valor_ate_200
            consumo -= 100
            valor_acima_200 = consumo * 0.27836
            valor_total += valor_acima_200 
        elif consumo <= 100:
            valor_ate_200 = consumo * 0.25052
            valor_total += valor_ate_200 
    elif consumo <= 100:
        valor_ate_100 = consumo * 0.16698
        valor_total += valor_ate_100 
else:
    valor_total = consumo * 0.09556
    

print(f"{valor_total:0.2f}")