
quant_num = int(input())

lista_num = []
soma = 0
somatorio_termos = 0 
while quant_num > 0:
    num = float(input())
    lista_num.append(num)
    soma += num 
    quant_num -= 1
    
media = soma / len(lista_num)
for i in range(len(lista_num)):
    somatorio_termos += (lista_num[i] - media) ** 2 

desvio_padrao = (somatorio_termos / (len(lista_num) - 1)) ** (1/2) 

print(desvio_padrao) 
    
    