list :: [Int]
list = [1,2,3]

media :: [Int] -> Float
media list 
    | list == [] = 0
    | otherwise = fromIntegral(soma list) / comprimento list
    where
        soma [] = 0
        soma (a:b) = a + soma b
        comprimento [] = 0
        comprimento (_:b) = 1 + (comprimento b)

main = do 
    print (media list)