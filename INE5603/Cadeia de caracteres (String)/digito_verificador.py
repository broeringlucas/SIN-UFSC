num = input()

soma = 0
peso = len(num)
for i in range(len(num)-1):
    soma += int(num[i]) * peso
    peso -= 1
dv = 11 - soma % 11
if dv >= 10:
    dv = 0
    
print(dv == int(num[-1]))