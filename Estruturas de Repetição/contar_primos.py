primero_n_da_seq = int(input())
ulitmo_n_da_seq = int(input())

contador_primo = 0
for n in range (primero_n_da_seq, ulitmo_n_da_seq + 1):
    if n != 1:
        for i in range(2,n):
            if n % i == 0:
                break
        else:
            contador_primo += 1 
                
        
print(contador_primo)