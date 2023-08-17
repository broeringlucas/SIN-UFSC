while True:
    try:
        dimensao_matriz = int(input())
        inicio_1 = int(dimensao_matriz/3)
        final_1 = dimensao_matriz-inicio_1
        
        m = [[0 for i in range(dimensao_matriz)] for j in range(dimensao_matriz)]
        
        for i in range(dimensao_matriz):
            m[i][i] = 2

        j = 0
        for i in range(dimensao_matriz-1,-1,-1):
            m[j][i] = 3
            j += 1
            
        for i in range(inicio_1, final_1):
            for j in range(inicio_1, final_1):
                m[i][j] = 1
        
        m[int(dimensao_matriz/2)][int(dimensao_matriz/2)] = 4
        
        for i in range(dimensao_matriz):
            for j in range(dimensao_matriz):
                print(m[j][i], end='')
            print()
        print()
    
    except EOFError:
        break