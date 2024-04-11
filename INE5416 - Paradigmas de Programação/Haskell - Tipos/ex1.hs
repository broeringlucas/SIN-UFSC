-- A 
type Nome = String
type Disciplina = String
type Nota = Float


type Aluno = (Nome, Disciplina, (Nota, Nota, Nota))

-- B
aluno :: Int -> Aluno
aluno 1 = ("Lucas", "Ingles", (10, 5.6, 7.8))
aluno 2 = ("Maria", "Portugues", (6.7, 8.9, 9.1))
aluno 3 = ("Joao", "Fisica", (7.6, 8.7, 9.8))
aluno _ = ("Desconhecido", "Desconhecido", (0, 0, 0))

-- C
getNome :: Aluno -> Nome
getNome (a,_,_) = a

-- D
media :: Aluno -> Float
media (_,_,(a,b,c)) = (a+b+c)/3

mediaTotal :: Int -> Float
mediaTotal n = (sum [media (aluno x) | x <- [1..n]]) / fromIntegral n


main = do
    nStr <- getLine
    let n = read nStr
    print (aluno n)
    print (getNome (aluno n))
    print (media (aluno n))
    print(mediaTotal 3)