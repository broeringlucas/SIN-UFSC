import json

from Algorithms.FIFO import FIFO
from Algorithms.LRU import LRU
from Algorithms.NRU import NRU
from Algorithms.SegundaChanceEhRelogio import SegundaChanceEhRelogio

frames = 64
pages = json.load(open('Accesses/pages100000.json'))
totalPages = 256
accessTohReset = 1000
accesses = len(pages)

# Instanciando os algoritmos de substituição de páginas
fifo = FIFO(frames, pages, totalPages, accesses)
segundaChanceEhRelogio = SegundaChanceEhRelogio(frames, pages, totalPages, accesses)
nru = NRU(frames, pages, totalPages, accessTohReset, accesses)
lru = LRU(frames, pages, totalPages, accesses)

# Executando os algoritmos de substituição de páginas e mostrando resultados 
fifo.results()
segundaChanceEhRelogio.results()
nru.results()
lru.results()


