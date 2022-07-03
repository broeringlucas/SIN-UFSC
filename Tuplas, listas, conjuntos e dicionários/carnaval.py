notas = [float(x) for x in input().split()]

notas.sort()
media = notas[1] + notas[2] + notas[3]

print(f"{media:0.1f}")