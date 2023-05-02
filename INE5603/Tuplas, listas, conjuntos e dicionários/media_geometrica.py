
quant_num = int(input())

lista_num = []
produto = 1 

while quant_num > 0:
    num = float(input())
    lista_num.append(num)
    produto *= num 
    quant_num -= 1


media_geo = produto ** (1 / len(lista_num))

print(media_geo) 
    
    