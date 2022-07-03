primeiro_conector = [int(x) for x in input().split()] 
segundo_conector = [int(x) for x in input().split()] 

conector_compativel = [] 
compativel = 'N'
for i in range(len(primeiro_conector)): 
    if primeiro_conector[i] - segundo_conector[i] == 1 or primeiro_conector[i] - segundo_conector[i] == -1: 
        conector_compativel.append(1) 

if conector_compativel == [1, 1, 1, 1, 1]:
    compativel = 'Y'

print(compativel)
        
