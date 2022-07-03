num_jogadores, num_partidas = [int(x) for x in input().split()] 

gols = 0 
gols_todas_partidas = 0 
for _ in range(num_jogadores): 
    desempenho_jogador = [int(x) for x in input().split()] 
    for i in range(3): 
        if desempenho_jogador[i] >= 1: 
            gols += 1
    if gols >= num_partidas:
        gols_todas_partidas += 1 
    gols = 0 

print(gols_todas_partidas) 

