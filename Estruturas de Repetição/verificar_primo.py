import math 
n = int(input())

if n == 1:
    primo= False
elif n % 2 == 0 and n != 2:
    primo = False 
else:
    primo = True
    raiz = int(math.sqrt(n))
    for i in range (3, raiz+1, 2):
        if n % i == 0:
            primo = False
            break 
        
print(primo)
            