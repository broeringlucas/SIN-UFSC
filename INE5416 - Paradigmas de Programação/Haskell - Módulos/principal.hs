import Pilha (Pilha (Stack), emptyStack, push, pop, top)

import Formas ( Forma(Trapezio), area )

import Ponto ( Ponto(Ponto2D), distancia, colineares )

main = do 
          

          print(area (Trapezio 2 3 3))

          print(distancia (Ponto2D 1 1) (Ponto2D 2 2))
          print(colineares (Ponto2D 1 1) (Ponto2D 2 2) (Ponto2D 3 3))
