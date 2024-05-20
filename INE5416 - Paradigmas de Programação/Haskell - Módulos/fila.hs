module Fila(Fila (Queue), emptyQueue, enqueue, dequeue, first) where


data Fila t = Queue [t]  
    deriving Show

emptyQueue :: Fila t
emptyQueue = Queue []

enqueue :: Fila t -> t -> Fila t
enqueue (Queue s) x = Queue (s ++ [x])

dequeue :: Fila t -> Fila t
dequeue (Queue []) = error "Empty"
dequeue (Queue (x:s)) = Queue s

first :: Fila t -> t
first (Queue []) = error "Empty"
first (Queue (x:s)) = x


