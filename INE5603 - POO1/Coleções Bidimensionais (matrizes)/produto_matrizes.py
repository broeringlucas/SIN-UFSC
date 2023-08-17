n = int(input())

p, q, r, s, x, y = [int(x) for x in input().split()]
i, j = [int(x) for x in input().split()]

soma = 0
for k in range(1, n+1):
    a = (p * i + q * k) % x
    b = (r * k + s * j) % y
    soma += a * b

print(soma)
    
    