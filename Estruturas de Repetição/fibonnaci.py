n = int(input())

ant = 0
prox = 1
if n == 0:
    fibonnaci = 0
elif n == 1:
    fibonnaci = 1
else: 
    for _ in range(1, n):
        fibonnaci = ant + prox
        ant = prox
        prox = fibonnaci
    
print(fibonnaci)
