
import Data.Array


type Valor = Int

type Posicao = (Int, Int)

type Board = Array Posicao Valor


puzzleBoard :: Board
puzzleBoard = array ((0, 0), (8, 8)) $ puzzleTuplas examplePuzzle


examplePuzzle :: [[Valor]] 
examplePuzzle = [[5, 3, 0,  0, 7, 0,  0, 0, 0],
                 [6, 0, 0,  1, 9, 5,  0, 0, 0],
                 [0, 9, 8,  3, 0, 0,  0, 6, 0],
                 [8, 0, 0,  0, 6, 0,  0, 0, 3],
                 [4, 0, 0,  8, 0, 3,  0, 0, 1],
                 [7, 0, 0,  0, 2, 0,  0, 0, 6],
                 [0, 6, 0,  0, 0, 0,  2, 8, 0],
                 [0, 0, 0,  4, 1, 9,  0, 0, 5],
                 [0, 0, 0,  0, 8, 0,  1, 7, 9]]

puzzleTuplas :: [[Valor]] -> [(Posicao, Valor)]
puzzleTuplas = concatMap linhasTuplas . zip [0..8]
    where 
        linhasTuplas :: (Int, [Valor]) -> [((Int, Int), Valor)]
        linhasTuplas (linha, valores) = colTuplas linha $ zip [0..8] valores

        colTuplas :: Int -> [(Int, Valor)] -> [((Int, Int), Valor)]
        colTuplas row cols = map (\(col, m) -> ((row, col), m)) cols

posicoesVazias :: Board -> [Posicao]
posicoesVazias b = [(linha, col) | linha <- [0..8], col <- [0..8], b ! (linha, col) == 0]

posicoesLinha :: Board -> Int -> [Valor]
b `posicoesLinha` linha = [b ! loc | loc <- range ((linha, 0), (linha, 8))]

posicoesColuna :: Board -> Int -> [Valor]
b `posicoesColuna` col = [b ! loc | loc <- range ((0, col), (8, col))]

posicoesQuadrante :: Board -> Posicao -> [Valor]
b `posicoesQuadrante` (linha, col) = [b ! loc | loc <- locs]
    where
        locs = range ((linha', col'), (linha' + 2, col' + 2))
        linha' = 3 * (linha `div` 3)
        col' = 3 * (col `div` 3)

posicaoPossivel :: Valor -> Posicao -> Board -> Bool
posicaoPossivel m (linha, col) b = notInRow && notInCol && notInQuad
    where
        notInRow = m `notElem` (b `posicoesLinha` linha)
        notInCol = m `notElem` (b `posicoesColuna` col)
        notInQuad = m `notElem` (b `posicoesQuadrante` (linha, col))

copiaComValor :: Valor -> Posicao -> Board -> Board
copiaComValor valor (linha, col) b = b // [((linha, col), valor)]

solucoes :: Board -> [Board]
solucoes b = solucoes' (posicoesVazias b) b
    where
        solucoes' :: [Posicao] -> Board -> [Board]
        solucoes' [] b = [b]
        solucoes' (x:xs) b = concatMap (solucoes' xs) boardsCandidatos
            where
                valoresCandidatos = [m | m <- [1..9], posicaoPossivel m x b]
                boardsCandidatos = map (\m -> copiaComValor m x b) valoresCandidatos

printBoard :: Maybe Board -> IO ()
printBoard Nothing  = putStrLn "No solution"
printBoard (Just b) = mapM_ putStrLn [show $ b `posicoesLinha` row | row <- [0..8]]

primeiroOuNada :: [a] -> Maybe a
primeiroOuNada [] = Nothing
primeiroOuNada (x:xs) = Just x

solucionar :: Board -> Maybe Board
solucionar = primeiroOuNada . solucoes

main = do 
    printBoard $ solucionar puzzleBoard
    putStrLn "Done!"
