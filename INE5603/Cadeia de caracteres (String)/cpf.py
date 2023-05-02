import re

cpf = input()
cpf = re.sub(r'[^\w\s]','',cpf)
padrao_cpf = '[0-9]{11}'

def verificar_ultimo_digito(numero):
    soma = 0
    peso = len(numero)   
    for i in range(len(numero)-1):
        soma += int(numero[i]) * peso
        peso -= 1
    dv = 11 - soma % 11
    if dv >= 10:
        dv = 0
    if(dv == int(numero[-1])):
        return True
    else:
        return False
    
def verificador_penultimo_digito(numero):
    soma = 0
    peso = len(numero) - 1   
    for i in range(len(numero)-2):
        soma += int(numero[i]) * peso
        peso -= 1    
    dv = 11 - soma % 11
    if dv >= 10:
        dv = 0
    if(dv == int(numero[-2])):
        return True
    else:
        return False

estadoUD = verificar_ultimo_digito(cpf)
estadoPD = verificador_penultimo_digito(cpf)
estado = estadoPD and estadoUD

primeiro_num = cpf[0]
if estado == True:
    if re.match(padrao_cpf, cpf):
        estado = True
    else:
        estado = False
    for i in range(len(cpf)):
        if cpf[i] != primeiro_num:
            estado = True
            break
        else:
            estado = False

print(estado)