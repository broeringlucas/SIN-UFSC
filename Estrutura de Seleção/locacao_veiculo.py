dias = int(input())
km = float(input())

if km / dias  > 60:
    km_excedido = km / dias - 60 
    preco_km_ex = km_excedido * 0.5 * dias 
    custo= 45 * dias + preco_km_ex
else:
    custo = 45 * dias 

print(custo)
