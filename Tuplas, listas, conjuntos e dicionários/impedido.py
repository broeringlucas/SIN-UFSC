atacantes, defensores = [int(x) for x in input().split()] 

while atacantes != 0: 
    impedido = "N"
    distancias_atacantes = [int(x) for x in input().split()] 
    distancias_defensores = [int(x) for x in input().split()]
    distancias_defensores.sort() 
    for i in range(atacantes):
        if defensores > 2:
            if distancias_atacantes[i] < distancias_defensores[-2]: 
                impedido = "Y"
                break
        elif defensores <= 2:
            if distancias_atacantes[i] < distancias_defensores[-1]: 
                impedido = "Y"
                break 
    print(impedido) 

    atacantes, defensores = [int(x) for x in input().split()]  
