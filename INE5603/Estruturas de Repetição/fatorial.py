n = int(input())
x = n - 1 
if x == 0: 
    fatorial = 1 
else: 
    while x != 0: 
        fatorial = n * x
        n = fatorial 
        x -= 1
    
print(fatorial)
