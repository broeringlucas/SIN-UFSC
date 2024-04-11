
list :: [Int]
list = [1, 2, 3]

diferencaMaiorMenor :: [Int] -> Int
diferencaMaiorMenor [] = 0
diferencaMaiorMenor [_] = 0
diferencaMaiorMenor (x:xs) = diferencaMaiorMenorAux x x xs
  where
    diferencaMaiorMenorAux maior menor [] = maior - menor
    diferencaMaiorMenorAux maior menor (y:ys)
      | y > maior = diferencaMaiorMenorAux y menor ys
      | y < menor = diferencaMaiorMenorAux maior y ys
      | otherwise = diferencaMaiorMenorAux maior menor ys

main = do 
    print (diferencaMaiorMenor list)
