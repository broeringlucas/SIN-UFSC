import math

x1, y1 = [float(w) for w in input().split()]
x2, y2 = [float(w) for w in input().split()]
 

x = (x2 - x1)**2 + (y2 - y1)**2

distan = round(math.sqrt(x),4)

print(distan)
