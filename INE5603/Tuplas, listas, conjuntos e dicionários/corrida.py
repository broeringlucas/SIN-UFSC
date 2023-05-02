carros, voltas = [int(x) for x in input().split()]

tempos = [0] * carros

primeiro_lugar = 0 
segundo_lugar = 0
terceiro_lugar = 0
 
for i in range(carros):
    tempo = [int(x) for x in input().split()] 
    tempos[i] += sum(tempo)
lista_tempos = tempos 
tempos_em_ordem = sorted(tempos)
for i in range(len(tempos)):
    if tempos[i] == tempos_em_ordem[0]:
        primeiro_lugar = i + 1
    elif tempos[i] == tempos_em_ordem[1]: 
        segundo_lugar = i + 1 
    elif tempos[i] == tempos_em_ordem[2]: 
        terceiro_lugar = i + 1

print(primeiro_lugar)
print(segundo_lugar)
print(terceiro_lugar)
 

