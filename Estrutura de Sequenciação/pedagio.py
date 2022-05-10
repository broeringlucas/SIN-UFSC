l, d = [float(w) for w in input().split()]
k, p = [float(w) for w in input().split()]
 
quant_pedagio =round(l / d)
preco_pedagio = quant_pedagio * p
custo_km = l * k 

total = round(custo_km + preco_pedagio)

print(total)
