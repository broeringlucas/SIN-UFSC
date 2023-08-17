num_sorteios = int(input()) 

num_mais_proximo = 0
igual = False 
while num_sorteios > 0: 
    num_alunos, num_secreto = [int(x) for x in input().split()] 
    lista_num_alunos = [int(x) for x in input().split()]  
    for i in range(len(lista_num_alunos)):
        if lista_num_alunos[i] == num_secreto: 
            igual = True 
            break 
        elif 0 < lista_num_alunos[i] < (num_secreto + 2) :
            if num_mais_proximo < lista_num_alunos[i]: 
                num_mais_proximo = lista_num_alunos[i]
    if igual == True:
        print(i + 1)
    else:
        print(lista_num_alunos.index(num_mais_proximo) + 1)      
    num_sorteios -= 1
    num_mais_proximo = 0 
    igual = False 
    
    