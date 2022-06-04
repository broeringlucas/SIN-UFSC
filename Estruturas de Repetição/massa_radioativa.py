massa_radiotiva = float(input())

tempo = 0 

while massa_radiotiva > 0.5:
    tempo += 50
    massa_radiotiva /= 2
    
print(tempo)