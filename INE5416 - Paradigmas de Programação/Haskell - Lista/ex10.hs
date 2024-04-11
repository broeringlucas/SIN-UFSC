list :: [Int]
list = [1, 2, 3, 3, 4, 3, 5, 3]

par :: Int -> Bool
par a = a `mod` 2 == 0

filtrar :: (Int -> Bool) -> [Int] -> [Int]
filtrar f [] = []
filtrar f (a:b)
    | f a = a : filtrar f b
    | otherwise = filtrar f b

main = do 
    print (filtrar par list)