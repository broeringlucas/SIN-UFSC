n = int(input())

binario = "" 

if n == 0:
    binario = binario + "0"
else:
    
    while n != 0:
        if n % 2 == 0:
            binario = binario + "0"
        else:
            binario = binario + "1"
        n = n // 2

print(binario[::-1])