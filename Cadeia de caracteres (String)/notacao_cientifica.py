def main():
    num = float(input())
    return num

def converter_notacao_cientifica(num):
    contador = 0
    if 1 <= num < 10: 
        print('+{:.4f}E+00'.format(num))
    elif 0 < num < 1:
        while num < 1:
            contador += 1
            num *= 10
        if contador > 10:
            print('+{:.4f}E-{}'.format(num,contador))
        else:
            print('+{:.4f}E-0{}'.format(num,contador))
    elif num >= 10:
        while num >= 10:
            contador += 1
            num /= 10
        if contador > 10:
            print('+{:.4f}E+{}'.format(num,contador))
        else:
            print('+{:.4f}E+0{}'.format(num,contador))
    elif -10 < num < -1:
        print('-{:.4f}E+00{}'.format(abs(num)))
    elif -1 < num < 0:
        num = abs(num)
        while num < 1:
            contador += 1
            num *= 10
        if contador > 10:
            print('-{:.4f}E-{}'.format(num,contador))
        else:
            print('-{:.4f}E-0{}'.format(num,contador))
    elif num < -2:
        num = abs(num)
        while num > 2:
            contador += 1
            num /= 10
        if contador >= 10:
            print('-{:.4f}E+{}'.format(num,contador))
        else:
            print('-{:.4f}E+0{}'.format(num,contador))
            
                  
converter_notacao_cientifica(main())
