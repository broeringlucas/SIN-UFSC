num_matrizes = int(input()) 
n_instancia = 0 
for _ in range(num_matrizes): 
    n_instancia += 1 

    m = [ [int(x) for x in input().split()]   for _ in range(9) ]

    sudoku = True

    for lin in range(9):
        c = set( m[lin] )
        if len(c) != 9:
            sudoku = False
            break

    if sudoku:
        for col in range(9):
            c = set( m[lin][col] for lin in range(9) )
            if len(c) != 9:
                sudoku = False
                break

    for lin in range(0, 9, 3):   
        if not sudoku:
            break
        for col in range(0, 9, 3):
            c = set( m[lin][col:col+3] + m[lin+1][col:col+3] + m[lin+2][col:col+3] )
            if len(c) != 9:
                sudoku = False
                break
    if sudoku: 
        print("Instancia", n_instancia)
        print("SIM")
    else: 
        print("Instancia", n_instancia)
        print("NAO")
   
    
    
    
    