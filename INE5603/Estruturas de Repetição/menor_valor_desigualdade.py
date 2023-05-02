import math

num = 1000

for i in range(1, num):
    if math.factorial(i) > i **10:
        print(i)
        break
    
