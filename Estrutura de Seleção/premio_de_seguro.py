
v_veiculo = float(input())
c_desconto = (input())
procedencia_carro = (input())
idade = int(input())

if procedencia_carro == "nacional":
    desconto_procedencia = 10/100
else:
    desconto_procedencia = 15/100

desconto_bruto = v_veiculo * desconto_procedencia

if c_desconto == "A":
    desconto_tipo_perc = 30 / 100
elif c_desconto == "B":
    desconto_tipo_perc = 20 / 100
elif c_desconto == "C":
    desconto_tipo_perc = 10 / 100
elif c_desconto == "D":
    desconto_tipo_perc = 5 / 100
else:
    desconto_tipo_perc = 0
    
desconto_tipo = desconto_bruto * desconto_tipo_perc

if idade > 24:
    desconto_idade_perc = 10/100
else:
    desconto_idade_perc = 0
    
desconto_idade = desconto_bruto * desconto_idade_perc

desconto = desconto_bruto - desconto_tipo - desconto_idade 

print(desconto)

