num_aeroportos, num_voos = [int(x) for x in input().split()]
contagem = [0] * num_aeroportos
n = 1 
while num_aeroportos != 0:
    for _ in range(num_voos):
        aeroporto_origem, aeroporto_destino = [int(x) for x in input().split()]
        contagem[aeroporto_origem - 1] += 1
        contagem[aeroporto_destino - 1] += 1
    maior = max(contagem)
        
    aeros = [i + 1  for i in range(len(contagem)) if contagem[i] == maior]
    print("Teste", n)
    print(*aeros)
    print()
    n += 1 
    num_aeroportos, num_voos = [int(x) for x in input().split()]
    contagem = [0] * num_aeroportos

