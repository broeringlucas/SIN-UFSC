sequencia_cartas = [int(x) for x in input().split()] 

ordem_crescente = sorted(sequencia_cartas)
ordem_decrescente = sorted(sequencia_cartas, reverse = True)  

if sequencia_cartas == ordem_crescente:
    print("C")
elif sequencia_cartas == ordem_decrescente:
    print("D")
else:
    print("N")

