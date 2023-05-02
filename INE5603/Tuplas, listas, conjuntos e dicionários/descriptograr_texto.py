alfabeto_normal = [(x) for x in input().split()]
alfabeto_cifragem =  [(x) for x in input().split()]
mensagem_cifrada =  input() 

dicionario_letras = {}
mensagem = ""

for i in range(26):
    dicionario_letras[alfabeto_cifragem[0][i]] = alfabeto_normal[0][i]
    
mensagem_descriptografada = ''

for i in range(len(mensagem_cifrada)):
    if mensagem_cifrada[i].isalpha(): 
        mensagem +=dicionario_letras[mensagem_cifrada[i]]
    elif mensagem_cifrada[i] == " ":
        mensagem += " "
    else:
        mensagem += mensagem_cifrada[i]
        
print(mensagem)