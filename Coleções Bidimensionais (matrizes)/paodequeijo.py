while True:
    try:
        n, m = [int(x) for x in input().split()]
        matriz = [ [int(x) for x in input().split()] for _ in range(n) ]
            
        for i in range(n):
            for j in range(m):
                if matriz[i][j] == 1:
                    matriz[i][j] = 9
                    
        for i in range(n):
            for j in range(m):
                if matriz[i][j] == 0:
                    for di,dj in ( (-1,0), (0,1), (1,0), (0,-1) ):
                        ni = i + di
                        nj = j + dj
                        if 0 <= ni < n and 0 <= nj < m and matriz[ni][nj] == 9:
                            matriz[i][j] += 1

        for i in range(n):
            for j in range(m):
                print(matriz[i][j], end='')
            print()
    except EOFError:
        break
