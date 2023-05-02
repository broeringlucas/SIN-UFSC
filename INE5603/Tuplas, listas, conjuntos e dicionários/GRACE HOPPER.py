test = [(x) for x in input().split("-")] 
palavra1 = ""
palavra2 = ""
while True:
    try:
        for i in range (len(test)): 
            if test[i][0].upper() in "COBOL":
                palavra1 += test[i][0].upper() 
            elif test[i][-1].upper() in "COBOL":
                palavra1 += test[i][-1].upper()
        if palavra1 == "COBOL": 
            print("GRACE HOPPER")
        elif palavra2 == "COBOL":
            print("GRACE HOPPER")
        else:
            print("BUG")

        test = [(x) for x in input().split("-")] 
        palavra1 = ""
        palavra2 = ""
    
    except EOFError:
        break
        

