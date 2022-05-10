import math

n = int(input())

P = round(n / math.log(n),1)
M = round(1.25506 * n / math.log(n),1)

print(P, M)
