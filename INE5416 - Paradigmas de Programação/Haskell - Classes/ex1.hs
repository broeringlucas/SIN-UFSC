class (Integral x) => MeuInt x where
    bigger :: x -> x -> x
    smaller :: x -> x -> x
    par :: x -> Bool
    impar :: x -> Bool
    primo :: x -> Bool
    mdc :: x -> x -> x
    (===) :: x -> x -> Bool
    triploDobro :: x -> x
    (=/=) :: x -> x -> Bool

    bigger a b | a > b = a
               | otherwise = b

    smaller a b | a == (bigger a b) = b
                | otherwise = a

    -- A 
    par x | mod x 2 == 0 = True
          | otherwise = False

    -- B
    impar x | mod x 2 /= 0 = True
            | otherwise = False

    -- C 
    primo n
        | n <= 1 = False
        | otherwise = null [x | x <- [2..isqrt n], n `mod` x == 0]
        where
            isqrt = floor . sqrt . fromIntegral
    
    -- D 
    mdc a b | b == 0 = a
            | otherwise = mdc b (mod a b)

    -- E
    (===) a b
            | abs (a - b) <= 1 = True
            | otherwise = False

    -- F 
    -- retorna o triplo do dobro de x
    triploDobro x = 3 * (2 * x)

    -- G
    -- O not do operador === 
    (=/=) a b = not (a === b)


    


instance MeuInt Integer
instance MeuInt Int

main = do 
    print (bigger (3 :: Integer) (4 :: Integer))
    print (smaller (3 :: Integer) (4 :: Integer))
    print (par (3 :: Integer))
    print (par (4 :: Integer))
    print (impar (3 :: Integer))
    print (impar (4 :: Integer))
    print (primo (3 :: Integer))
    print (primo (4 :: Integer))
    print (mdc (20 :: Integer) (10 :: Integer))
    print ((===) (4 :: Integer) (3 :: Integer))
    print ((===) (3 :: Integer) (5 :: Integer))