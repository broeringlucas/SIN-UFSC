mdc :: Int -> Int -> Int -> Int
mdc x y z 
    | x == 0 = y
    | y == 0 = x
    | z == 0 = x
    | otherwise = mdc y z (mod x y)
    

main = do 
    xStr <- getLine
    yStr <- getLine
    zStr <- getLine
    let x = (read xStr :: Int)
        y = (read yStr :: Int)
        z = (read zStr :: Int)
        result = mdc x y z
    print result