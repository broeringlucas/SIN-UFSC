nome = [(x) for x in input().split()]

nome_abreviado = ""
nomes_do_meio = ""
for i in range(1,(len(nome) - 1)): 
    if len(nome[i]) > 3:
        nomes_do_meio += nome[i][0] + "." + " "
    elif len(nome[i]) <= 3:
        nomes_do_meio += nome[i] + " " 
    
nome_abreviado = nome[0] + " " + nomes_do_meio + nome[-1] 

print(nome_abreviado)