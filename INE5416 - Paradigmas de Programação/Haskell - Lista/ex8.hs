list :: [Int]
list = [1, 2, 3, 3, 4, 3, 5, 3]

inverte :: [Int] -> [Int]
inverte [] = []
inverte (a:b) = inverte b ++ [a]

main = do 
    print (inverte list)