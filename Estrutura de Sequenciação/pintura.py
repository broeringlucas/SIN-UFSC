area = int(input())

area_galao = 64.8

n_galoes = round(max(area / area_galao ,1))
preco_total = round(n_galoes * 25)

print("- área de cobertura:",area)
print("- número de galões:",n_galoes)
print(f"- valor a ser pago: R$ {preco_total:.2f}")
