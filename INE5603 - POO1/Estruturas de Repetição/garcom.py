n_bandejas = int(input())
contador = 0 
copos_quebrados = 0 

while n_bandejas > contador: 
    n_latas, n_copos = [int(x) for x in input().split()]
    if n_latas > n_copos: 
        copos_quebrados += n_copos 
    contador += 1 

print(copos_quebrados) 

