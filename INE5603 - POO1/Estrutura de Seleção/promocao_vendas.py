valor_total = float(input())

valor_com_desconto = valor_total * (80/100)

if valor_total >= 500: 
    valor_desconto = valor_total * (10/100)
    valor_com_desconto -= valor_desconto 
    if valor_total > 1000: 
        valor_total -= 1000
        valor_desconto = valor_total * (15/100)
        valor_com_desconto -= valor_desconto
        
print(valor_com_desconto)