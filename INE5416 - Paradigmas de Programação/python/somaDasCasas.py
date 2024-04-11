# https://judge.beecrowd.com/pt/problems/view/2422

def encontrar_casas(casas, soma_duas_casas):
    esq = 0
    dir = len(casas) - 1

    while esq < dir: 
        soma = casas[esq] + casas[dir]
        if soma == soma_duas_casas:
            return casas[esq], casas[dir]
        elif soma < soma_duas_casas:
            esq += 1
        else:
            dir -= 1
        
def main():
    num_casas = int(input())
    casas = []

    for _ in range(num_casas): 
        casas.append(int(input()))

    k = int(input())

    print(*encontrar_casas(casas, k))


main()

