gabarito = input()
respostas = input()

quant_perguntas = len(gabarito)
num_acertos = 0

for i in range(quant_perguntas):
    if gabarito[i] == respostas[i]:
        num_acertos += 1

print(num_acertos) 
    
    