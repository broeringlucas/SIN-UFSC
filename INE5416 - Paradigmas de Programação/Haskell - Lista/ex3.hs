list :: [Int]
list = [2,3,6,1,8,9]

menor :: [Int] -> Int
menor [] = 0
menor [a] = a
menor (a:b)
    | a < menorResto = a 
    | otherwise = menorResto
    where menorResto = menor b

main = do 
    print (menor list)