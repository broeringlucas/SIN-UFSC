-- Enumerações em Haskell
-- Em Haskell, podemos criar enumerações usando a palavra-chave data. 
-- Vamos supor que queremos criar uma enumeração para representar os dias da semana. Aqui está um exemplo:

data DiaDaSemana = Domingo | Segunda | Terca | Quarta | Quinta | Sexta | Sabado
    deriving (Read)

-- Função que verifica se um dia é final de semana
finalDeSemana :: DiaDaSemana -> Bool
finalDeSemana Sabado = True
finalDeSemana Domingo = True
finalDeSemana _ = False

-- Exemplo de uso
main :: IO ()
main = do
    putStrLn "Digite um dia da semana:"
    dia <- getLine
    let diaEnum = read dia :: DiaDaSemana
    putStrLn $ if finalDeSemana diaEnum then "É final de semana!" else "Não é final de semana."
