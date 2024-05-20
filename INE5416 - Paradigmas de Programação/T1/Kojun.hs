-- Lucas Broering
-- ghc Kojun.hs 
-- ./Kojun

import Data.List

import Matriz
import Control.Monad.RWS (MonadState(put))

-- Representa o grid do jogo
type Grid = Matriz Valor

-- Representa os valores possíveis para cada célula
type Seleção = [Valor]

-- | Funções referentes a divisão de um Grid (Tabuleiro) em regiões

-- divide a matriz base em regiões seguindo a matriz de regiões
matrizRegioes :: Eq m => Matriz m -> Grid -> [Linha m]
matrizRegioes valores regioes = [regiaoFilter regiao tuples | regiao <- regioesMap ]
    where
        -- monta uma lista de tuplas com os valores e suas regiões
        tuples = montarTuples valores regioes
        -- agrupa as regiões
        regioesMap = nub (map snd tuples)
        -- filtra as regiões
        regiaoFilter regiao list = map fst $ filter ((== regiao) . snd) list

-- retorna uma lista dos valores que já estão na região
valoresRegiao :: Eq m => Matriz m -> Grid -> Int -> [m]
valoresRegiao valores regioes id = map fst $ filter ((== id) . snd) tuples
    where
        tuples = montarTuples valores regioes

-- monta uma lista de tuplas com os valores e suas regiões
montarTuples :: Eq m => Matriz m -> Grid -> [(m, Int)]
montarTuples valores regioes = foldl1 (++) (zipWith zip valores regioes)

-- retorna o tamanho de uma região
tamRegiao :: Eq m => m -> Matriz m -> Int
tamRegiao _ [] = 0
tamRegiao id regioes = sum [count id x | x <- regioes]
    where
        count x xs = length (filter (== x) xs)

-- Refaz as colunas originais a partir das colunas da matriz de regiões
colunasOriginais :: [Linha l] -> Int -> [Linha l]
colunasOriginais bs n = dividir n (concat bs)

-- Divide uma lista em outras listas menores
dividir :: Int -> [a] -> [[a]]
dividir a = takeWhile (not . null) . map (take a) . iterate (drop a)

-- colunas da matriz dividida pelas regiões 
regioesColunas :: Eq m => Matriz m -> Grid -> [Linha m]
regioesColunas valores regioes = zipWith zip (colunas valores) (colunas regioes) >>= map (map fst) . groupBy (\x y -> snd x == snd y)

-- Funções referentes a lógica do Kojun 

-- valida adjacência, não pode haver valores iguais em células adjacentes
validarAdjacencia :: Eq a => Linha [a] -> Bool
validarAdjacencia [] = True
validarAdjacencia [x] = True
validarAdjacencia (x:y:xs)
    | length x <= 1 && length y <= 1 = (x /= y) && validarAdjacencia (y:xs)
    | otherwise = validarAdjacencia (y:xs)

-- valida linha, não pode haver valores iguais na linha
validarLinha :: Eq a => Linha [a] -> Bool
validarLinha [] = True
validarLinha (x:xs) = if (length x <= 1) then not (elem x xs) && validarLinha xs else validarLinha xs

-- valida linha em ordem descrecente
validarDescrescente :: Ord a => Linha [a] -> Bool
validarDescrescente [] = True
validarDescrescente [x] = True
validarDescrescente (x:y:xs)
    | length x <= 1 && length y <= 1 = (x >= y) && validarDescrescente (y:xs)
    | otherwise = validarDescrescente (y:xs)

-- valida seguindo todas as verificacoes do jogo 
validaMatriz :: Matriz Seleção -> Grid -> Bool
validaMatriz valores regioes = all validarAdjacencia (colunas valores) &&
                               all validarAdjacencia (linhas valores) &&
                               all validarLinha (matrizRegioes valores regioes) &&
                               all validarDescrescente (regioesColunas valores regioes)

-- verifica se a linha tem apenas um valor
apenasUmValor :: [a] -> Bool
apenasUmValor [_] = True
apenasUmValor _ = False

-- Faz a subtração entre duas listas
menos :: Seleção -> Seleção -> Seleção
xs `menos` ys = if apenasUmValor xs then xs else xs \\ ys

-- busca escolhas possíveis em cada espaço
buscaEscolhas :: Grid -> Grid -> Matriz Seleção
buscaEscolhas valores regioes = map (map escolha) (zipWith zip valores regioes)
    where
        -- escolhe um valor para o espaço, os valores já selecionados são removidos. As demais possuem valores referentes ao tamanho da região
        escolha (x, y) = if x == 0 then [1..tamRegiao y regioes] `menos` (valoresRegiao valores regioes y) else [x]

-- reduz escolhas usando a coluna dividida pelas regiões
reduzirEscolhas :: Matriz Seleção -> Grid -> Matriz Seleção
reduzirEscolhas valores regioes = colunas $ colunasOriginais (map reduzirEscolhasUnicas (regioesColunas valores regioes)) (ordem valores)

-- reduz escolhas únicas, seta o valor para um espaço que só possui uma escolha
reduzirEscolhasUnicas :: Linha Seleção -> Linha Seleção
reduzirEscolhasUnicas xss = [xs `menos` unicos | xs <- xss]
    where unicos = concat (filter apenasUmValor xss)

-- verifica se a matriz não possui solução
semSolucao :: Matriz Seleção -> Grid -> Bool
semSolucao valores regioes = vazia valores || not (validaMatriz valores regioes)

-- verifica  espaços vazios no grid
vazia :: Matriz Seleção -> Bool
vazia = any (any null)

-- expande as possibilidades de busca
buscaExpandida :: Matriz Seleção -> [Matriz Seleção]
buscaExpandida m = [linhas1 ++ [linha1 ++ [c] : linha2] ++ linhas2 | c <- cs]
    where
        (linhas1,linha:linhas2) = span (all apenasUmValor) m
        (linha1,cs:linha2) = span apenasUmValor linha

-- faz a filtragem das solucoes possíveis, seguindo a Seleção de valores
-- retorna uma lista de grids
buscaSolucoes :: Matriz Seleção -> Grid -> [Grid]
buscaSolucoes valores regioes
    -- quando não tem solucao retna uma lista vazia
    | semSolucao valores regioes = []
    -- quando todas as casas possuem escolha únicas, retorna a matriz
    | all (all apenasUmValor) valores = [map concat valores]
    -- expande as possibilidades de busca
    | otherwise = [x | valores' <- buscaExpandida valores, x <- buscaSolucoes (reduzirEscolhas valores' regioes) regioes]

-- Pega a primeira solucao encontrada da lista de solucoes
solucionar :: Grid -> Grid -> Grid
solucionar valores regioes = if null solucoes
                              then []
                              else head solucoes
  where
    solucoes = buscaSolucoes (reduzirEscolhas (buscaEscolhas valores regioes) regioes) regioes

valores6x6 :: Grid
valores6x6 = [[0,0,0,0,0,2],
             [2,0,0,5,0,0],
             [0,0,3,0,0,4],
             [0,0,0,3,0,1],
             [0,0,0,0,0,0],
             [0,0,3,0,2,5]]

regioes6x6 :: Grid
regioes6x6 = [[1,2,3,3,4,4],
            [1,2,5,4,4,4],
            [1,1,5,5,5,6],
            [8,8,7,6,6,6],
            [8,8,7,10,0,0],
            [9,9,10,10,10,10]]

valores10x10 :: Grid 
valores10x10 = [[4,0,7,0,4,6,3,0,2,3],
                [0,0,0,1,0,4,0,2,0,2],
                [2,0,0,4,0,0,7,0,0,4],
                [0,6,0,0,0,6,0,4,0,3],
                [5,0,5,0,4,0,6,0,0,1],
                [4,1,0,3,0,4,2,0,0,0],
                [0,0,1,0,0,7,0,3,0,7],
                [5,3,0,5,6,0,5,0,6,3],
                [3,0,4,0,0,0,0,0,0,0],
                [1,0,6,4,3,0,2,0,4,0]]

regioes10x10 :: Grid
regioes10x10 = [[1,1,2,2,2,2,2,3,3,3],
                [1,1,4,2,2,5,5,5,6,6],
                [7,7,4,8,8,5,9,9,9,10],
                [7,12,12,13,8,8,8,9,11,10],
                [12,12,13,13,13,8,9,9,10,10],
                [12,12,13,14,14,14,9,15,15,15],
                [16,16,14,14,14,17,17,17,15,18],
                [19,16,20,20,20,17,17,17,18,18],
                [19,16,16,20,20,21,17,22,18,18],
                [19,19,19,19,20,21,21,22,18,18]]

valores12x12 :: Grid
valores12x12 = [[4,0,0,3,0,3,0,0,2,0,0,0],
                [0,6,0,0,0,0,0,6,0,5,0,0],
                [0,2,0,3,4,0,2,0,0,4,0,4],
                [0,0,4,0,0,0,1,3,0,2,5,0],
                [0,0,0,5,0,5,0,1,0,0,2,0],
                [5,0,4,0,0,0,2,0,0,0,0,0],
                [0,0,0,0,0,2,0,2,4,0,4,0],
                [0,0,4,6,0,0,0,0,0,6,0,0],
                [0,2,0,0,0,7,0,0,3,0,1,4],
                [5,0,0,4,0,5,3,0,4,0,6,0],
                [0,0,0,0,7,0,0,0,0,0,0,3],
                [6,0,0,0,0,5,0,0,1,5,2,1]]

regioes12x12 :: Grid
regioes12x12 = [[1,1,1,2,3,4,4,5,6,6,6,6],
                [1,1,2,2,7,8,4,5,5,5,5,6],
                [1,1,7,7,7,8,9,10,10,5,5,6],
                [11,12,12,12,7,9,9,13,10,10,10,14],
                [11,11,12,12,15,15,13,13,16,16,17,18],
                [19,19,19,12,15,15,13,20,20,17,17,18],
                [19,19,21,21,15,15,22,23,20,20,18,18],
                [21,21,21,21,21,15,23,23,20,24,24,18],
                [25,25,25,25,26,23,23,27,24,24,24,24],
                [25,28,29,25,26,23,23,27,30,30,30,30],
                [25,28,28,28,28,31,31,31,32,32,32,30],
                [28,28,33,33,34,31,31,31,32,32,32,30]]


main = do

    let valores = valores6x6
    let regioes = regioes6x6
    let solucao = solucionar valores regioes
    
    -- putStrLn "Matriz Regioes"
    -- print (matrizRegioes valores regioes)
    -- putStrLn ""
    -- putStrLn "Valores Regiao"
    -- print (valoresRegiao valores regioes 4)
    -- putStrLn ""
    -- putStrLn "Tamanho Regiao"
    -- print (tamRegiao 4 regioes)
    -- putStrLn ""
    -- putStrLn "Regioes Colunas"
    -- print (regioesColunas valores regioes)
    -- putStrLn ""
    -- putStrLn "Colunas Originais"
    -- print (colunasOriginais valores 6)
    -- putStrLn ""
    -- putStrLn "Tuplas"
    -- print (montarTuples valores regioes)
    -- putStrLn ""
    -- putStrLn "-------------------------------------------------"
    putStrLn ""
    if null solucao
        then putStrLn "Sem solução"
        else mapM_ print solucao
    putStrLn ""