salario_bruto = float(input())
n_dependentes = int(input())

IRRF = (salario_bruto - (n_dependentes * 137.99))

if salario_bruto <= 720:
    inss = (7.65/100) * salario_bruto
elif salario_bruto <= 1200:
    inss = (9/100) * salario_bruto
elif salario_bruto <= 2400:
    inss = (11/100) * salario_bruto
elif salario_bruto > 2400:
    inss = (11/100) * 2400

IRRF -= inss 

if salario_bruto < 1372.81:
    IRRF = 0 
elif 1372.82 <= salario_bruto <=  2743.25:
    IRRF = IRRF * 15/100
    IRRF -= 205.92
elif salario_bruto > 2743.25:
    IRRF = IRRF * 27.5/100
    IRRF -= 548.82

IRRF_final = max(IRRF, 0)

print(f"{IRRF_final:0.2f}")    
