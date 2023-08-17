num_praias = int(input())

mais_distante = ""
maior_distancia = 0
praias_perto_centro = 0
m_distancia = 0 

for _ in range(num_praias):
    praia, distancia = input().split(";")
    distancia = int(distancia)
    if  15 <= distancia <= 20:
        praias_perto_centro += 1
    if distancia > m_distancia:
        mais_distante = praia
        m_distancia = distancia
    maior_distancia += distancia
    

distancia_media = round(maior_distancia / num_praias, 1) 

print(f"{mais_distante};{praias_perto_centro};{distancia_media}")