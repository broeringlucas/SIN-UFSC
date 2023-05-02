num_valores = 4 
lista_num = [] 
while num_valores > 0: 
    num = int(input()) 
    if num not in lista_num:  
        lista_num.append(num)
    num_valores -= 1
         
num_distintos = len(lista_num)

print(num_distintos)
    
