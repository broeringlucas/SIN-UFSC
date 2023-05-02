
nota = float(input())

nota_inteiro = int(nota)
nota_decimal = nota - nota_inteiro

if nota_decimal < 0.25:
    nota_decimal = 0
elif 0.25 <= nota_decimal < 0.75:
    nota_decimal = 0.5
elif nota_decimal >= 0.75:
    nota_decimal = 1
    
nota_arredondada = nota_inteiro + nota_decimal 

print(nota_arredondada)