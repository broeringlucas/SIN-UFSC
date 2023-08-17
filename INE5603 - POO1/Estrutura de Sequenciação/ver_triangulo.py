l1 = float(input())
l2 = float(input())
l3 = float(input())

cond_exist = l1 > abs(l2 - l3) and l2 > abs(l1 - l3) and l3 > abs(l1 - l2)

print(cond_exist)
