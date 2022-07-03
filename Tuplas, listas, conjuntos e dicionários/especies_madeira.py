num_testes = int(input())

lista_arvores = []

arvore = input()
for _ in range(num_testes):
    arvore = input()
    while arvore != '': 
        lista_arvores.append(arvore)
        arvore = input()
    lista_arvores.sort()
    for i in range(len(lista_arvores)):
        if lista_arvores[i] != lista_arvores[i - 1]:
            contar = lista_arvores.count(lista_arvores[i])
            media = (contar / len(lista_arvores) * 100)
            print(f'{lista_arvores[i]} {media:0.4f}')
    
    print()
    lista_arvores = [] 
        
        
        
        
            


