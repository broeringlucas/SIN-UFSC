
contador = 0 
todos_nomes = []

while contador <= 1:
    tamanho_lista = int(input())
    for i in range(tamanho_lista): 
        nome = input()
        todos_nomes.append(nome) 
    contador +=1 
    tamanho_lista = 0
todos_nomes.sort() 
for i in range(len(todos_nomes)):
    print(todos_nomes[i]) 

 