list :: [Int]
list = [1, 2, 3, 3, 4, 3, 5, 3]

dobro :: Int -> Int
dobro a = a * a

mapear :: (Int -> Int) -> [Int] -> [Int]
mapear f [] = []
mapear f (a:b) = f a : mapear f b


main = do 
    print (mapear dobro list)