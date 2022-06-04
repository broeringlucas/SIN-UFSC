num = int(input())

while num != 0:
    sum_varetas = 0
    for _ in range(num):
        comprimento, quantidade = [int(x) for x in input().split()]
    
        if quantidade % 2 == 0:
            sum_varetas += quantidade
        else:
            sum_varetas += quantidade - 1
    
        num_retangulos = sum_varetas // 4
    print(num_retangulos)
    num = int(input())
    
    
