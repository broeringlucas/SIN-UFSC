num_pessoas = int(input()) 

tempo_ativado = 10 
while num_pessoas != 0: 
    tempos_aproximacao = [int(x) for x in input().split()] 
    if isinstance(tempos_aproximacao, list):
        for i in range(1, (len(tempos_aproximacao))):
            resto = tempos_aproximacao[i] - tempos_aproximacao[i - 1] 
            if resto < 10: 
                tempo_ativado += resto 
            elif resto >= 10:
                tempo_ativado += 10 
    print(tempo_ativado) 
    num_pessoas = int(input())
    tempo_ativado = 10 

    

    


