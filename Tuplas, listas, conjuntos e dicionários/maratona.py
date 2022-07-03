postos_agua, distancia_maxima = [int(x) for x in input().split()] 
distancia_postos_agua = [int(x) for x in input().split()] 

consegue_terminar = 'N'

for i in range(1,postos_agua): 
    if (distancia_postos_agua[i] - distancia_postos_agua[i - 1]) <= distancia_maxima:
        consegue_terminar = 'S'
    else: 
        consegue_terminar = 'N'
        break 

print(consegue_terminar)