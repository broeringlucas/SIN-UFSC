numero_jogadas = int(input())

maria_ganhou = 0
john_ganhou = 0
while numero_jogadas != 0:
    jogadas = input().split() 
    jogadas_tamanho = len(jogadas) 
    for i in range(jogadas_tamanho):
        perc_jogada = jogadas[i]
        if perc_jogada == "0":
            maria_ganhou += 1
        elif perc_jogada == "1":
            john_ganhou += 1
    print(f"Mary won {maria_ganhou} times and John won {john_ganhou} times")
    numero_jogadas = int(input())