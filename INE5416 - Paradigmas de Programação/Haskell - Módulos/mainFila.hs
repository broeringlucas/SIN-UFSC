import Fila

main = do 
    putStrLn (show (enqueue (enqueue emptyQueue 1) 2))
    putStrLn (show (first (Queue [1,2,3,4,5])))
    putStrLn (show (dequeue (Queue [1,2,3,4,5])))
    putStrLn (show (dequeue (dequeue (Queue [1,2,3,4,5]))))