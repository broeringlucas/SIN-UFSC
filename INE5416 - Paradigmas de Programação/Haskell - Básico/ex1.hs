potencia :: Float -> Float -> Float
potencia x y = (x ** y)

main = do 
    putStrLn "Digite dois numeros: "
    xStr <- getLine
    yStr <- getLine
    let x = (read xStr :: Float)
    let y = (read yStr :: Float)
    print (potencia x y)