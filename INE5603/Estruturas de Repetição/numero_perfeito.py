numero_casos = int(input())

divisores = 0
while numero_casos > 0:
    num = int(input())
    for a in range(1, num):
        if num % a == 0:
            divisores += a
    if divisores == num:
        print(num, "eh perfeito")
    else:
        print(num, "nao eh perfeito")       
    numero_casos -= 1
    divisores = 0 
    
    