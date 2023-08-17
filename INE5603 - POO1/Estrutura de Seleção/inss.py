salario = float(input())

if salario <= 720: 
    inss = salario * (7.65 / 100)
elif salario <= 1200:
    inss = salario * (9 / 100)
elif salario <= 2400:
    inss = salario * (11 / 100)
elif salario > 2400:
    inss = 2400 * (11 / 100)

print(inss)



