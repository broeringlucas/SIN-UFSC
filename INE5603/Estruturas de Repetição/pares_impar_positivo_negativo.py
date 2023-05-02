
n_par = 0 
n_impar = 0 
n_positivo = 0 
n_negativo = 0
contador = 0

while contador < 5:
    valor_int = int(input())
    if valor_int % 2 == 0:
        n_par += 1 
    else:
        n_impar += 1
    if valor_int > 0:
        n_positivo += 1
    elif valor_int < 0:
        n_negativo += 1 
    contador += 1

print(n_par, "valor(es) par(es)")
print(n_impar, "valor(es) impar(es)")
print(n_positivo, "valor(es) positivo(s)")
print(n_negativo, "valor(es) negativo(s)")
