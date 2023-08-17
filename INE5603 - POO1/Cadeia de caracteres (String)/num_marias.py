num_nomes = int(input())

num_marias = 0

for _ in range(num_nomes):
    nome = input()
    if "Maria"  in nome:
        num_marias += 1
        if "Mariana" in nome:
            num_marias -= 1

print(num_marias)