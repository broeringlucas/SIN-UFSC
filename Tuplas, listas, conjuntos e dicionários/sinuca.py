num_bolas = int(input()) 
cores_bolas = [(x) for x in input().split()] 

while num_bolas > 1:
    num_bolas -= 1 
    proxima_fila = [0] * (num_bolas)
    for i in range(len(cores_bolas) -1):
        if cores_bolas[i] != cores_bolas[i + 1]:
            proxima_fila[i] = "-1"
        else:
            proxima_fila[i] = "1"
    cores_bolas = proxima_fila

if cores_bolas[0] ==  "-1":
    print("branca")
elif cores_bolas[0] == "1":
    print("preta") 
