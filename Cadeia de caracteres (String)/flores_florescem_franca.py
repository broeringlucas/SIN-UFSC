sentence = [(x) for x in input().split()]

contador = 0
lista_letras = [] 
tautograma = "N"
while sentence != ["*"]:
    for i in range(len(sentence)): 
        if sentence[i][0].upper() == ((sentence[0][0])).upper(): 
            lista_letras.append(sentence[i][0].upper())
        contador += 1
    if lista_letras.count(((sentence[0][0])).upper()) == contador:
        tautograma = "Y"

    print(tautograma)
    tautograma = "N"
    lista_letras = []
    contador = 0 
    sentence = [(x) for x in input().split()]
    

    
            