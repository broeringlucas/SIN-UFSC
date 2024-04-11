funcaoXOR :: Bool -> Bool -> Bool
funcaoXOR True False = True
funcaoXOR False True = True
funcaoXOR False False = False
funcaoXOR True True = False

main = do
    xStr <- getLine
    yStr <- getLine
    let x = (read xStr :: Bool)
    let y = (read yStr :: Bool)
    print (funcaoXOR x y) 