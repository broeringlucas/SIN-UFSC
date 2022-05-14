comprimento_mesa = float(input())
largura_mesa = float(input())
n_gavetas = int(input())
tipo_madeira = input()

preco_minimo = 200 

area_mesa = comprimento_mesa * largura_mesa
preco = area_mesa * 100 
preco += n_gavetas * 30 

if area_mesa > 2:
    preco += 50
    
if tipo_madeira == "mogno":
    preco += 150
elif tipo_madeira == "carvalho":
    preco += 125
    
preco_final = max(preco, 200)

print(f"{preco_final: 0.2f}")
        