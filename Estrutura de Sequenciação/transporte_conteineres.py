a, b, c = [float(w) for w in input().split()]
x, y, z = [float(w) for w in input().split()]

larg = x // a 
comp = y // b
alt = z //  c

quant_conteiner = round(larg * comp * alt)

print(quant_conteiner)
