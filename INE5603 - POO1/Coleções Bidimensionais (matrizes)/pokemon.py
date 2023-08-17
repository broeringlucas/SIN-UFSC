cont = 0 
while True: 
    try: 
        num_linhas, num_colunas = [int(x) for x in input().split()] 

        matriz = [[int(x) for x in input().split()] for x in range(num_linhas)]

        for linhas in range(num_linhas): 
            for colunas in range(num_colunas): 
                if matriz[linhas][colunas] == 2: 
                    coluna_pokemon = colunas 
                    linha_pokemon = linhas 
                elif matriz[linhas][colunas] == 1:
                    coluna_treinador = colunas
                    linha_treinador = linhas 

        num_passos = abs(linha_treinador - linha_pokemon) + abs(coluna_treinador - coluna_pokemon)

        print(num_passos) 
    except EOFError: 
        break
print(cont) 

    