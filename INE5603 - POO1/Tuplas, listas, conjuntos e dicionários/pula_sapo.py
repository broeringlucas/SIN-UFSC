limite, quant = [int(x) for x in input().split()]
alturas = [int(x) for x in input().split()]

sapo_pula = False
altura_sapo = alturas[0] 

for i in range(len(alturas)): 
    if alturas[i] < limite + altura_sapo:
        sapo_pula = True 
    elif alturas[i] > limite + altura_sapo:  
        sapo_pula = False 
        break
    altura_sapo = alturas[i] 
if sapo_pula == True: 
    print("YOU WIN")
else: 
    print("GAME OVER")
        
