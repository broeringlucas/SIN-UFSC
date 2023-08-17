
n1 = int(input())
n2 = int(input())

a = n1
b = n2
while b > 0:
    resto = a % b
    a = b
    b = resto
    
print(a)