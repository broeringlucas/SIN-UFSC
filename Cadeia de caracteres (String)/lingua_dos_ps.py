mensagem_codificada = input()

tamanho_mensagem = len(mensagem_codificada)

mensagem_decodificada = ""

for i in range(tamanho_mensagem):
    letras = mensagem_codificada[i]
    if "p" not in letras:
        mensagem_decodificada += letras
        
print(mensagem_decodificada)


