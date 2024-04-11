areaTriangulo :: Float -> Float -> Float
areaTriangulo base altura = (base * altura) / 2

main = do 
    baseStr <- getLine
    alturaStr <- getLine
    let base = (read baseStr :: Float)
    let altura = (read alturaStr :: Float)
    print (areaTriangulo base altura)