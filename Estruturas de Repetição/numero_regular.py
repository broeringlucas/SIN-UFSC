n = int(input())

if n == 1: 
    print(False)
else:
    while n % 2 == 0:
        n //= 2
    while n % 3 == 0:
        n //= 3
    while n % 5 == 0:
        n //= 5
    
    print(n == 1)
