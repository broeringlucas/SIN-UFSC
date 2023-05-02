
media_mensal_chuvas = [0]*12 
for i in range(12): 
    mes = [int(x) for x in input().split()] 
    media_mensal_chuvas[i] = round(sum(mes) / len(mes), 2) 

print(*media_mensal_chuvas) 