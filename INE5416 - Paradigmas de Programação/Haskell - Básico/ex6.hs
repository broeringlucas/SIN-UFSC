construirTriangulo :: Int -> Int -> Int -> String
construirTriangulo x y z
    | x + y > z && x + z > y && y + z > x = "Pode-se construir um triângulo"
    | otherwise = "Nao pode-se construir um triângulo"

main = do 
    xStr <- getLine
    yStr <- getLine
    zStr <- getLine
    let x = (read xStr :: Int)
    let y = (read yStr :: Int)
    let z = (read zStr :: Int)
    putStrLn (construirTriangulo x y z)
