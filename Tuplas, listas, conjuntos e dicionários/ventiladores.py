num_linhas, num_colunas, coluna = [int(x) for x in input().split()]

estourado_esq = False
estourado_dir = False
linha_estourou = 0 
coluna_estourou = 0 
while num_linhas != 0:
    coluna -= 1
    for linha in range(num_linhas):
        compartimentos = [int(x) for x in input().split()]
        
        if not estourado_esq and not estourado_dir:
            ind_esq = coluna
            while compartimentos[ind_esq] == 0:
                ind_esq -= 1
                
            ind_dir = coluna
            while compartimentos[ind_dir] == 0:
                ind_dir += 1
                
            coluna += compartimentos[ind_esq] - compartimentos[ind_dir]
        if not estourado_esq and not estourado_dir:
            if coluna <= ind_esq:
                linha_estourou = linha+1
                coluna_estourou = ind_esq+1 
                estourado_esq = True 
            elif coluna >= ind_dir:
                linha_estourou = linha + 1
                coluna_estourou = ind_dir + 1 
                estourado_dir = True 
    if not estourado_esq and not estourado_dir: 
        print("OUT", coluna+1)
    elif estourado_esq: 
        print("BOOM", linha_estourou , coluna_estourou)
    elif estourado_dir: 
        print("BOOM", linha_estourou , coluna_estourou)
    
    num_linhas, num_colunas, coluna = [int(x) for x in input().split()]
    
