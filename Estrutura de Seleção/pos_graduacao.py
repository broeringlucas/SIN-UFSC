conceito1 = (input())
conceito2 = (input())
conceito3 = (input())
conceito4 = (input())

if conceito1 == "A": 
    nota1 = 4 
elif conceito1 == "B": 
    nota1 = 3 
elif conceito1 == "C": 
    nota1 = 2 
elif conceito1 == "E": 
    nota1 = 0 

if conceito2 == "A": 
    nota2 = 4 
elif conceito2 == "B": 
    nota2 = 3 
elif conceito2 == "C": 
    nota2 = 2 
elif conceito2 == "E": 
    nota2 = 0 

if conceito3 == "A": 
    nota3 = 4 
elif conceito3 == "B": 
    nota3 = 3 
elif conceito3 == "C": 
    nota3 = 2 
elif conceito3 == "E": 
    nota3 = 0

if conceito4 == "A": 
    nota4 = 4 
elif conceito4 == "B": 
    nota4 = 3 
elif conceito4 == "C": 
    nota4 = 2 
elif conceito4 == "E": 
    nota4 = 0

if nota1 >= 2 and nota2 >= 2 and nota3 >= 2 and nota4 >= 2: 
    aprovado = True 
else: 
    aprovado = False

ia = (nota1 + nota2 + nota3 + nota4) / 4 

if ia >= 3 and aprovado == True: 
    resultado = True 
else: 
    resultado = False 

print(resultado)

