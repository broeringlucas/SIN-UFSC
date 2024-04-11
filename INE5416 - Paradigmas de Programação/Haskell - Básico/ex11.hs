mdc :: Int -> Int -> Int
mdc x y
    | y == 0 = x
    | otherwise = mdc y (mod x y)


main = do 
    xStr <- getLine
    yStr <- getLine
    let x = (read xStr :: Int)
        y = (read yStr :: Int)
        result = mdc x y 
    print result