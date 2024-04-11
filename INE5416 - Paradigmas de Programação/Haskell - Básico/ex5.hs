aprovadoReprovado :: Float -> Float -> Float -> String
aprovadoReprovado n1 n2 n3
    | media >= 6 = "Aprovado"
    | otherwise = "Reprovado"
    where media = (n1 + n2 + n3) / 3

main = do
    n1Str <- getLine
    n2Str <- getLine
    n3Str <- getLine
    let n1 = (read n1Str :: Float)
    let n2 = (read n2Str :: Float)
    let n3 = (read n3Str :: Float)
    putStrLn (aprovadoReprovado n1 n2 n3)