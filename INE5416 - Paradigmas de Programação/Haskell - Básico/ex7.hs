fibonnaci :: Int -> String
fibonnaci n
    | n == 0 = "0"
    | n == 1 = "1"
    | otherwise = show(fib n 0 1)
    where fib n a b
            | n == 0 = a
            | n == 1 = b
            | otherwise = fib (n-1) b (a+b)

main = do 
    nStr <- getLine
    let n = (read nStr :: Int)
    putStrLn(fibonnaci n)