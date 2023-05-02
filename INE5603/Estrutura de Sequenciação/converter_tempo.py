n = int(input())

h = n // 3600
h1 = n % 3600

min = h1 // 60
min1 = h1 % 60

s = min1 

print(f"{h}:{min}:{s}")

