perguntas_realizadas, frequencia = [int(x) for x in input().split()] 

while perguntas_realizadas != 0: 
    pergunta_frequente = 0 
    perguntas = [int(x) for x in input().split()] 
    for i in range(len(perguntas)): 
        contar = perguntas.count(perguntas[i]) 
        if contar >= frequencia: 
            pergunta_frequente = perguntas[i] 
    print(pergunta_frequente)
    perguntas_realizadas, frequencia = [int(x) for x in input().split()] 
