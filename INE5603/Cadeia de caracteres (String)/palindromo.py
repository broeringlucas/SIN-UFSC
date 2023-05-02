frase = input()

n_frase =""
for i in frase.lower():
    if i.isalpha():
        n_frase += i 
    
    
    
print(n_frase == n_frase[::-1])
