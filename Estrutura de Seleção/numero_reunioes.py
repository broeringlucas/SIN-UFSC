dia_aniver1 = int(input())
dia_aniver2 = int(input())
dia_aniver3 = int(input())

if dia_aniver1 != dia_aniver2 and dia_aniver1 != dia_aniver3 and dia_aniver2 != dia_aniver3:
    numero_festas = 3
elif dia_aniver1 == dia_aniver2 == dia_aniver3:
    numero_festas = 1 
elif dia_aniver1 == dia_aniver2 or dia_aniver1 == dia_aniver3 or dia_aniver2 == dia_aniver3: 
    numero_festas = 2 

print(numero_festas)