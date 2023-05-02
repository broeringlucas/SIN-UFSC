quant_c = int(input())
quant_boi = int(input())
quant_b = int(input())
quant_m = int(input())
quant_l = int(input())

p_c = 300 * quant_c
p_boi = 1500 * quant_boi
p_b = 600 * quant_b
p_m = 1000 * quant_m
p_l = 150 * quant_l

quant_mandi = round(p_c + p_boi + p_b + p_m + p_l + 225)

print(quant_mandi)
