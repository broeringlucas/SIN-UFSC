num_participantes = int(input()) 
num_testes = 1 


while num_participantes != 0:
    lista_participantes = [int(x) for x in input().split()]
    for i in range(num_participantes): 
        if lista_participantes[i] == i + 1:
            print("Teste", num_testes) 
            print(lista_participantes[i])
            print() 
            break 
    num_testes += 1 
    num_participantes = int(input()) 
