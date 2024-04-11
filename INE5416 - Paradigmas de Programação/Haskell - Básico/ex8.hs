bhaskara :: Float -> Float -> Float -> Float
bhaskara a b c = if delta < 0 then -1 else ((-b) + sqrt(delta)) / (2 * a)
    where delta = (b^2) - 4 * a * c

main = do
    aStr <- getLine
    bStr <- getLine
    cStr <- getLine
    let a = (read aStr :: Float)
        b = (read bStr :: Float)
        c = (read cStr :: Float)
        result = bhaskara a b c
    print result