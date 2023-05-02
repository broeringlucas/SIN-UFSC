
try:
    while True:
        nl, nc = [int(x) for x in input().split()]
        mat = [ input().split() for _ in range(nl) ]

        # Encontra as coordenadas de 'X'
        for i in range(len(mat)):
            if 'X' in mat[i]:
                j = mat[i].index('X')
                break

        # Percorre o caminho
        direcao_ant = None
        while True:   
            for direcao, di, dj in ( ('N',-1,0), ('S',1,0), ('L',0,1), ('O',0,-1) ):
                ni = i + di
                nj = j + dj
                if 0 <= ni < nl and 0 <= nj < nc and mat[ni][nj] == '0':
                    if direcao_ant != None and direcao != direcao_ant:
                        giro = 'R' if direcao_ant+direcao in ('NL', 'LS', 'SO', 'ON') else 'L'
                        print(giro, end=' ')
                    print('F', end=' ')
                    i = ni
                    j = nj
                    mat[i][j] = 'X'
                    direcao_ant = direcao
                    break
            else:
                break
        print('E')
except EOFError:
    pass