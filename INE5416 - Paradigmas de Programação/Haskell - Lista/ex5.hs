list :: [Int]
list = [1, 2, 3]

busca :: [Int] -> Int -> Bool 
busca [] _ = False
busca (a:b) n 
    | a == n = True
    | otherwise = busca b n 


main = do 
    nStr <- getLine
    let n = read nStr :: Int
    print (busca list n)