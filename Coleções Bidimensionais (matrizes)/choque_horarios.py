horarios = ["0730", "0820", "0910", "1010", "1100", "1330", "1420", "1510", "1620", "1710", "1830", "1920", "2020", "2110"]
 
quadro = [ [None] * 6 for _ in range(len(horarios)) ]
 
n = int(input())

tem_choque = False
for _ in range(n):
    horarios_disciplina = input().split()
    disciplina = horarios_disciplina.pop(0)
    for horario in horarios_disciplina:
        dia_semana = int(horario[0])
        hora = horario[1:5]
        num_aulas = int(horario[-1])
        
        c = dia_semana - 2
        lin = horarios.index(hora)
        for l in range(lin, lin+num_aulas):
            if quadro[l][c] == None:
                quadro[l][c] = disciplina
            else:
                print(quadro[l][c], disciplina)
                tem_choque = True
                break
        if tem_choque:
            break
    if tem_choque:
        break
            