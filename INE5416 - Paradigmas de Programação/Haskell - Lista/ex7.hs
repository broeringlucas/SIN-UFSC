alunos :: [(Int, String, Float)]
alunos = [(1, "Ana", 3.4), (2, "Bob", 6.7), (3, "Tom", 7.6)]

getNome :: (Int, String, Float) -> String
getNome (a,b,c) = b

getPrimeiroAluno :: [(Int, String, Float)] -> (Int, String, Float)
getPrimeiroAluno (a:_) = a

gerarPares :: [(Int, String, Float)] -> [(Int, String, Float)] -> [(String, String)] 
gerarPares l1 l2 = [(getNome a, getNome b) | a <- l1, b <- l2, getNome a /= getNome b]

aprovados :: [(Int, String, Float)] -> [String]
aprovados alunos = 
    let aprovados = filter (\(_, _, nota) -> nota >= 6) alunos
    in map (\(_, nome, _) -> nome) aprovados

aprovados2 :: [(Int, String, Float)] -> [String]
aprovados2 [] = []
aprovados2 ((a,b,c):resto)
    | c >= 6 = b : aprovados resto
    | otherwise = aprovados resto

main = do
    print (gerarPares alunos alunos)