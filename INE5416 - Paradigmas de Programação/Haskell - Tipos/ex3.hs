
data Ponto = DoisD Float Float | TresD Float Float Float
distancia :: Ponto -> Ponto -> Float
distancia (DoisD x1 y1) (DoisD x2 y2) = sqrt((x2-x1)^2 + (y2-y1)^2)

main = do 
    print (distancia (DoisD 3 3) (DoisD 1 1))
