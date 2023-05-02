escala_o = input()
temp = float(input())
escala_d = input()

if escala_o == "c":
    temp = temp + 273.15 
elif escala_o == "f":
    temp = (temp + 459.67) * (5/9)
elif escala_o == "r":
    temp = temp * (5/9)
if escala_d == "c":
    temp = temp - 273.15
elif escala_d == "f":
    temp = (temp - 273.15) * 1.8 + 32 
elif escala_d == "r":
    temp = (temp - 273.15) * 1.8 + 491.67

print(temp)

