-- Definição de um módulo
module Exemplo where

-- Definição de uma classe
class Concatenable a where
    (+++) :: a -> a -> a
    (***) :: a -> a -> a  -- Definição do operador ***

-- Instância da classe para listas
instance Concatenable [a] where
    (+++) = (++)
    xs *** ys = xs ++ ys  -- Definição do operador ***

-- Definição de precedências para os operadores *** e +++
infixr 5 ***
infixl 6 +++

-- Função que utiliza os operadores definidos
foo :: [Int] -> [Int] -> [Int]
foo xs ys = xs +++ ys *** [1,2,3]
