list :: [Int]
list = [1,2,3]

soma :: [Int] -> Int
soma [] = 0
soma (a:b) = a + soma b

main = do 
    print (soma list)