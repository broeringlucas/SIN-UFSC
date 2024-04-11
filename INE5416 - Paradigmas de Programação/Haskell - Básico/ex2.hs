absoluto :: Float -> Float
absoluto num = abs num

main = do 
    putStrLn "Digite um numero: "
    numStr <- getLine
    let x = (read numStr :: Float)
    print (absoluto x)