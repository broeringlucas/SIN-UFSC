data Arvore = Null | No Int Arvore Arvore

minhaArvore :: Arvore
minhaArvore = No 52 (No 32 (No 12 Null Null) (No 35 Null Null)) (No 56 (No 32 Null Null) (No 64 Null Null))

somaElementos :: Arvore -> Int
somaElementos Null = 0
somaElementos (No n esq dir) = n + (somaElementos esq) + (somaElementos dir)

buscaElemento :: Arvore -> Int -> Bool
buscaElemento Null _ = False
buscaElemento (No n esq dir) x 
    | (n == x) = True                           
    | otherwise = (buscaElemento esq x) || (buscaElemento dir x)

limiteSup :: Int
limiteSup = 1000 --Define um limite superior para o maior número

minimo :: Int -> Int -> Int
minimo x y | (x < y) = x
           | otherwise = y

minimoElemento :: Arvore -> Int
minimoElemento Null = limiteSup 
minimoElemento (No n esq dir) = 
    minimo n (minimo (minimoElemento esq) (minimoElemento dir))

-- A 
ocorrenciasElemento :: Arvore -> Int -> Int
ocorrenciasElemento Null _ = 0
ocorrenciasElemento (No n esq dir) x 
    | (n == x) = 1 + (ocorrenciasElemento esq x) + (ocorrenciasElemento dir x)
    | otherwise = (ocorrenciasElemento esq x) + (ocorrenciasElemento dir x)

-- B 
maioresQueElemento :: Arvore -> Int -> Int
maioresQueElemento Null _ = 0
maioresQueElemento (No n esq dir) x 
    | (n > x) = 1 + (maioresQueElemento esq x) + (maioresQueElemento dir x)
    | otherwise = (maioresQueElemento esq x) + (maioresQueElemento dir x)


mediaElementos :: Arvore -> Float
mediaElementos Null = 0
mediaElementos arvore = fromIntegral (somaElementos arvore) / fromIntegral (numeroElementos arvore)

-- D
numeroElementos :: Arvore -> Int
numeroElementos Null = 0
numeroElementos (No _ esq dir) = 1 + (numeroElementos esq) + (numeroElementos dir)

-- E
elementos :: Arvore -> [Int]
elementos Null = []
elementos (No n esq dir) = n : (elementos esq) ++ (elementos dir)

main = do putStrLn (show (somaElementos minhaArvore))
          putStrLn (show (buscaElemento minhaArvore 30))
          putStrLn (show (buscaElemento minhaArvore 55))
          putStrLn (show (minimoElemento minhaArvore))
          print(ocorrenciasElemento minhaArvore 32)
          print(maioresQueElemento minhaArvore 50)
          print(mediaElementos minhaArvore)
          print(numeroElementos minhaArvore)
          print(elementos minhaArvore)

