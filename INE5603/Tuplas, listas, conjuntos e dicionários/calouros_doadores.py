num_calouros = int(input()) 

calouros = [] 
doadores = [] 
calouros_doadores = [] 

for _ in range(num_calouros): 
    nome_calouros = input()
    calouros.append(nome_calouros) 

num_doadores = int(input())
for _ in range(num_doadores): 
    nome_doadores = input()
    doadores.append(nome_doadores)

for i in range(len(calouros)):
    if calouros[i] in doadores: 
        calouros_doadores.append(calouros[i])
        doadores.remove(calouros[i])

proporcao = len(calouros_doadores) / len(doadores) 

print(f"{proporcao:5f}") 