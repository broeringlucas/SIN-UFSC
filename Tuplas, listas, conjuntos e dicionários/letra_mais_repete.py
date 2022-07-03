sentence = input() 

letra_minuscula = sentence.lower()
lista_sentence = [] 
lista_sentence.append(letra_minuscula) 
quant_mais_aparece = 0
letra_mais_aparece = '' 
for i in range(len(letra_minuscula)): 
    n_letra = letra_minuscula.count(lista_sentence[0][i])
    if n_letra > quant_mais_aparece:
        quant_mais_aparece = n_letra 
        letra_mais_aparece = lista_sentence[0][i]   

print(letra_mais_aparece)