idade = int(input())

anos = idade // 365
resto_a = idade % 365

meses = resto_a // 30
dias = resto_a % 30


print(f"{anos} ano(s)")
print(f"{meses} mes(es)")
print(f"{dias} dia(s)")
