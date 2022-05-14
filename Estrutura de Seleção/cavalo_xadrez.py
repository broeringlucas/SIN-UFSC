import math

x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())

mover = math.sqrt((x1 - x2)**2 + (y1 - y2)**2) == math.sqrt(5)

print(mover)