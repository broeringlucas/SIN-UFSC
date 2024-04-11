maior :: Float -> Float -> Float -> Float
maior a b c 
    | a > b && a > c = a
    | b > a && b > c = b
    | otherwise = c

main = do 
    aStr <- getLine
    bStr <- getLine
    cStr <- getLine
    let a = (read aStr :: Float)
        b = (read bStr :: Float)
        c = (read cStr :: Float)
        result = maior a b c 
    print result