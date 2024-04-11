list :: [Int]
list = [1, 2, 3, 3, 4, 3, 5, 3]

ocorrencia :: [Int] -> Int -> Int
ocorrencia [] _ = 0
ocorrencia (a:b) n
    | a == n = 1 + ocorrencia b n
    | otherwise = ocorrencia b n

main = do 
    nStr <- getLine
    let n = read nStr :: Int
    print (ocorrencia list n)