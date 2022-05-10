import math

a = int(input("Digite o valor de a : "))
b = int(input("Digite o valor de b : "))
c = int(input("Digite o valor de c : "))

delta = b**2 - 4*a*c

x1 = (- b + math.sqrt(delta))/(2*a)
x2 = (- b - math.sqrt(delta))/(2*a)

print("As raízes reais são: ", x1, x2)
