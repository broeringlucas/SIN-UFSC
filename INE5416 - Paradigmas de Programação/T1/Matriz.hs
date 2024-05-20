-- | Módulo que define o tipo Matriz e suas operações.
module Matriz(Valor, Linha, Matriz, linhas, colunas, ordem) where

import Data.List

-- Tipo que representa o valor de uma célula da matriz.
type Valor = Int
-- Tipo que representa uma linha da matriz.
type Linha a = [a]
--- Tipo que representa uma matriz.
type Matriz a = [Linha a]

-- Retorna a dimensao da matriz (ordem)
ordem :: Matriz a -> Int
ordem m = length (m !! 0)

-- Retorna as colunas de uma matriz
colunas :: Matriz a -> [Linha a]
colunas = transpose

-- Retorna as linhas de uma matriz
linhas :: Matriz a -> [Linha a]
linhas a = a

