valores_romanos = {"M":1000, "D":500, "C":100, "L":50, "X":10, "V":5, "I":1}
num_romano = input()

num_decimal = 0
for i in range(len(num_romano)-1):
    num = num_romano[i]
    num_seguinte = num_romano[i+1]
    if valores_romanos[num] >= valores_romanos[num_seguinte]:
        num_decimal += valores_romanos[num]
    else:
        num_decimal -= valores_romanos[num]
num_decimal += valores_romanos[num_romano[-1]]

print(num_decimal)