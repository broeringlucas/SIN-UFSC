
main = do
    let x = 3.7 :: Double
        y = -2.5 :: Double

    putStrLn $ "Valor original de x: " ++ show x
    putStrLn $ "Valor original de y: " ++ show y

    -- Ceiling: Arredonda para o próximo inteiro superior
    putStrLn $ "Teto de x: " ++ show (ceiling x)
    putStrLn $ "Teto de y: " ++ show (ceiling y)

    -- Floor: Arredonda para o próximo inteiro inferior
    putStrLn $ "Piso de x: " ++ show (floor x)
    putStrLn $ "Piso de y: " ++ show (floor y)
