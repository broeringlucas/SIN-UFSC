h = int(input())
h_e = int(input())

s_hora = 2500 / 200 

s_bruto = h * s_hora + h_e * (s_hora * 1.2)

inss = s_bruto * 0.09

ir = s_bruto * 0.13

s_liquido = (s_bruto - inss - ir)

print(f"- Salário Bruto : R$ {s_bruto:.2f}")
print(f"- IR (13%) : R$ {ir :.2f}")
print(f"- INSS (9%) : R$ {inss :.2f}")
print(f"- Salário Líquido : R$ {s_liquido:.2f}")

