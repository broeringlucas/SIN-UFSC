v = float(input())
s = input()
i = int(input())

seguro = v * (10/100)

if s == "M":
    if i <= 24: 
        pagar = seguro
    elif 25 <= i <= 33: 
        pagar = seguro * (90 / 100)
    elif  i > 33:
        pagar = seguro * (20 / 100) 
    print(pagar)
elif s == "F": 
    if i <= 24:
        pagar = seguro * (95 / 100)
    elif 25 <= i <= 33:
        pagar = seguro * (80 / 100)
    elif i > 33:
        pagar = seguro * (65 / 100)
    print(pagar)

