import random
import json

# Essa função gera um arquivo json com uma lista de acessos aleatórios, recebe dois parâmetros: 
# 1 - o número de acessos e o 2 - total de páginas distintas endereçáveis

def generateJson(accesses, total_pages):
    pages = [random.randint(0, total_pages) for _ in range(accesses)]

    # Aqui esscolhe o nome do arquivo json
    with open('pages100000.json', 'w') as json_file:
        json.dump(pages, json_file)

    return pages

generateJson(100000, 256)